/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include "i2s_helper.h"
#include "format_wav.h"

#include "py/objstr.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/stream.h"
#include "extmod/vfs_fat.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <freertos/semphr.h>
#include "driver/i2s_std.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "esp_resample.h"

#include <stdio.h>
#include <string.h>
#include <math.h>

#ifndef MAX
#define MAX(a,b)    ((a) > (b) ? (a) : (b))
#endif

#define RESAMPLE_MAX_INDATA_BYTES 512
#define RESAMPLE_OUTDATA_BYTES 512

#define DEFAULT_RESAMPLE_FILTER_CONFIG() {           \
        .src_rate = 44100,                               \
        .src_ch = 2,                                     \
        .dest_rate = 48000,                              \
        .dest_bits = 16,                                 \
        .dest_ch = 2,                                    \
        .src_bits = 16,                                  \
        .mode = RESAMPLE_DECODE_MODE,                    \
        .max_indata_bytes = RESAMPLE_MAX_INDATA_BYTES,   \
        .out_len_bytes = RESAMPLE_OUTDATA_BYTES,         \
        .type = ESP_RESAMPLE_TYPE_AUTO,                  \
        .complexity = 2,                                 \
        .down_ch_idx = 0,                                \
        .prefer_flag = ESP_RSP_PREFER_TYPE_SPEED,        \
}


typedef struct _audio_recorder_obj_t {
    mp_obj_base_t base;
    bool is_open;
    i2s_port_t i2s_id;
    int sample_rate;
    i2s_mode_t mode;
    mp_hal_pin_obj_t sck;
    mp_hal_pin_obj_t ws;
    mp_hal_pin_obj_t sd;
    mp_hal_pin_obj_t mck;
    int bits;
    channel_t channel;
    i2s_chan_handle_t i2s_chan_handle;

    // resample
    void *rsp_hd;
    resample_info_t resample_info;
    unsigned char *out_buf;
    unsigned char *in_buf;

    struct {
        void *buf;
        size_t cur_len;
        size_t total;
    } pcm_buf;

} audio2_recorder_obj_t;

const static char *TAG = "Audio2";

extern const mp_obj_type_t audio2_recorder_type;


static void recorder_i2s_init_helper(audio2_recorder_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_id, ARG_sck, ARG_ws, ARG_sd, ARG_mck, ARG_rate, ARG_bits, ARG_channel };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_id,      MP_ARG_REQUIRED | MP_ARG_INT, { .u_int = 0 }           },
        { MP_QSTR_sck,     MP_ARG_KW_ONLY | MP_ARG_OBJ,  { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_ws,      MP_ARG_KW_ONLY | MP_ARG_OBJ,  { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_sd,      MP_ARG_KW_ONLY | MP_ARG_OBJ,  { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_mck,     MP_ARG_KW_ONLY | MP_ARG_OBJ,  { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_rate,    MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 16000 }       },
        { MP_QSTR_bits,    MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 16 }          },
        { MP_QSTR_channel, MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = STEREO }      },
        /* *FORMAT-ON* */
    };

    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    self->i2s_id = args[ARG_id].u_int;
    self->sck = args[ARG_sck].u_obj == MP_OBJ_NULL ? -1 : mp_hal_get_pin_obj(args[ARG_sck].u_obj);
    self->ws = args[ARG_ws].u_obj == MP_OBJ_NULL ? -1 : mp_hal_get_pin_obj(args[ARG_ws].u_obj);
    self->sd = args[ARG_sd].u_obj == MP_OBJ_NULL ? -1 : mp_hal_get_pin_obj(args[ARG_sd].u_obj);
    self->mck = args[ARG_mck].u_obj == MP_OBJ_NULL ? -1 : mp_hal_get_pin_obj(args[ARG_mck].u_obj);
    self->sample_rate = args[ARG_rate].u_int;
    self->bits = args[ARG_bits].u_int;
    self->channel = args[ARG_channel].u_int;
    self->mode = I2S_MODE_RX;

    #if 0
    check_esp_err(i2s_std_init_helper(
        self->i2s_id,
        self->mode,
        self->sck,
        self->ws,
        self->sd,
        self->mck,
        self->sample_rate,
        self->bits,
        self->channel,
        &self->i2s_chan_handle
        ));
    #endif
}


static mp_obj_t recorder_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);

    audio2_recorder_obj_t *self = mp_obj_malloc(audio2_recorder_obj_t, &audio2_recorder_type);
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    recorder_i2s_init_helper(self, n_args, args, &kw_args);

    self->is_open = false;

    self->pcm_buf.buf = NULL;
    self->pcm_buf.cur_len = 0;
    self->pcm_buf.total = 0;

    return self;
}


