/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include "py/objstr.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/stream.h"
#include "extmod/vfs_fat.h"
#include "_vfs_stream.h"
#include "i2s_helper.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <freertos/semphr.h>
#include "driver/i2s_std.h"
#include "esp_log.h"
#include "esp_resample.h"

#include <ctype.h>
#include <math.h>

#ifndef MAX
#define MAX(a,b)    ((a) > (b) ? (a) : (b))
#endif

#define DEFAULT_RESAMPLE_FILTER_CONFIG() {           \
        .src_rate = 44100,                           \
        .src_ch = 2,                                 \
        .dest_rate = 48000,                          \
        .dest_bits = 16,                             \
        .dest_ch = 2,                                \
        .src_bits = 16,                              \
        .mode = RESAMPLE_DECODE_MODE,                \
        .max_indata_bytes = 512,                     \
        .out_len_bytes = 512,                        \
        .type = ESP_RESAMPLE_TYPE_AUTO,              \
        .complexity = 2,                             \
        .down_ch_idx = 0,                            \
        .prefer_flag = ESP_RSP_PREFER_TYPE_SPEED,    \
}

struct __attribute__((packed)) wav_header_t
{
    char RIFF[4];
    uint32_t chunk_size;
    char WAVEfmt[8];
    uint32_t fmt_chunk_size;
    uint16_t audiofmt;
    uint16_t channel;
    uint32_t sample_rate;
    uint32_t byte_per_sec;
    uint16_t block_size;
    uint16_t bit_per_sample;
};

struct __attribute__((packed)) sub_chunk_t
{
    char identifier[4];
    uint32_t chunk_size;
    // uint8_t data[1];
};

typedef enum play_state_t {
    PLAY_STATE_IDLE,
    PLAY_STATE_PLAYING,
    PLAY_STATE_PAUSED,
    PLAY_STATE_STOPPED,
} play_state_t;

typedef struct _audio2_player_obj_t {
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

    TaskHandle_t task_handle;

    // resample
    void *rsp_hd;
    resample_info_t resample_info;
    unsigned char *out_buf;
    unsigned char *in_buf;

    // play
    struct {
        struct {
            char path[128];
            int sample_rate;
            int channel;
            int bit_per_sample;
            int data_offset;
            int data_len;
        } wav_file;
        struct {
            const void *data;
            int sample_rate;
            int channel;
            int bit_per_sample;
            int data_offset;
            int data_len;
        } wav_buf;
        struct {
            int freq; // Hz
            int duration; // ms
        } tone;

        play_state_t state;
    } play_info;

} audio2_player_obj_t;

const static char *TAG = "Audio2";
extern const mp_obj_type_t audio2_player_type;

static void player_stop_helper(audio2_player_obj_t *self);

static void player_i2s_init_helper(audio2_player_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
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
    self->mode = I2S_MODE_TX;

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


static mp_obj_t player_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);

    audio2_player_obj_t *self = mp_obj_malloc(audio2_player_obj_t, &audio2_player_type);
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    player_i2s_init_helper(self, n_args, args, &kw_args);

    self->is_open = false;
    self->play_info.state = PLAY_STATE_IDLE;

    return self;
}


