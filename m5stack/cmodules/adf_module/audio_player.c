/*
 * ESPRESSIF MIT License
 *
 * Copyright (c) 2019 <ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD>
 * Copyright (c) 2024 M5Stack Technology CO LTD
 *
 * Permission is hereby granted for use on all ESPRESSIF SYSTEMS products, in which case,
 * it is free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the Software is furnished
 * to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include <stdio.h>
#include <string.h>
#include <math.h>

#include "py/objstr.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "esp_audio.h"

#include "amr_decoder.h"
#include "mp3_decoder.h"
#include "wav_decoder.h"
#include "pcm_decoder.h"

#include "http_stream.h"
#include "vfs_stream.h"
#include "i2s_stream.h"
#include "raw_stream.h"

#include "board_init.h"
#include "esp_log.h"

typedef struct _audio_player_obj_t {
    mp_obj_base_t base;
    mp_obj_t callback;

    esp_audio_handle_t player;
    mp_obj_dict_t *state;
    int volume;
} audio_player_obj_t;

static const qstr player_info_fields[] = {
    MP_QSTR_input, MP_QSTR_codec
};

typedef struct play_info_t {
    esp_audio_handle_t player;

    union {
        struct {
            uint16_t freq;
            float time;
        } tone;
        struct {
            char *buf;
            int len;
            int sample_rates;
            int channels;
            int bits;
        } raw;
    } info;
} play_info_t;

audio_element_handle_t i2s_stream_writer;
static audio_element_handle_t raw_stream_reader;
static audio_element_handle_t pcm_decoder;
static TaskHandle_t play_tone_bg_task_handle = NULL;
static TaskHandle_t play_raw_bg_task_handle = NULL;
static bool play_tone_task_running = false;
static bool play_raw_task_running = false;
static bool pause_flag = false;

static const MP_DEFINE_STR_OBJ(player_info_input_obj, "http|file stream");
static const MP_DEFINE_STR_OBJ(player_info_codec_obj, "mp3|amr");

static MP_DEFINE_ATTRTUPLE(
    player_info_obj,
    player_info_fields,
    2,
    (mp_obj_t)&player_info_input_obj,
    (mp_obj_t)&player_info_codec_obj);

extern const mp_obj_type_t audio_player_type;


static mp_obj_t player_info(void) {
    return (mp_obj_t)&player_info_obj;
}
static MP_DEFINE_CONST_FUN_OBJ_0(audio_player_info_obj, player_info);


static void audio_state_cb(esp_audio_state_t *state, void *ctx) {
    audio_player_obj_t *self = (audio_player_obj_t *)ctx;

    if (self->callback != mp_const_none) {
        mp_obj_dict_t *dict = self->state;

        mp_obj_dict_store(dict, MP_ROM_QSTR(MP_QSTR_status), MP_OBJ_TO_PTR(mp_obj_new_int(state->status)));
        mp_obj_dict_store(dict, MP_ROM_QSTR(MP_QSTR_err_msg), MP_OBJ_TO_PTR(mp_obj_new_int(state->err_msg)));
        mp_obj_dict_store(dict, MP_ROM_QSTR(MP_QSTR_media_src), MP_OBJ_TO_PTR(mp_obj_new_int(state->media_src)));

        mp_sched_schedule(self->callback, dict);
    }
}


static int _http_stream_event_handle(http_stream_event_msg_t *msg) {
    if (msg->event_id == HTTP_STREAM_RESOLVE_ALL_TRACKS) {
        return ESP_OK;
    }

    if (msg->event_id == HTTP_STREAM_FINISH_TRACK) {
        return http_stream_next_track(msg->el);
    }
    if (msg->event_id == HTTP_STREAM_FINISH_PLAYLIST) {
        return http_stream_restart(msg->el);
    }
    return ESP_OK;
}


static esp_audio_handle_t audio_player_create(void) {
    // init player
    esp_audio_cfg_t cfg = DEFAULT_ESP_AUDIO_CONFIG();
    cfg.vol_handle = board_codec_init();
    cfg.vol_set = (audio_volume_set)board_codec_volume_set;
    cfg.vol_get = (audio_volume_get)board_codec_volume_get;
    cfg.resample_rate = 48000;
    cfg.prefer_type = ESP_AUDIO_PREFER_MEM;
    esp_audio_handle_t player = esp_audio_create(&cfg);

    // add input stream
    // fatfs stream
    vfs_stream_cfg_t fs_reader = VFS_STREAM_CFG_DEFAULT();
    fs_reader.type = AUDIO_STREAM_READER;
    fs_reader.task_core = 1;
    esp_audio_input_stream_add(player, vfs_stream_init(&fs_reader));
    // http stream
    http_stream_cfg_t http_cfg = HTTP_STREAM_CFG_DEFAULT();
    http_cfg.event_handle = _http_stream_event_handle;
    http_cfg.type = AUDIO_STREAM_READER;
    http_cfg.enable_playlist_parser = true;
    http_cfg.task_core = 1;
    audio_element_handle_t http_stream_reader = http_stream_init(&http_cfg);
    esp_audio_input_stream_add(player, http_stream_reader);
    // raw stream
    raw_stream_cfg_t raw_cfg = RAW_STREAM_CFG_DEFAULT();
    raw_cfg.type = AUDIO_STREAM_READER;
    raw_stream_reader = raw_stream_init(&raw_cfg);
    esp_audio_input_stream_add(player, raw_stream_reader);

    // add decoder
    // mp3
    mp3_decoder_cfg_t mp3_dec_cfg = BOARD_MP3_DECODER_CONFIG();
    esp_audio_codec_lib_add(player, AUDIO_CODEC_TYPE_DECODER, mp3_decoder_init(&mp3_dec_cfg));
    // amr
    amr_decoder_cfg_t amr_dec_cfg = BOARD_AMR_DECODER_CONFIG();
    esp_audio_codec_lib_add(player, AUDIO_CODEC_TYPE_DECODER, amr_decoder_init(&amr_dec_cfg));
    // wav
    wav_decoder_cfg_t wav_dec_cfg = BOARD_WAV_DECODER_CONFIG();
    esp_audio_codec_lib_add(player, AUDIO_CODEC_TYPE_DECODER, wav_decoder_init(&wav_dec_cfg));
    // pcm
    pcm_decoder_cfg_t pcm_dec_cfg = BOARD_PCM_DECODER_CONFIG();
    pcm_decoder = pcm_decoder_init(&pcm_dec_cfg);
    esp_audio_codec_lib_add(player, AUDIO_CODEC_TYPE_DECODER, pcm_decoder);

    // Create writers and add to esp_audio
    // i2s_stream_cfg_t i2s_writer = I2S_STREAM_CFG_DEFAULT_WITH_PARA(I2S_NUM_0, 48000, I2S_DATA_BIT_WIDTH_16BIT, AUDIO_STREAM_WRITER);
    if (i2s_stream_writer == NULL) {
        i2s_stream_cfg_t i2s_writer = BOARD_I2S_STREAM_CFG_DEFAULT();
        i2s_stream_writer = i2s_stream_init(&i2s_writer);
        esp_audio_output_stream_add(player, i2s_stream_writer);
    }

    return player;
}


static mp_obj_t audio_player_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, 1, false);

    static esp_audio_handle_t basic_player = NULL;

    audio_player_obj_t *self = mp_obj_malloc(audio_player_obj_t, &audio_player_type);
    self->callback = args[0];
    if (basic_player == NULL) {
        basic_player = audio_player_create();
    }
    self->player = basic_player;
    self->state = mp_obj_new_dict(3);
    self->volume = 50;
    esp_audio_vol_set(self->player, self->volume);

    return MP_OBJ_FROM_PTR(self);
}


static mp_obj_t audio_player_play_helper(audio_player_obj_t *self, mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_uri, ARG_pos, ARG_volume, ARG_sync, };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_uri,    MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = mp_const_none } },
        { MP_QSTR_pos,    MP_ARG_INT,                   { .u_int = 0 }             },
        { MP_QSTR_volume, MP_ARG_INT,                   { .u_int = -1 }            },
        { MP_QSTR_sync,   MP_ARG_BOOL,                  { .u_bool = true }         },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_uri].u_obj == mp_const_none) {
        check_esp_err(ESP_ERR_AUDIO_INVALID_PARAMETER);
        return mp_obj_new_int(ESP_ERR_AUDIO_INVALID_PARAMETER);
    }

    const char *uri = mp_obj_str_get_str(args[ARG_uri].u_obj);
    int pos = args[ARG_pos].u_int;
    bool sync = args[ARG_sync].u_bool;
    int volume = args[ARG_volume].u_int;

    // mp_printf(&mp_plat_print, "audio_player_play_helper: uri=%s, pos=%d, sync=%d, volume=%d\n", uri, pos, sync, volume);

    // 停止 raw task
    if (play_raw_task_running) {
        play_raw_task_running = false;
        while (play_raw_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    // 停止 tone task
    if (play_tone_task_running) {
        play_tone_task_running = false;
        while (play_tone_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    esp_audio_state_t state = { 0 };
    esp_audio_state_get(self->player, &state);
    if (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED) {
        esp_audio_stop(self->player, TERMINATION_TYPE_NOW);
        int wait = 20;
        esp_audio_state_get(self->player, &state);
        while (wait-- && (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED)) {
            vTaskDelay(pdMS_TO_TICKS(100));
            esp_audio_state_get(self->player, &state);
        }
    }
    esp_audio_callback_set(self->player, audio_state_cb, self);

    check_esp_err(esp_audio_vol_set(self->player, volume == -1 ? self->volume : volume));

    if (sync == true) {
        mp_obj_t dest[2];
        mp_load_method(self->state, MP_QSTR_clear, dest);
        mp_call_method_n_kw(0, 0, dest);

        mp_obj_dict_store(self->state, MP_ROM_QSTR(MP_QSTR_status),     MP_OBJ_TO_PTR(mp_obj_new_int(AUDIO_STATUS_UNKNOWN)));
        mp_obj_dict_store(self->state, MP_ROM_QSTR(MP_QSTR_err_msg),    MP_OBJ_TO_PTR(mp_obj_new_int(ESP_ERR_AUDIO_NO_ERROR)));
        mp_obj_dict_store(self->state, MP_ROM_QSTR(MP_QSTR_media_src),  MP_OBJ_TO_PTR(mp_obj_new_int(0)));

        return mp_obj_new_int(esp_audio_sync_play(self->player, uri, pos));
    } else {
        return mp_obj_new_int(esp_audio_play(self->player, AUDIO_CODEC_TYPE_DECODER, uri, pos));
    }

    return mp_const_none;
}


static mp_obj_t audio_player_play(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    return audio_player_play_helper(args[0], n_args - 1, args + 1, kw_args);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_player_play_obj, 1, audio_player_play);



void audio_player_play_raw_helper(esp_audio_handle_t player, char *buf, int len, int sample_rates, int channels, int bits, bool sync) {
    audio_element_info_t info;
    audio_element_getinfo(pcm_decoder, &info);
    info.sample_rates = sample_rates;
    info.channels = channels;
    info.bits = bits;
    audio_element_setinfo(pcm_decoder, &info);

    int remaining_length = len;
    size_t i = 0;

    esp_audio_play(player, AUDIO_CODEC_TYPE_DECODER, "raw://48000:1/flash/test.pcm", 0);

    int index = 0;
    while (play_raw_task_running || sync) {

        if (pause_flag) {
            vTaskDelay(pdMS_TO_TICKS(100));
            continue;
        }

        int read_size = 4096;
        if (remaining_length == 0 || remaining_length == 1) {
            // mp_printf(&mp_plat_print, "raw play complete\n");
            audio_element_set_ringbuf_done(raw_stream_reader);
            audio_element_finish_state(raw_stream_reader);
            break;
        } else if (4096 < remaining_length) {
            read_size = 4096;
        } else if (4096 > remaining_length) {
            read_size = remaining_length;
        }

        remaining_length -= read_size;
        raw_stream_write(raw_stream_reader, &buf[index * 4096], read_size);
        index++;
    }

    if (remaining_length > 0) {
        // mp_printf(&mp_plat_print, "tone raw complete\n");
        audio_element_set_ringbuf_done(raw_stream_reader);
        audio_element_finish_state(raw_stream_reader);
    }

    if (sync) {
        esp_audio_state_t state = { 0 };
        esp_audio_state_get(player, &state);
        if (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED) {
            int wait = 20;
            esp_audio_state_get(player, &state);
            while (wait-- && (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED)) {
                vTaskDelay(pdMS_TO_TICKS(100));
                esp_audio_state_get(player, &state);
            }
        }
    }

}


static void play_raw_bg_task(void *arg) {
    play_info_t *play_info = (play_info_t *)arg;

    ESP_LOGI("*", "play_tone_bg_task");

    audio_player_play_raw_helper(
        play_info->player,
        play_info->info.raw.buf,
        play_info->info.raw.len,
        play_info->info.raw.sample_rates,
        play_info->info.raw.channels,
        play_info->info.raw.bits,
        false
        );

    play_raw_bg_task_handle = NULL;
    vTaskDelete(NULL);
}


static mp_obj_t audio_player_play_raw(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_data, ARG_sample, ARG_stereo, ARG_bits, ARG_pos, ARG_volume, ARG_sync, };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_data,   MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = mp_const_none } },
        { MP_QSTR_sample, MP_ARG_INT,                   { .u_int= 16000 }          },
        { MP_QSTR_stereo, MP_ARG_BOOL,                  { .u_bool = false }        },
        { MP_QSTR_bits,   MP_ARG_INT,                   { .u_int = 16 }            },
        { MP_QSTR_pos,    MP_ARG_INT,                   { .u_int = 0 }             },
        { MP_QSTR_volume, MP_ARG_INT,                   { .u_int = -1 }            },
        { MP_QSTR_sync,   MP_ARG_BOOL,                  { .u_bool = true }         },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    audio_player_obj_t *self = (audio_player_obj_t *)args_in[0];
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[ARG_data].u_obj, &bufinfo, MP_BUFFER_READ);
    int sample = args[ARG_sample].u_int;
    bool stereo = args[ARG_stereo].u_bool;
    int bits = args[ARG_bits].u_int;
    int pos = args[ARG_pos].u_int;
    int volume = args[ARG_volume].u_int;
    bool sync = args[ARG_sync].u_bool;

    // 停止 raw task
    if (play_raw_task_running) {
        play_raw_task_running = false;
        while (play_raw_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    // 停止 tone task
    if (play_tone_task_running) {
        play_tone_task_running = false;
        while (play_tone_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    esp_audio_state_t state = { 0 };
    esp_audio_state_get(self->player, &state);
    if (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED) {
        esp_audio_stop(self->player, TERMINATION_TYPE_NOW);
        int wait = 20;
        esp_audio_state_get(self->player, &state);
        while (wait-- && (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED)) {
            vTaskDelay(pdMS_TO_TICKS(100));
            esp_audio_state_get(self->player, &state);
        }
    }
    esp_audio_callback_set(self->player, audio_state_cb, self);

    check_esp_err(esp_audio_vol_set(self->player, volume == -1 ? self->volume : volume));

    audio_element_info_t info;
    audio_element_getinfo(pcm_decoder, &info);
    info.sample_rates = sample;
    info.channels = stereo ? 2 : 1;
    audio_element_setinfo(pcm_decoder, &info);

    int remaining_length = bufinfo.len;

    if (args[ARG_sync].u_bool == true) {
        pause_flag = false;
        audio_player_play_raw_helper(self->player, bufinfo.buf, bufinfo.len, sample, stereo ? 2 : 1, bits, true);
    } else {
        static play_info_t play_info;
        play_info.player = self->player;
        play_info.info.raw.buf = bufinfo.buf;
        play_info.info.raw.len = bufinfo.len;
        play_info.info.raw.sample_rates = sample;
        play_info.info.raw.channels = stereo ? 2 : 1;
        play_info.info.raw.bits = bits;
        play_raw_task_running = true;
        pause_flag = false;
        BaseType_t createStatus = xTaskCreatePinnedToCore(
            play_raw_bg_task,
            "play_raw_bg_task",
            4 * 1024,
            &play_info,
            5,
            &play_raw_bg_task_handle,
            1
            );
        if (createStatus != pdPASS) {
            ESP_LOGI("*", "audio_play_tone_bg create task fail");
            play_raw_bg_task_handle = NULL;
        }
    }


    // if (args[ARG_sync].u_bool == true) {

    // } else {
    //     esp_audio_play(((audio_player_obj_t *)args_in[0])->player, AUDIO_CODEC_TYPE_DECODER, "raw://48000:1/flash/test.pcm", 0);

    //     int index = 0;
    //     while (true) {
    //         int read_size = 4096;
    //         if (remaining_length == 0 || remaining_length == 1) {
    //             mp_printf(&mp_plat_print, "raw play complete\n");
    //             audio_element_set_ringbuf_done(raw_stream_reader);
    //             audio_element_finish_state(raw_stream_reader);
    //             break;
    //         } else if (4096 < remaining_length) {
    //             read_size = 4096;
    //         } else if (4096 > remaining_length) {
    //             read_size = remaining_length;
    //         }

    //         remaining_length -= read_size;
    //         raw_stream_write(raw_stream_reader, &(((char *)bufinfo.buf)[index * 4096]), read_size);
    //         index++;
    //     }
    // }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_player_play_raw_obj, 1, audio_player_play_raw);


void audio_player_play_tone_helper(esp_audio_handle_t player, uint16_t freq, float time, bool sync) {
    #define AMPLITUDE  (32767)
    #define PI         (3.1415926)
    #define SAMPLE_BIT (16)
    #define TONE_SAMPLE_RATE (8000)

    audio_element_info_t info;
    audio_element_getinfo(pcm_decoder, &info);
    info.sample_rates = TONE_SAMPLE_RATE;
    info.channels = 1;
    audio_element_setinfo(pcm_decoder, &info);

    double increment = 2.0 * PI * freq / TONE_SAMPLE_RATE;
    size_t sample_data_len = round((double)(TONE_SAMPLE_RATE * 2 * time));
    int remaining_length = sample_data_len;
    size_t i = 0;
    double phase = 0.0;

    esp_audio_play(player, AUDIO_CODEC_TYPE_DECODER, "raw://48000:1/flash/test.pcm", 0);

    char *buf = (char *)malloc(4096);
    while (play_tone_task_running || sync) {
        if (pause_flag) {
            vTaskDelay(pdMS_TO_TICKS(100));
            continue;
        }

        int read_size = 4096;
        if (remaining_length == 0 || remaining_length == 1) {
            // mp_printf(&mp_plat_print, "tone play complete\n");
            audio_element_set_ringbuf_done(raw_stream_reader);
            audio_element_finish_state(raw_stream_reader);
            break;
        } else if (4096 < remaining_length) {
            read_size = 4096;
        } else if (4096 > remaining_length) {
            read_size = remaining_length;
        }

        int index = 0;
        int end = i + read_size / 2;
        for (; i < end; i++) {
            uint16_t sample_data = (int16_t)(AMPLITUDE * sin(phase));
            memcpy(&buf[index * 2], &sample_data, 2);
            index++;
            phase += increment;
        }
        remaining_length = sample_data_len - i * 2;
        raw_stream_write(raw_stream_reader, buf, read_size);
    }

    if (remaining_length > 0) {
        // mp_printf(&mp_plat_print, "tone play complete\n");
        audio_element_set_ringbuf_done(raw_stream_reader);
        audio_element_finish_state(raw_stream_reader);
    }

    if (sync) {
        esp_audio_state_t state = { 0 };
        esp_audio_state_get(player, &state);
        if (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED) {
            int wait = 20;
            esp_audio_state_get(player, &state);
            while (wait-- && (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED)) {
                vTaskDelay(pdMS_TO_TICKS(100));
                esp_audio_state_get(player, &state);
            }
        }
    }
    free(buf);
}


static void play_tone_bg_task(void *arg) {
    play_info_t *play_info = (play_info_t *)arg;

    ESP_LOGI("*", "play_tone_bg_task");

    audio_player_play_tone_helper(play_info->player, play_info->info.tone.freq, play_info->info.tone.time, false);

    play_tone_bg_task_handle = NULL;
    vTaskDelete(NULL);
}


static mp_obj_t audio_player_play_tone(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_freq, ARG_time, ARG_volume, ARG_sync, };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_freq,   MP_ARG_REQUIRED | MP_ARG_INT, { .u_int = 1000 }           },
        { MP_QSTR_time,   MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = mp_const_none }  },
        { MP_QSTR_volume, MP_ARG_INT,                   { .u_int = -1 }             },
        { MP_QSTR_sync,   MP_ARG_BOOL,                  { .u_bool = false } },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    audio_player_obj_t *self = (audio_player_obj_t *)args_in[0];
    int freq = args[ARG_freq].u_int;
    float time = mp_obj_get_float(args[ARG_time].u_obj);
    int volume = args[ARG_volume].u_int;
    bool sync = args[ARG_sync].u_bool;

    check_esp_err(esp_audio_vol_set(self->player, volume == -1 ? self->volume : volume));

    // 停止 raw task
    if (play_raw_task_running) {
        play_raw_task_running = false;
        while (play_raw_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    // 停止 tone task
    if (play_tone_task_running) {
        play_tone_task_running = false;
        while (play_tone_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    esp_audio_state_t state = { 0 };
    esp_audio_state_get(self->player, &state);
    if (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED) {
        esp_audio_stop(self->player, TERMINATION_TYPE_NOW);
        int wait = 20;
        esp_audio_state_get(self->player, &state);
        while (wait-- && (state.status == AUDIO_STATUS_RUNNING || state.status == AUDIO_STATUS_PAUSED)) {
            vTaskDelay(pdMS_TO_TICKS(100));
            esp_audio_state_get(self->player, &state);
        }
    }
    esp_audio_callback_set(self->player, audio_state_cb, self);

    if (sync == true) {
        pause_flag = false;
        audio_player_play_tone_helper(self->player, freq, time, true);
    } else {
        static play_info_t play_info;
        play_info.player = self->player;
        play_info.info.tone.freq = freq;
        play_info.info.tone.time = time;
        play_tone_task_running = true;
        pause_flag = false;
        BaseType_t createStatus = xTaskCreatePinnedToCore(
            play_tone_bg_task,
            "play_tone_bg_task",
            4 * 1024,
            &play_info,
            5,
            &play_tone_bg_task_handle,
            1
            );
        if (createStatus != pdPASS) {
            ESP_LOGI("*", "audio_play_tone_bg create task fail");
            play_tone_bg_task_handle = NULL;
        }
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_player_play_tone_obj, 1, audio_player_play_tone);


static mp_obj_t audio_player_stop_helper(audio_player_obj_t *self, mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_termination, };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_termination, MP_ARG_INT, { .u_int = TERMINATION_TYPE_NOW } },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    return mp_obj_new_int(esp_audio_stop(self->player, args[ARG_termination].u_int));
}


static mp_obj_t audio_player_stop(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    // 停止 raw task
    if (play_raw_task_running) {
        play_raw_task_running = false;
        while (play_raw_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    // 停止 tone task
    if (play_tone_task_running) {
        play_tone_task_running = false;
        while (play_tone_bg_task_handle != NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }

    return audio_player_stop_helper(args[0], n_args - 1, args + 1, kw_args);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_player_stop_obj, 1, audio_player_stop);


static mp_obj_t audio_player_pause(mp_obj_t self_in) {
    audio_player_obj_t *self = self_in;
    pause_flag = true;
    return mp_obj_new_int(esp_audio_pause(self->player));
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_player_pause_obj, audio_player_pause);


static mp_obj_t audio_player_resume(mp_obj_t self_in) {
    audio_player_obj_t *self = self_in;
    pause_flag = false;
    return mp_obj_new_int(esp_audio_resume(self->player));
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_player_resume_obj, audio_player_resume);


static mp_obj_t audio_player_vol_helper(audio_player_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_vol, };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_vol, MP_ARG_INT, { .u_int = 0xffff } },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_vol].u_int == 0xffff) {
        int vol = 0;
        esp_audio_vol_get(self->player, &vol);
        return mp_obj_new_int(vol);
    } else {
        if (args[ARG_vol].u_int >= 0 && args[ARG_vol].u_int <= 100) {
            self->volume = args[ARG_vol].u_int;
            return mp_obj_new_int(esp_audio_vol_set(self->player, args[ARG_vol].u_int));
        } else {
            return mp_obj_new_int(ESP_ERR_AUDIO_INVALID_PARAMETER);
        }
    }
}


static mp_obj_t audio_player_vol(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    return audio_player_vol_helper(args[0], n_args - 1, args + 1, kw_args);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_player_vol_obj, 1, audio_player_vol);


static mp_obj_t audio_player_get_vol(mp_obj_t self_in) {
    audio_player_obj_t *self = self_in;
    int vol = 0;
    // esp_audio_vol_get(self->player, &vol);
    return mp_obj_new_int(self->volume);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_player_get_vol_obj, audio_player_get_vol);


static mp_obj_t audio_player_set_vol(mp_obj_t self_in, mp_obj_t vol) {
    audio_player_obj_t *self = self_in;
    int volume = mp_obj_get_int(vol);

    if (volume < 0 || volume > 100) {
        mp_raise_ValueError("Volume must be between 0 and 100");
    }

    self->volume = volume;
    return mp_obj_new_int(esp_audio_vol_set(self->player, volume));
}
static MP_DEFINE_CONST_FUN_OBJ_2(audio_player_set_vol_obj, audio_player_set_vol);


static mp_obj_t audio_player_state(mp_obj_t self_in) {
    audio_player_obj_t *self = self_in;
    esp_audio_state_t state = { 0 };
    esp_audio_state_get(self->player, &state);
    mp_obj_dict_t *dict = self->state;

    mp_obj_dict_store(dict, MP_ROM_QSTR(MP_QSTR_status), MP_OBJ_TO_PTR(mp_obj_new_int(state.status)));
    mp_obj_dict_store(dict, MP_ROM_QSTR(MP_QSTR_err_msg), MP_OBJ_TO_PTR(mp_obj_new_int(state.err_msg)));
    mp_obj_dict_store(dict, MP_ROM_QSTR(MP_QSTR_media_src), MP_OBJ_TO_PTR(mp_obj_new_int(state.media_src)));

    return self->state;
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_player_state_obj, audio_player_state);


static mp_obj_t audio_player_pos(mp_obj_t self_in) {
    audio_player_obj_t *self = self_in;
    int pos = -1;
    int err = esp_audio_pos_get(self->player, &pos);
    if (err == ESP_ERR_AUDIO_NO_ERROR) {
        return mp_obj_new_int(pos);
    } else {
        return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_player_pos_obj, audio_player_pos);


static mp_obj_t audio_player_time(mp_obj_t self_in) {
    audio_player_obj_t *self = self_in;
    int time = 0;
    int err = esp_audio_time_get(self->player, &time);
    if (err == ESP_ERR_AUDIO_NO_ERROR) {
        return mp_obj_new_int(time);
    } else {
        return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_player_time_obj, audio_player_time);


static const mp_rom_map_elem_t player_locals_dict_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_info),      MP_ROM_PTR(&audio_player_info_obj)      },
    { MP_ROM_QSTR(MP_QSTR_play),      MP_ROM_PTR(&audio_player_play_obj)      },
    { MP_ROM_QSTR(MP_QSTR_play_raw),  MP_ROM_PTR(&audio_player_play_raw_obj)  },
    { MP_ROM_QSTR(MP_QSTR_play_tone), MP_ROM_PTR(&audio_player_play_tone_obj) },
    { MP_ROM_QSTR(MP_QSTR_stop),      MP_ROM_PTR(&audio_player_stop_obj)      },
    { MP_ROM_QSTR(MP_QSTR_pause),     MP_ROM_PTR(&audio_player_pause_obj)     },
    { MP_ROM_QSTR(MP_QSTR_resume),    MP_ROM_PTR(&audio_player_resume_obj)    },
    { MP_ROM_QSTR(MP_QSTR_vol),       MP_ROM_PTR(&audio_player_vol_obj)       },
    { MP_ROM_QSTR(MP_QSTR_get_vol),   MP_ROM_PTR(&audio_player_get_vol_obj)   },
    { MP_ROM_QSTR(MP_QSTR_set_vol),   MP_ROM_PTR(&audio_player_set_vol_obj)   },
    { MP_ROM_QSTR(MP_QSTR_get_state), MP_ROM_PTR(&audio_player_state_obj)     },
    { MP_ROM_QSTR(MP_QSTR_pos),       MP_ROM_PTR(&audio_player_pos_obj)       },
    { MP_ROM_QSTR(MP_QSTR_time),      MP_ROM_PTR(&audio_player_time_obj)      },

    // esp_audio_status_t
    { MP_ROM_QSTR(MP_QSTR_STATUS_UNKNOWN),  MP_ROM_INT(AUDIO_STATUS_UNKNOWN)  },
    { MP_ROM_QSTR(MP_QSTR_STATUS_RUNNING),  MP_ROM_INT(AUDIO_STATUS_RUNNING)  },
    { MP_ROM_QSTR(MP_QSTR_STATUS_PAUSED),   MP_ROM_INT(AUDIO_STATUS_PAUSED)   },
    { MP_ROM_QSTR(MP_QSTR_STATUS_STOPPED),  MP_ROM_INT(AUDIO_STATUS_STOPPED)  },
    { MP_ROM_QSTR(MP_QSTR_STATUS_FINISHED), MP_ROM_INT(AUDIO_STATUS_FINISHED) },
    { MP_ROM_QSTR(MP_QSTR_STATUS_ERROR),    MP_ROM_INT(AUDIO_STATUS_ERROR)    },

    // audio_termination_type
    { MP_ROM_QSTR(MP_QSTR_TERMINATION_NOW),  MP_ROM_INT(TERMINATION_TYPE_NOW)  },
    { MP_ROM_QSTR(MP_QSTR_TERMINATION_DONE), MP_ROM_INT(TERMINATION_TYPE_DONE) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(player_locals_dict, player_locals_dict_table);


MP_DEFINE_CONST_OBJ_TYPE(
    audio_player_type,
    MP_QSTR_audio_player,
    MP_TYPE_FLAG_NONE,
    make_new, audio_player_make_new,
    locals_dict, &player_locals_dict
    );