static void recorder_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
    audio2_recorder_obj_t *self = (audio2_recorder_obj_t *)MP_OBJ_TO_PTR(self_in);
    if (dest[0] == MP_OBJ_NULL) {
        // Load
        if (attr == MP_QSTR_pcm_buffer) {
            dest[0] = mp_obj_new_bytearray_by_ref(self->pcm_buf.cur_len, self->pcm_buf.buf);
        } else {
            // Continue lookup in locals_dict.
            dest[1] = MP_OBJ_SENTINEL;
        }
    } else if (dest[1] != MP_OBJ_NULL) {
        // Store
    }
}


static mp_obj_t recorder_init(mp_obj_t self_in) {
    audio2_recorder_obj_t *self = self_in;
    if (self->is_open == false) {
        check_esp_err(i2s_std_init_helper(
            self->i2s_id,
            self->mode,
            self->sck,
            self->ws,
            self->sd,
            self->mck,
            self->sample_rate,
            self->bits,
            self->channel,
            &self->i2s_chan_handle
            ));
        self->is_open = true;
    }

    return mp_obj_new_bool(self->is_open);
}
static MP_DEFINE_CONST_FUN_OBJ_1(recorder_init_obj, recorder_init);


static mp_obj_t recorder_deinit(size_t n_args, const mp_obj_t *args) {
    audio2_recorder_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    if (self->is_open) {
        i2s_std_deinit_helper(self->i2s_chan_handle);
        self->is_open = false;
    }

    if (n_args > 1) {
        if (mp_obj_is_true(args[1])) {
            if (self->pcm_buf.buf) {
                m_free(self->pcm_buf.buf);
            }
            self->pcm_buf.buf = NULL;
            self->pcm_buf.cur_len = 0;
            self->pcm_buf.total = 0;
        }
    }

    return mp_obj_new_bool(self->is_open);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(recorder_deinit_obj, 1, 2, recorder_deinit);


static mp_obj_t recorder_is_running(mp_obj_t self_in) {
    audio2_recorder_obj_t *self = self_in;

    return mp_obj_new_bool(self->is_open);
}
static MP_DEFINE_CONST_FUN_OBJ_1(recorder_is_running_obj, recorder_is_running);


static mp_obj_t recorder_record_wav_file(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_path, ARG_rate, ARG_bits, ARG_channel, ARG_duration };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_path,     MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = mp_const_none }   },
        { MP_QSTR_rate,     MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 16000 }           },
        { MP_QSTR_bits,     MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 16 }              },
        { MP_QSTR_channel,  MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = STEREO }          },
        { MP_QSTR_duration, MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 3000 }            },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    audio2_recorder_obj_t *self = args_in[0];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    const char *path = mp_obj_str_get_str(args[ARG_path].u_obj);
    if (self->sample_rate != args[ARG_rate].u_int ||
        self->bits != args[ARG_bits].u_int ||
        self->channel != args[ARG_channel].u_int
        ) {
        self->sample_rate = args[ARG_rate].u_int;
        self->bits = args[ARG_bits].u_int;
        self->channel = args[ARG_channel].u_int;

        i2s_std_deinit_helper(self->i2s_chan_handle);
        check_esp_err(i2s_std_init_helper(
            self->i2s_id,
            self->mode,
            self->sck,
            self->ws,
            self->sd,
            self->mck,
            self->sample_rate,
            self->bits,
            self->channel,
            &self->i2s_chan_handle
            ));
        self->is_open = true;
    }

    if (self->is_open == false) {
        check_esp_err(i2s_std_init_helper(
            self->i2s_id,
            self->mode,
            self->sck,
            self->ws,
            self->sd,
            self->mck,
            self->sample_rate,
            self->bits,
            self->channel,
            &self->i2s_chan_handle
            ));
        self->is_open = true;
    }

    mp_obj_t file_args[2];
    file_args[0] = args[ARG_path].u_obj;
    file_args[1] = mp_obj_new_str("wb+", strlen("wb+"));
    mp_obj_t wav_file = mp_vfs_open(2, file_args, (mp_map_t *)&mp_const_empty_map);
    if (wav_file == mp_const_none) {
        mp_raise_OSError(MP_ENOENT);
        // mp_raise_ValueError(MP_ERROR_TEXT("open file failed"));
    }

    size_t src_len = round((double)(args[ARG_duration].u_int / 1000.0) * self->sample_rate * self->channel * (self->bits >> 3));

    wav_header_t wav_header = WAV_HEADER_PCM_DEFAULT(src_len, self->bits, self->sample_rate, self->channel);
    int rlen = mp_stream_posix_write(wav_file, &wav_header, sizeof(wav_header_t));
    if (rlen != sizeof(wav_header_t)) {
        mp_stream_close(wav_file);
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
    }

    static const size_t I2S_CHUNK_SIZE = 512;
    int16_t *chunk_buf = m_malloc(I2S_CHUNK_SIZE);
    if (!chunk_buf) {
        mp_stream_close(wav_file);
        mp_raise_OSError(MP_ENOMEM);
    }
    size_t read_len = 0;
    if (self->channel == 1) {
        src_len *= 2; // 实际读取立体声的大小（假设用户是期望录 N 秒的单声道）
    }

    while (read_len < src_len) {
        size_t to_read = I2S_CHUNK_SIZE;
        if (src_len - read_len < I2S_CHUNK_SIZE) {
            to_read = src_len - read_len;
        }

        size_t bytes_read = 0;
        i2s_channel_read(
            self->i2s_chan_handle,
            chunk_buf,
            to_read,
            &bytes_read,
            portMAX_DELAY
            );
        if (bytes_read > 0) {
            if (self->channel == 1) {
                // 从立体声中提取左声道，每组 2 个 int16_t（4 字节）取一个
                int sample_count = bytes_read / (self->bits >> 2);  // 每帧立体声 4 字节
                for (int i = 0; i < sample_count; i++) {
                    chunk_buf[i] = chunk_buf[i * 2]; // 取左声道
                }
                mp_stream_posix_write(wav_file, chunk_buf, bytes_read / 2);
            } else {
                mp_stream_posix_write(wav_file, chunk_buf, bytes_read);
            }
            read_len += bytes_read;
        }
    }

    mp_stream_close(wav_file);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(recorder_record_wav_file_obj, 2, recorder_record_wav_file);