static void player_wav_file_task(void *arg) {
    audio2_player_obj_t *self = (audio2_player_obj_t *)arg;

    ESP_LOGI(TAG, "player task started");

    resample_info_t resample_info = DEFAULT_RESAMPLE_FILTER_CONFIG();
    memcpy(&self->resample_info, &resample_info, sizeof(resample_info_t));
    self->resample_info.dest_rate = self->sample_rate;
    self->resample_info.dest_bits = self->bits;
    self->resample_info.dest_ch = self->channel;
    self->resample_info.src_rate = self->play_info.wav_file.sample_rate;
    self->resample_info.src_bits = self->play_info.wav_file.bit_per_sample;
    self->resample_info.src_ch = self->play_info.wav_file.channel;

    self->rsp_hd = esp_resample_create(&self->resample_info, (unsigned char **)&self->in_buf, (unsigned char **)&self->out_buf);
    if (self->rsp_hd == NULL) {
        ESP_LOGI(TAG, "Failed to create the resample handler");
    }
    ESP_LOGI(TAG,
        "source rate: %d, source channel: %d, source bits: %d, destination rate: %d, destination channel: %d, destination bits: %d",
        self->resample_info.src_rate,
        self->resample_info.src_ch,
        self->resample_info.src_bits,
        self->resample_info.dest_rate,
        self->resample_info.dest_ch,
        self->resample_info.dest_bits
        );

    ESP_LOGI(TAG, "open path %s", self->play_info.wav_file.path);

    void *wav_file = vfs_stream_open(self->play_info.wav_file.path, VFS_READ);

    vfs_stream_seek(wav_file, self->play_info.wav_file.data_offset, SEEK_SET);
    ESP_LOGI(TAG, "file pos: %ld", vfs_stream_tell(wav_file));

    uint32_t data_len = self->play_info.wav_file.data_len;
    bool flg_16bit = (self->play_info.wav_file.bit_per_sample >> 4);

    size_t buf_num = 3;
    size_t buf_size = 256;
    uint8_t wav_data[buf_num][buf_size];

    size_t idx = 0;
    int in_offset = buf_size;
    while (data_len > 0) {

        if (self->play_info.state == PLAY_STATE_STOPPED) {
            ESP_LOGI(TAG, "player task stopped");
            break;
        }

        if (self->play_info.state == PLAY_STATE_PAUSED) {
            vTaskDelay(10 / portTICK_PERIOD_MS);
            continue;
        }

        size_t len = (data_len > buf_size) ? buf_size : data_len;
        // mp_printf(&mp_plat_print, "buf idx: %d len: %d data_len: %d\r\n", idx, len, data_len);
        if (vfs_stream_read(wav_file, (uint8_t *)wav_data[idx], len) != len) {
            vfs_stream_close(wav_file);
            ESP_LOGE(TAG, "File is too short");
            break;
        }
        data_len -= len;

        if (len != in_offset && len > 0) {
            memset(self->in_buf + len, 0, in_offset - len);
        }
        int in_bytes_consumed = esp_resample_run(
            self->rsp_hd,
            &self->resample_info,
            wav_data[idx],
            self->out_buf,
            len,
            &self->resample_info.out_len_bytes
            );

        // ESP_LOGE(TAG, "in_bytes_consumed: %d, out_len_bytes: %d", in_bytes_consumed, self->resample_info.out_len_bytes);

        size_t num_bytes_written = 0;
        esp_err_t ret = i2s_channel_write(self->i2s_chan_handle, self->out_buf, self->resample_info.out_len_bytes, &num_bytes_written, portMAX_DELAY);

        idx = idx < (buf_num - 1) ? idx + 1 : 0;
    }

    vfs_stream_close(wav_file);

    esp_resample_destroy(self->rsp_hd);

    self->play_info.state = PLAY_STATE_IDLE;

    vTaskDelete(NULL);
}


static bool check_file_type(const char *path) {
    // check file type
    char ftype[5] = {0};
    for (size_t i = 0; i < 4; i++) {
        ftype[i] = tolower((char)path[i + strlen(path) - 4]);
    }
    ftype[4] = '\0';
    if (strcmp(ftype, ".wav") != 0) {
        return false;
    }
    return true;
}

static mp_obj_t player_play_wav_file(mp_obj_t self_in, mp_obj_t path_in) {
    audio2_player_obj_t *self = self_in;
    const char *path = mp_obj_str_get_str(path_in);

    // check file type
    if (check_file_type(path) == false) {
        mp_raise_ValueError(MP_ERROR_TEXT("file type not supported"));
    }

    // stop previous task
    player_stop_helper(self);

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
    file_args[0] = path_in;
    file_args[1] = mp_obj_new_str("rb", strlen("rb"));
    mp_obj_t wav_file = mp_vfs_open(2, file_args, (mp_map_t *)&mp_const_empty_map);
    if (wav_file == mp_const_none) {
        mp_raise_OSError(MP_ENOENT);
        // mp_raise_ValueError(MP_ERROR_TEXT("open file failed"));
    }

    struct wav_header_t header;
    int rlen = mp_stream_posix_read(wav_file, &header, sizeof(struct wav_header_t));
    if (rlen != sizeof(struct wav_header_t)) {
        mp_stream_close(wav_file);
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
    }

    if (memcmp(header.RIFF, "RIFF", 4)
        || memcmp(header.WAVEfmt, "WAVEfmt ", 8)
        || header.audiofmt != 1
        || header.bit_per_sample < 8
        || header.bit_per_sample > 16
        || header.channel == 0
        || header.channel > 2
        || header.sample_rate < 8000
        || header.sample_rate > 96000) {
        mp_stream_close(wav_file);
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("file format is not supported"));
    }

    ESP_LOGI(TAG,
        "wav bit_per_sample: %d, channel: %d, sample_rate: %ld",
        header.bit_per_sample,
        header.channel,
        header.sample_rate
        );

    struct sub_chunk_t sub_chunk;
    while (true) {
        if (mp_stream_posix_read(wav_file, &sub_chunk, sizeof(struct sub_chunk_t)) != sizeof(struct sub_chunk_t)) {
            mp_stream_close(wav_file);
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
        }

        if (strncmp(sub_chunk.identifier, "data", 4) == 0) {
            break;
        }

        if (mp_stream_posix_lseek(wav_file, sub_chunk.chunk_size, SEEK_CUR) == -1) {
            mp_stream_close(wav_file);
            mp_raise_OSError(MP_ESPIPE);
        }
    }

    memset(self->play_info.wav_file.path, 0, sizeof(self->play_info.wav_file.path));
    memcpy(self->play_info.wav_file.path, path, strlen(path));
    self->play_info.wav_file.sample_rate = header.sample_rate;
    self->play_info.wav_file.channel = header.channel;
    self->play_info.wav_file.bit_per_sample = header.bit_per_sample;
    self->play_info.wav_file.data_offset = mp_stream_posix_lseek(wav_file, 0, SEEK_CUR);
    self->play_info.wav_file.data_len = sub_chunk.chunk_size;
    self->play_info.state = PLAY_STATE_PLAYING;

    mp_stream_close(wav_file);

    ESP_LOGE(TAG, "path: %s, data_offset: %d", self->play_info.wav_file.path, self->play_info.wav_file.data_offset);

    #if portNUM_PROCESSORS > 1
    xTaskCreatePinnedToCore(
        player_wav_file_task,
        "player_wav_file_task",
        4096,
        self,
        5,
        &self->task_handle,
        0
        );
    #else
    xTaskCreate(
        player_wav_file_task,
        "player_wav_file_task",
        4096,
        self,
        5,
        &self->task_handle
        );
    #endif

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(player_play_wav_file_obj, player_play_wav_file);


static void player_tone_task(void *arg) {
    audio2_player_obj_t *self = (audio2_player_obj_t *)arg;

    ESP_LOGI(TAG, "player tone task started");

    #define AMPLITUDE  (32767)
    #define PI         (3.1415926)

    #define SINE_LUT_SIZE 16
    static const int16_t sine_lut[SINE_LUT_SIZE] = {
        0,       12539,  23169,  30272,
        32767,   30272,  23169,  12539,
        0,      -12539, -23169, -30272,
        -32767, -30272, -23169, -12539
    };
    int freq = self->play_info.tone.freq;
    double duration = (double)(self->play_info.tone.duration / 1000.0);

    size_t sample_data_len = round((double)(self->sample_rate * self->channel * ((self->bits >> 3) / 2) * duration));
    size_t remaining_length = sample_data_len;

    ESP_LOGI(TAG, "sample_data_len: %d", sample_data_len);

    size_t buf_num = 3;
    size_t buf_size = 256;
    int16_t wav_data[buf_num][buf_size];

    size_t i = 0;
    size_t idx = 0;

    double step = (double)SINE_LUT_SIZE * freq / self->sample_rate;
    double lidx = 0.0;

    while (remaining_length > 0) {
        if (self->play_info.state == PLAY_STATE_STOPPED) {
            ESP_LOGI(TAG, "player task stopped");
            break;
        }

        if (self->play_info.state == PLAY_STATE_PAUSED) {
            vTaskDelay(10 / portTICK_PERIOD_MS);
            continue;
        }

        int read_size = buf_size;
        if (buf_size > remaining_length) {
            read_size = remaining_length;
        }

        int index = 0;
        int end = i + read_size;
        for (; i < end; i++) {
            wav_data[idx][index++] = sine_lut[(uint32_t)lidx % SINE_LUT_SIZE];
            // Accumulate and take a new phase next time
            lidx += step;
            if (lidx >= SINE_LUT_SIZE) {
                lidx -= SINE_LUT_SIZE;
            }
        }
        remaining_length = sample_data_len - i;

        size_t num_bytes_written = 0;
        esp_err_t ret = i2s_channel_write(
            self->i2s_chan_handle,
            wav_data[idx],
            read_size * 2,
            &num_bytes_written,
            portMAX_DELAY
            );

        idx = idx < (buf_num - 1) ? idx + 1 : 0;
    }

    self->play_info.state = PLAY_STATE_IDLE;
    vTaskDelete(NULL);
}