static mp_obj_t recorder_record(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_rate, ARG_bits, ARG_channel, ARG_duration };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_rate,     MP_ARG_KW_ONLY | MP_ARG_INT, { .u_int = 16000 }   },
        { MP_QSTR_bits,     MP_ARG_KW_ONLY | MP_ARG_INT, { .u_int = 16 }      },
        { MP_QSTR_channel,  MP_ARG_KW_ONLY | MP_ARG_INT, { .u_int = STEREO }  },
        { MP_QSTR_duration, MP_ARG_KW_ONLY | MP_ARG_INT, { .u_int = 3000 }    },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    audio2_recorder_obj_t *self = args_in[0];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (self->sample_rate != args[ARG_rate].u_int ||
        self->bits != args[ARG_bits].u_int ||
        self->channel != args[ARG_channel].u_int
        ) {
        self->sample_rate = args[ARG_rate].u_int;
        self->bits = args[ARG_bits].u_int;
        self->channel = args[ARG_channel].u_int;
        i2s_std_deinit_helper(self->i2s_chan_handle);
        check_esp_err(i2s_std_init_helper(
            self->i2s_id,
            self->mode,
            self->sck,
            self->ws,
            self->sd,
            self->mck,
            self->sample_rate,
            self->bits,
            self->channel,
            &self->i2s_chan_handle
            ));
        self->is_open = true;
    }

    if (self->is_open == false) {
        check_esp_err(i2s_std_init_helper(
            self->i2s_id,
            self->mode,
            self->sck,
            self->ws,
            self->sd,
            self->mck,
            self->sample_rate,
            self->bits,
            self->channel,
            &self->i2s_chan_handle
            ));
        self->is_open = true;
    }

    size_t src_len = round((double)(args[ARG_duration].u_int / 1000.0) * self->sample_rate * self->channel * (self->bits >> 3));
    if (src_len > self->pcm_buf.total) {
        self->pcm_buf.buf = m_realloc(self->pcm_buf.buf, src_len);
        self->pcm_buf.total = src_len;
    }
    self->pcm_buf.cur_len = src_len;

    ESP_LOGE(TAG, "src_len: %d", src_len);

    size_t read_len = 0;

    while (read_len < src_len) {
        size_t bytes_read = 0;
        i2s_channel_read(
            self->i2s_chan_handle,
            &self->pcm_buf.buf[read_len],
            src_len - read_len,
            &bytes_read,
            portMAX_DELAY
            );
        read_len += bytes_read;
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(recorder_record_obj, 1, recorder_record);


static const mp_rom_map_elem_t recorder_locals_dict_table[] = {
    /* *FORMAT-OFF* */
    // methods
    { MP_ROM_QSTR(MP_QSTR_init),            MP_ROM_PTR(&recorder_init_obj)            },
    { MP_ROM_QSTR(MP_QSTR_deinit),          MP_ROM_PTR(&recorder_deinit_obj)          },
    { MP_ROM_QSTR(MP_QSTR_is_running),      MP_ROM_PTR(&recorder_is_running_obj)      },
    { MP_ROM_QSTR(MP_QSTR_record_wav_file), MP_ROM_PTR(&recorder_record_wav_file_obj) },
    { MP_ROM_QSTR(MP_QSTR_record),          MP_ROM_PTR(&recorder_record_obj)          },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(recorder_locals_dict, recorder_locals_dict_table);


MP_DEFINE_CONST_OBJ_TYPE(
    audio2_recorder_type,
    MP_QSTR_Recorder,
    MP_TYPE_FLAG_NONE,
    make_new, recorder_make_new,
    attr, recorder_attr,
    locals_dict, &recorder_locals_dict
    );