static mp_obj_t player_tone(mp_obj_t self_in, mp_obj_t freq_in, mp_obj_t duration_in) {
    audio2_player_obj_t *self = self_in;
    self->play_info.tone.freq = mp_obj_get_int(freq_in);
    self->play_info.tone.duration = mp_obj_get_int(duration_in);

    // stop previous task
    player_stop_helper(self);

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

    self->play_info.state = PLAY_STATE_PLAYING;

    #if portNUM_PROCESSORS > 1
    xTaskCreatePinnedToCore(
        player_tone_task,
        "player_tone_task",
        4096,
        self,
        5,
        &self->task_handle,
        0
        );
    #else
    xTaskCreate(
        player_tone_task,
        "player_tone_task",
        4096,
        self,
        5,
        &self->task_handle
        );
    #endif

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(player_tone_obj, player_tone);


static void player_wav_task(void *arg) {
    audio2_player_obj_t *self = (audio2_player_obj_t *)arg;

    ESP_LOGI(TAG, "player task started");

    resample_info_t resample_info = DEFAULT_RESAMPLE_FILTER_CONFIG();
    memcpy(&self->resample_info, &resample_info, sizeof(resample_info_t));
    self->resample_info.dest_rate = self->sample_rate;
    self->resample_info.dest_bits = self->bits;
    self->resample_info.dest_ch = self->channel;
    self->resample_info.src_rate = self->play_info.wav_buf.sample_rate;
    self->resample_info.src_bits = self->play_info.wav_buf.bit_per_sample;
    self->resample_info.src_ch = self->play_info.wav_buf.channel;

    self->rsp_hd = esp_resample_create(&self->resample_info, (unsigned char **)&self->in_buf, (unsigned char **)&self->out_buf);
    if (self->rsp_hd == NULL) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("Failed to create the resample handler"));
    }
    ESP_LOGI(TAG,
        "source rate: %d, source channel: %d, source bits: %d, destination rate: %d, destination channel: %d, destination bits: %d",
        self->resample_info.src_rate,
        self->resample_info.src_ch,
        self->resample_info.src_bits,
        self->resample_info.dest_rate,
        self->resample_info.dest_ch,
        self->resample_info.dest_bits
        );

    uint32_t data_len = self->play_info.wav_buf.data_len;
    size_t data_offset = self->play_info.wav_buf.data_offset;
    bool flg_16bit = (self->play_info.wav_buf.bit_per_sample >> 4);

    size_t buf_num = 3;
    size_t buf_size = 256;
    uint8_t wav_data[buf_num][buf_size];

    size_t idx = 0;
    int in_offset = buf_size;
    while (data_len > 0) {
        if (self->play_info.state == PLAY_STATE_STOPPED) {
            ESP_LOGI(TAG, "player task stopped");
            break;
        }

        if (self->play_info.state == PLAY_STATE_PAUSED) {
            vTaskDelay(10 / portTICK_PERIOD_MS);
            continue;
        }

        size_t len = (data_len > buf_size) ? buf_size : data_len;
        if (data_offset + len > self->play_info.wav_buf.data_len) {
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
        }
        memcpy(wav_data[idx], &((uint8_t *)self->play_info.wav_buf.data)[data_offset], len);
        data_offset += len;

        data_len -= len;

        if (len != in_offset && len > 0) {
            memset(self->in_buf + len, 0, in_offset - len);
        }
        int in_bytes_consumed = esp_resample_run(
            self->rsp_hd,
            &self->resample_info,
            wav_data[idx],
            self->out_buf,
            len,
            &self->resample_info.out_len_bytes
            );

        // ESP_LOGE(TAG, "in_bytes_consumed: %d, out_len_bytes: %d", in_bytes_consumed, self->resample_info.out_len_bytes);

        size_t num_bytes_written = 0;
        esp_err_t ret = i2s_channel_write(self->i2s_chan_handle, self->out_buf, self->resample_info.out_len_bytes, &num_bytes_written, portMAX_DELAY);

        idx = idx < (buf_num - 1) ? idx + 1 : 0;
    }

    esp_resample_destroy(self->rsp_hd);

    self->play_info.state = PLAY_STATE_IDLE;

    vTaskDelete(NULL);
}


static mp_obj_t player_play_wav(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_buf, ARG_duration };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_buf,         MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_duration,    MP_ARG_KW_ONLY |MP_ARG_INT,   { .u_int = -1 }          },
        /* *FORMAT-ON* */
    };

    // parse args
    audio2_player_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[ARG_buf].u_obj, &bufinfo, MP_BUFFER_READ);
    size_t buf_offset = 0;
    int duration = args[ARG_duration].u_int;

    // stop previous task
    player_stop_helper(self);

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

    if (bufinfo.len < sizeof(struct wav_header_t)) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
    }
    struct wav_header_t header;
    const uint8_t *ptr = (const uint8_t *)bufinfo.buf;
    memcpy(&header, ptr + buf_offset, sizeof(struct wav_header_t));
    buf_offset += sizeof(struct wav_header_t);

    ESP_LOGE(TAG, "wav bit_per_sample: %d, channel: %d, sample_rate: %ld", header.bit_per_sample, header.channel, header.sample_rate);

    if (memcmp(header.RIFF, "RIFF", 4)
        || memcmp(header.WAVEfmt, "WAVEfmt ", 8)
        || header.audiofmt != 1
        || header.bit_per_sample < 8
        || header.bit_per_sample > 16
        || header.channel == 0
        || header.channel > 2
        || header.sample_rate < 8000
        || header.sample_rate > 96000) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("file format is not supported"));
    }

    struct sub_chunk_t sub_chunk;
    while (true) {
        if (buf_offset + sizeof(struct sub_chunk_t) > bufinfo.len) {
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
        }
        memcpy(&sub_chunk, ptr + buf_offset, sizeof(struct sub_chunk_t));
        buf_offset += sizeof(struct sub_chunk_t);

        if (strncmp(sub_chunk.identifier, "data", 4) == 0) {
            break;
        }

        if (buf_offset + sub_chunk.chunk_size > bufinfo.len) {
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
        }
        buf_offset += sub_chunk.chunk_size;
    }

    ESP_LOGE(TAG, "buf_offset: %d", buf_offset);

    self->play_info.wav_buf.data = bufinfo.buf + buf_offset;
    self->play_info.wav_buf.sample_rate = header.sample_rate;
    self->play_info.wav_buf.channel = header.channel;
    self->play_info.wav_buf.bit_per_sample = header.bit_per_sample;
    self->play_info.wav_buf.data_offset = 0;
    self->play_info.wav_buf.data_len = round((double)(duration / 1000.0) * header.sample_rate * header.channel * (header.bit_per_sample >> 3));
    if (duration == -1 || self->play_info.wav_buf.data_len > sub_chunk.chunk_size) {
        self->play_info.wav_buf.data_len = sub_chunk.chunk_size;
    }

    self->play_info.state = PLAY_STATE_PLAYING;

    #if portNUM_PROCESSORS > 1
    xTaskCreatePinnedToCore(
        player_wav_task,
        "player_wav_task",
        4096,
        self,
        5,
        &self->task_handle,
        0
        );
    #else
    xTaskCreate(
        player_wav_task,
        "player_wav_task",
        4096,
        self,
        5,
        &self->task_handle
        );
    #endif

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(player_play_wav_obj, 2, player_play_wav);


static mp_obj_t player_play_raw(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_buf, ARG_rate, ARG_bits, ARG_channel, ARG_duration };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_buf,         MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_rate,        MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 16000 }       },
        { MP_QSTR_bits,        MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = 16 }          },
        { MP_QSTR_channel,     MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = STEREO }      },
        { MP_QSTR_duration,    MP_ARG_KW_ONLY | MP_ARG_INT,  { .u_int = -1 }          },
        /* *FORMAT-ON* */
    };

    // parse args
    audio2_player_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[ARG_buf].u_obj, &bufinfo, MP_BUFFER_READ);

    // stop previous task
    player_stop_helper(self);

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

    uint32_t sample_rate = args[ARG_rate].u_int;
    uint16_t channel = args[ARG_channel].u_int;
    uint16_t bit_per_sample = args[ARG_bits].u_int;
    int duration = args[ARG_duration].u_int;

    if (duration == 0) {
        return mp_const_none;
    }

    self->play_info.wav_buf.data = bufinfo.buf;
    self->play_info.wav_buf.sample_rate = sample_rate;
    self->play_info.wav_buf.channel = channel;
    self->play_info.wav_buf.bit_per_sample = bit_per_sample;
    self->play_info.wav_buf.data_offset = 0;
    self->play_info.wav_buf.data_len = round((double)(duration / 1000.0) * sample_rate * channel * (bit_per_sample >> 3));
    if (duration == -1 || self->play_info.wav_buf.data_len > bufinfo.len) {
        self->play_info.wav_buf.data_len = bufinfo.len;
    }

    self->play_info.state = PLAY_STATE_PLAYING;

    #if portNUM_PROCESSORS > 1
    xTaskCreatePinnedToCore(
        player_wav_task,
        "player_wav_task",
        4096,
        self,
        5,
        &self->task_handle,
        0
        );
    #else
    xTaskCreate(
        player_wav_task,
        "player_wav_task",
        4096,
        self,
        5,
        &self->task_handle
        );
    #endif

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(player_play_raw_obj, 2, player_play_raw);


static mp_obj_t player_pause(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;

    self->play_info.state = PLAY_STATE_PAUSED;

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_pause_obj, player_pause);


static mp_obj_t player_resume(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;

    if (self->play_info.state == PLAY_STATE_PAUSED) {
        self->play_info.state = PLAY_STATE_PLAYING;
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_resume_obj, player_resume);


static void player_stop_helper(audio2_player_obj_t *self) {
    if (self->play_info.state == PLAY_STATE_IDLE) {
        return;
    }
    self->play_info.state = PLAY_STATE_STOPPED;
    while (self->play_info.state != PLAY_STATE_IDLE) {
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

static mp_obj_t player_stop(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;

    player_stop_helper(self);

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_stop_obj, player_stop);


static mp_obj_t player_is_running(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;

    return mp_obj_new_bool(self->is_open);
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_is_running_obj, player_is_running);


static mp_obj_t player_is_playing(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;

    return mp_obj_new_bool(self->play_info.state == PLAY_STATE_PLAYING);
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_is_playing_obj, player_is_playing);


static mp_obj_t player_set_volume_percentage(mp_obj_t self_in, mp_obj_t volume_in) {
    audio2_player_obj_t *self = self_in;
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(player_set_volume_percentage_obj, player_set_volume_percentage);


static mp_obj_t player_get_volume_percentage(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_get_volume_percentage_obj, player_get_volume_percentage);


static mp_obj_t player_init(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;
    if (self->is_open) {
        return mp_const_none;
    }

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

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_init_obj, player_init);


static mp_obj_t player_deinit(mp_obj_t self_in) {
    audio2_player_obj_t *self = self_in;
    if (self->is_open) {
        player_stop_helper(self);
        i2s_std_deinit_helper(self->i2s_chan_handle);
    }
    self->is_open = false;
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(player_deinit_obj, player_deinit);


static const mp_rom_map_elem_t player_locals_dict_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_play_wav_file),         MP_ROM_PTR(&player_play_wav_file_obj)         },
    { MP_ROM_QSTR(MP_QSTR_tone),                  MP_ROM_PTR(&player_tone_obj)                  },
    { MP_ROM_QSTR(MP_QSTR_play_wav),              MP_ROM_PTR(&player_play_wav_obj)              },
    { MP_ROM_QSTR(MP_QSTR_play_raw),              MP_ROM_PTR(&player_play_raw_obj)              },
    { MP_ROM_QSTR(MP_QSTR_pause),                 MP_ROM_PTR(&player_pause_obj)                 },
    { MP_ROM_QSTR(MP_QSTR_resume),                MP_ROM_PTR(&player_resume_obj)                },
    { MP_ROM_QSTR(MP_QSTR_stop),                  MP_ROM_PTR(&player_stop_obj)                  },
    { MP_ROM_QSTR(MP_QSTR_is_running),            MP_ROM_PTR(&player_is_running_obj)            },
    { MP_ROM_QSTR(MP_QSTR_is_playing),            MP_ROM_PTR(&player_is_playing_obj)            },
    { MP_ROM_QSTR(MP_QSTR_set_volume_percentage), MP_ROM_PTR(&player_set_volume_percentage_obj) },
    { MP_ROM_QSTR(MP_QSTR_get_volume_percentage), MP_ROM_PTR(&player_get_volume_percentage_obj) },
    { MP_ROM_QSTR(MP_QSTR_init),                  MP_ROM_PTR(&player_init_obj)                  },
    { MP_ROM_QSTR(MP_QSTR_deinit),                MP_ROM_PTR(&player_deinit_obj)                },
    /* *FORMAT-ON* */
};

static MP_DEFINE_CONST_DICT(player_locals_dict, player_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    audio2_player_type,
    MP_QSTR_Player,
    MP_TYPE_FLAG_NONE,
    make_new, player_make_new,
    locals_dict, &player_locals_dict
    );
