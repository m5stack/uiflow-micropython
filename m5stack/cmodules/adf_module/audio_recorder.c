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

#include "esp_timer.h"
#include "esp_log.h"
#include "freertos/event_groups.h"

#include "audio_pipeline.h"
#include "filter_resample.h"

#include "raw_stream.h"
#include "vfs_stream.h"
#include "i2s_stream.h"

#include "amrnb_encoder.h"
// #include "amrwb_encoder.h"
#include "wav_encoder.h"

#include "board_init.h"

#include "mpconfigboard.h"

// NOTE: Adding the amrwb encoder will increase the firmware size.
#define AUDIO_RECORDER_SUPPORT_AMRWB_ENCODER (0)

// format suffix
#define FILE_WAV_SUFFIX_TYPE   "wav"
#define FILE_AMR_SUFFIX_TYPE   "amr"
#define FILE_AMRWB_SUFFIX_TYPE "Wamr"

typedef enum format_t {
    UNKNOW,
    PCM,
    AMR,
    AMRWB,
    WAV,
    MP3,
} format_t;

typedef struct _audio_recorder_obj_t {
    mp_obj_base_t base;

    audio_pipeline_handle_t pipeline;
    audio_element_handle_t i2s_stream;
    audio_element_handle_t filter;
    audio_element_handle_t encoder;
    audio_element_handle_t out_stream;

    mp_obj_t end_cb;

    // pcm
    int sample;
    int bits;
    int channels;
    struct {
        void *buf;
        size_t len;
    } pcm_buf;
    TaskHandle_t async_record_task_handle;
    EventGroupHandle_t xRecordPCMEventGroup;

    bool is_record_file;

    int64_t record_us;
    int64_t start_us;
    bool is_pause;
    EventGroupHandle_t xEndtimeEventGroup;
} audio_recorder_obj_t;


extern const mp_obj_type_t audio_recorder_type;

static mp_obj_t audio_recorder_stop_helper(audio_recorder_obj_t *self);


#define EVENT_BIT_RUN (1UL << 0) // 事件位，用于控制运行
#define EVENT_BIT_STOP (1UL << 1) // 事件位，用于停止任务

static void audio_recorder_endtime_task(void *arg) {
    audio_recorder_obj_t *self = (audio_recorder_obj_t *)arg;

    BaseType_t xStatus;
    EventBits_t uxBits;
    while (1) {
        uxBits = xEventGroupWaitBits(
            self->xEndtimeEventGroup, // 事件组
            EVENT_BIT_RUN,     // 等待的事件位
            pdFALSE,           // 不清除事件位
            pdTRUE,            // 等待所有指定的事件位
            portMAX_DELAY      // 无限期等待
            );

        if ((uxBits & EVENT_BIT_RUN) != 0) {
            int64_t ticks = esp_timer_get_time();
            if (ticks - self->start_us >= self->record_us) {
                audio_recorder_stop_helper(self);
                if (self->end_cb != mp_const_none) {
                    mp_sched_schedule(self->end_cb, self);
                }
                xEventGroupClearBits(self->xEndtimeEventGroup, EVENT_BIT_RUN);
            }
        }
    }

    vTaskDelete(NULL);
}


static mp_obj_t audio_recorder_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum { ARG_sample, ARG_bits, ARG_stereo, };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_sample,   MP_ARG_INT,  { .u_int = 8000 }   },
        { MP_QSTR_bits,     MP_ARG_INT,  { .u_int = 16 }     },
        { MP_QSTR_stereo, MP_ARG_BOOL, { .u_bool = false } },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    audio_recorder_obj_t *self = mp_obj_malloc(audio_recorder_obj_t, &audio_recorder_type);
    self->end_cb = mp_const_none;

    self->sample = args[ARG_sample].u_int;
    self->bits = args[ARG_bits].u_int;
    self->channels = args[ARG_stereo].u_bool ? 2 : 1;
    self->async_record_task_handle = NULL;

    self->xRecordPCMEventGroup = xEventGroupCreate();
    self->xEndtimeEventGroup = xEventGroupCreate();
    BaseType_t createStatus = xTaskCreatePinnedToCore(
        audio_recorder_endtime_task,
        "audio_recorder_endtime_task",
        4 * 1024,
        self,
        8,
        NULL,
        0
        );
    if (createStatus != pdPASS) {
        ESP_LOGI("*", "audio_recorder_endtime_task create task fail");
    }

    return MP_OBJ_FROM_PTR(self);
}


static audio_element_handle_t audio_recorder_create_filter(int encoder_type, int sample, int bits, int channels) {
    rsp_filter_cfg_t rsp_cfg = DEFAULT_RESAMPLE_FILTER_CONFIG();
    rsp_cfg.src_rate = 48000;
    rsp_cfg.src_ch = 2;
    rsp_cfg.task_core = 1;

    rsp_cfg.dest_rate = sample;
    rsp_cfg.dest_bits = bits;
    rsp_cfg.dest_ch = channels;

    switch (encoder_type) {
        case AMR: {
            rsp_cfg.dest_ch = 1;
            #if defined(AUDIO_RECORDER_DOWN_CH)
            rsp_cfg.complexity = 0;
            rsp_cfg.down_ch_idx = AUDIO_RECORDER_DOWN_CH;
            #endif
            break;
        }

        default:
            break;
    }
    return rsp_filter_init(&rsp_cfg);
}


static audio_element_handle_t audio_recorder_create_encoder(int encoder_type) {
    audio_element_handle_t encoder = NULL;

    switch (encoder_type) {
        #if AUDIO_RECORDER_SUPPORT_AMRWB_ENCODER
        case AMRWB: {
            amrwb_encoder_cfg_t amrwb_enc_cfg = DEFAULT_AMRWB_ENCODER_CONFIG();
            amrwb_enc_cfg.task_core = 1;
            encoder = amrwb_encoder_init(&amrwb_enc_cfg);
            break;
        }
        #endif

        case AMR: {
            amrnb_encoder_cfg_t amr_enc_cfg = DEFAULT_AMRNB_ENCODER_CONFIG();
            amr_enc_cfg.task_core = 1;
            encoder = amrnb_encoder_init(&amr_enc_cfg);
            break;
        }
        case WAV: {
            wav_encoder_cfg_t wav_cfg = DEFAULT_WAV_ENCODER_CONFIG();
            wav_cfg.task_core = 1;
            encoder = wav_encoder_init(&wav_cfg);
            break;
        }
        default:
            break;
    }

    return encoder;
}


static audio_element_handle_t audio_recorder_create_outstream(const char *uri) {
    audio_element_handle_t out_stream = NULL;
    if (strstr(uri, "/flash/") != NULL) {
        vfs_stream_cfg_t vfs_cfg = VFS_STREAM_CFG_DEFAULT();
        vfs_cfg.type = AUDIO_STREAM_WRITER;
        vfs_cfg.task_core = 1;
        out_stream = vfs_stream_init(&vfs_cfg);
    } else if (strstr(uri, "/spiffs/") != NULL) {
        // TODO: spiffs
    } else {
        raw_stream_cfg_t raw_cfg = RAW_STREAM_CFG_DEFAULT();
        raw_cfg.type = AUDIO_STREAM_WRITER;
        out_stream = raw_stream_init(&raw_cfg);
    }
    audio_element_set_uri(out_stream, uri);

    return out_stream;
}


static format_t get_type(const char *str) {
    char *relt = strrchr(str, '.');
    if (relt != NULL) {
        relt++;
        if (strncasecmp(relt, FILE_WAV_SUFFIX_TYPE, 3) == 0) {
            return WAV;
        } else if (strncasecmp(relt, FILE_AMR_SUFFIX_TYPE, 3) == 0) {
            return AMR;
        } else if (strncasecmp(relt, FILE_AMRWB_SUFFIX_TYPE, 4) == 0) {
            return AMRWB;
        } else {
            return UNKNOW;
        }
    } else {
        return UNKNOW;
    }
}


// from esp-adf/components/audio_stream/i2s_stream.c
typedef struct i2s_stream {
    audio_stream_type_t type;
    i2s_stream_cfg_t config;
    bool is_open;
    bool use_alc;
    void *volume_handle;
    int volume;
    bool uninstall_drv;
    int data_bit_width;
} i2s_stream_t;


static int _i2s_read(audio_element_handle_t self, char *buffer, int len, TickType_t ticks_to_wait, void *context) {
    audio_recorder_obj_t *recorder = (audio_recorder_obj_t *)context;
    while (recorder->is_pause) {
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }

    i2s_stream_t *i2s = (i2s_stream_t *)audio_element_getdata(self);
    size_t bytes_read = 0;
    i2s_read(i2s->config.i2s_port, buffer, len, &bytes_read, ticks_to_wait);
    audio_element_info_t info;
    audio_element_getinfo(self, &info);
    if (bytes_read > 0) {
        #ifdef CONFIG_IDF_TARGET_ESP32
        if (info.channels == 1) {
            i2s_mono_fix(info.bits, (uint8_t *)buffer, bytes_read);
        }
        #endif
    }
    return bytes_read;
}


static void audio_recorder_create(audio_recorder_obj_t *self, const char *uri, int format, int sample, int bits, int channels) {
    // init audio board
    board_codec_init();

    if (format == UNKNOW) {
        format = get_type(uri);
    }

    // pipeline
    audio_pipeline_cfg_t pipeline_cfg = DEFAULT_AUDIO_PIPELINE_CONFIG();
    self->pipeline = audio_pipeline_init(&pipeline_cfg);
    // I2S
    i2s_stream_cfg_t i2s_cfg = BOARD_I2S_STREAM_CFG_DEFAULT();
    i2s_cfg.i2s_config.sample_rate = 48000;
    i2s_cfg.i2s_config.bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT;
    i2s_cfg.type = AUDIO_STREAM_READER;
    i2s_cfg.task_core = 1;
    i2s_cfg.uninstall_drv = false;
    self->i2s_stream = i2s_stream_init(&i2s_cfg);
    audio_element_set_read_cb(self->i2s_stream, _i2s_read, self);
    // filter
    self->filter = audio_recorder_create_filter(format, sample, bits, channels);
    // encoder
    self->encoder = audio_recorder_create_encoder(format);
    // out stream
    self->out_stream = audio_recorder_create_outstream(uri);
    // register to pipeline
    audio_pipeline_register(self->pipeline, self->i2s_stream, "i2s");
    if (self->filter) {
        audio_pipeline_register(self->pipeline, self->filter, "filter");
    }
    if (self->encoder) {
        audio_pipeline_register(self->pipeline, self->encoder, "encoder");
    }
    audio_pipeline_register(self->pipeline, self->out_stream, "out");
    if (format == WAV) {
        audio_element_info_t out_stream_info;
        audio_element_getinfo(self->out_stream, &out_stream_info);
        out_stream_info.sample_rates = sample;
        out_stream_info.bits = bits;
        out_stream_info.channels = channels;
        audio_element_setinfo(self->out_stream, &out_stream_info);
    }
    // link
    if (self->filter && self->encoder) {
        const char *link_tag[4] = {"i2s", "filter", "encoder", "out"};
        audio_pipeline_link(self->pipeline, &link_tag[0], 4);
    } else if (self->filter) {
        const char *link_tag[3] = {"i2s", "filter", "out"};
        audio_pipeline_link(self->pipeline, &link_tag[0], 3);
    } else if (self->encoder) {
        const char *link_tag[3] = {"i2s", "encoder", "out"};
        audio_pipeline_link(self->pipeline, &link_tag[0], 3);
    } else {
        const char *link_tag[2] = {"i2s", "out"};
        audio_pipeline_link(self->pipeline, &link_tag[0], 2);
    }
}


static mp_obj_t audio_recorder_record(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_uri, ARG_time, ARG_sync };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_uri,    MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = mp_const_none } },
        { MP_QSTR_time,   MP_ARG_REQUIRED | MP_ARG_INT, { .u_int = 0 }             },
        { MP_QSTR_sync,   MP_ARG_BOOL,                  { .u_bool = true }         },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    audio_recorder_obj_t *self = args_in[0];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // stop previous recording
    if (self->pipeline != NULL) {
        audio_recorder_stop_helper(self);
    }

    audio_recorder_create(
        self,
        mp_obj_str_get_str(args[ARG_uri].u_obj),
        UNKNOW,
        self->sample,
        self->bits,
        self->channels
        );
    if (audio_pipeline_run(self->pipeline) == ESP_OK) {
        self->is_record_file = true;
        if (args[ARG_sync].u_bool == true) {
            vTaskDelay(args[ARG_time].u_int * 1000 / portTICK_PERIOD_MS);
            audio_recorder_stop_helper(self);
        } else {
            if (args[ARG_time].u_int > 0) {
                self->record_us = args[ARG_time].u_int * 1000000;
                self->start_us = esp_timer_get_time();
                self->is_pause = false;
                xEventGroupSetBits(self->xEndtimeEventGroup, EVENT_BIT_RUN);
            }
        }
        return mp_obj_new_bool(true);
    } else {
        return mp_obj_new_bool(false);
    }
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_recorder_record_obj, 2, audio_recorder_record);


static void async_record_task(void *arg) {
    audio_recorder_obj_t *self = (audio_recorder_obj_t *)arg;

    BaseType_t xStatus;
    EventBits_t uxBits;
    int index = 0;
    bool is_terminate = false;
    while (index < (self->pcm_buf.len - 1)) {
        uxBits = xEventGroupWaitBits(
            self->xRecordPCMEventGroup, // 事件组
            EVENT_BIT_RUN,     // 等待的事件位
            pdFALSE,           // 不清除事件位
            pdTRUE,            // 等待所有指定的事件位
            portMAX_DELAY      // 无限期等待
            );

        if ((uxBits & EVENT_BIT_RUN) != 0) {
            if (self->is_pause) {
                vTaskDelay(100 / portTICK_PERIOD_MS);
                continue;
            } else {
                int read_size = raw_stream_read(self->out_stream, &((char *)self->pcm_buf.buf)[index], self->pcm_buf.len);
                index += read_size;
            }
        }

        if ((uxBits & EVENT_BIT_STOP) != 0) {
            is_terminate = true;
            break;
        }
    }
    xEventGroupClearBits(self->xRecordPCMEventGroup, EVENT_BIT_RUN);
    xEventGroupClearBits(self->xRecordPCMEventGroup, EVENT_BIT_STOP);
    if (is_terminate == false) {
        audio_recorder_stop_helper(self);
    }

    vTaskDelay(1000 / portTICK_PERIOD_MS);

    self->async_record_task_handle = NULL;
    vTaskDelete(NULL);
}


static mp_obj_t audio_recorder_record_into(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_buf, ARG_sync };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_buf,  MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = mp_const_none } },
        { MP_QSTR_sync, MP_ARG_BOOL,                  { .u_bool = true }         },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    audio_recorder_obj_t *self = args_in[0];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // stop previous recording
    if (self->pipeline != NULL) {
        audio_recorder_stop_helper(self);
    }

    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[ARG_buf].u_obj, &bufinfo, MP_BUFFER_WRITE);

    audio_recorder_create(
        self,
        "",
        UNKNOW,
        self->sample,
        self->bits,
        self->channels
        );
    if (audio_pipeline_run(self->pipeline) == ESP_OK) {
        self->is_record_file = false;
        if (args[ARG_sync].u_bool == true) {
            int index = 0;
            while (index < (bufinfo.len - 1)) {
                int read_size = raw_stream_read(self->out_stream, &((char *)bufinfo.buf)[index], bufinfo.len);
                index += read_size;
            }
            audio_recorder_stop_helper(self);
        } else {
            if (bufinfo.len > 0) {
                self->pcm_buf.buf = bufinfo.buf;
                self->pcm_buf.len = bufinfo.len;
                BaseType_t createStatus = xTaskCreatePinnedToCore(
                    async_record_task,
                    "async_record_task",
                    4 * 1024,
                    self,
                    5,
                    &self->async_record_task_handle,
                    0
                    );
                if (createStatus != pdPASS) {
                    ESP_LOGI("*", "audio_play_tone_bg create task fail");
                    self->async_record_task_handle = NULL;
                }
                xEventGroupSetBits(self->xRecordPCMEventGroup, EVENT_BIT_RUN);
            }
        }
        return mp_obj_new_bool(true);
    } else {
        return mp_obj_new_bool(false);
    }
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_recorder_record_into_obj, 2, audio_recorder_record_into);



static mp_obj_t audio_recorder_stop_helper(audio_recorder_obj_t *self) {
    if (self->pipeline != NULL) {
        self->is_pause = false;
        if (self->is_record_file == false) {
            xEventGroupSetBits(self->xRecordPCMEventGroup, EVENT_BIT_STOP);
        }
        audio_element_set_ringbuf_done(self->i2s_stream);
        while (audio_element_get_state(self->i2s_stream) != AEL_STATE_FINISHED) {
            vTaskDelay(100 / portTICK_PERIOD_MS);
        }
        audio_pipeline_stop(self->pipeline);
        audio_pipeline_wait_for_stop(self->pipeline);
        audio_pipeline_deinit(self->pipeline);
    } else {
        return mp_obj_new_bool(false);
    }

    self->i2s_stream = NULL;
    self->filter = NULL;
    self->encoder = NULL;
    self->out_stream = NULL;
    self->pipeline = NULL;

    return mp_obj_new_bool(true);
}


static mp_obj_t audio_recorder_pause(mp_obj_t self_in) {
    audio_recorder_obj_t *self = self_in;

    if (self->pipeline != NULL) {
        self->record_us = self->record_us - (esp_timer_get_time() - self->start_us);
        self->is_pause = true;
        if (self->is_record_file) {
            xEventGroupClearBits(self->xEndtimeEventGroup, EVENT_BIT_RUN);
        } else {
            xEventGroupClearBits(self->xRecordPCMEventGroup, EVENT_BIT_RUN);
        }
    } else {
        return mp_obj_new_bool(false);
    }

    return mp_obj_new_bool(true);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_recorder_pause_obj, audio_recorder_pause);


static mp_obj_t audio_recorder_resume(mp_obj_t self_in) {
    audio_recorder_obj_t *self = self_in;

    if (self->pipeline != NULL) {
        self->start_us = esp_timer_get_time();
        self->is_pause = false;
        if (self->is_record_file) {
            xEventGroupSetBits(self->xEndtimeEventGroup, EVENT_BIT_RUN);
        } else {
            xEventGroupSetBits(self->xRecordPCMEventGroup, EVENT_BIT_RUN);
        }
    } else {
        return mp_obj_new_bool(false);
    }

    return mp_obj_new_bool(true);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_recorder_resume_obj, audio_recorder_resume);


static mp_obj_t audio_recorder_stop(mp_obj_t self_in) {
    audio_recorder_obj_t *self = self_in;

    return audio_recorder_stop_helper(self);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_recorder_stop_obj, audio_recorder_stop);


static mp_obj_t audio_recorder_rms(mp_obj_t self_in) {
    audio_recorder_obj_t *self = self_in;

    audio_recorder_stop_helper(self);

    audio_recorder_create(
        self,
        "",
        UNKNOW,
        8000,
        16,
        2
        );

    #define RAW_SAMPLE_DATA_SIZE (1024)// RAW_STREAM_RINGBUFFER_SIZE

    if (audio_pipeline_run(self->pipeline) == ESP_OK) {
        int index = 0;
        char *buf = m_malloc_with_finaliser(RAW_SAMPLE_DATA_SIZE);
        memset(buf, 0, RAW_SAMPLE_DATA_SIZE);
        while (index < (RAW_SAMPLE_DATA_SIZE - 1)) {
            int read_size = raw_stream_read(self->out_stream, &buf[index], RAW_SAMPLE_DATA_SIZE);
            index += read_size;
        }
        audio_recorder_stop_helper(self);

        int16_t *p_buf = (int16_t *)buf;
        float sum = 0.0f;
        for (uint16_t i = 0; i < RAW_SAMPLE_DATA_SIZE / 2; i++) {
            sum += p_buf[i] * p_buf[i];
        }
        m_free(buf);

        float k_max_squared_level = 32767 * 32767;
        sum = sum / (RAW_SAMPLE_DATA_SIZE / 2);
        float rms = sum / k_max_squared_level;
        float rms_db = 10 * log10(rms);

        return mp_obj_new_float(rms_db);
    } else {
        return mp_obj_new_float(-96);
    }

    return mp_obj_new_float(-96);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_recorder_rms_obj, audio_recorder_rms);


static mp_obj_t audio_recorder_volume(mp_obj_t self_in) {
    audio_recorder_obj_t *self = self_in;

    audio_recorder_stop_helper(self);

    audio_recorder_create(
        self,
        "",
        UNKNOW,
        8000,
        16,
        2
        );

    #define RAW_SAMPLE_DATA_SIZE (1024)// RAW_STREAM_RINGBUFFER_SIZE

    if (audio_pipeline_run(self->pipeline) == ESP_OK) {
        int index = 0;
        char *buf = m_malloc_with_finaliser(RAW_SAMPLE_DATA_SIZE);
        memset(buf, 0, RAW_SAMPLE_DATA_SIZE);
        while (index < (RAW_SAMPLE_DATA_SIZE - 1)) {
            int read_size = raw_stream_read(self->out_stream, &buf[index], RAW_SAMPLE_DATA_SIZE);
            index += read_size;
        }
        audio_recorder_stop_helper(self);

        int16_t *p_buf = (int16_t *)buf;
        float sum = 0.0f;
        for (uint16_t i = 0; i < RAW_SAMPLE_DATA_SIZE / 2; i++) {
            sum += p_buf[i] * p_buf[i];
        }
        m_free(buf);

        float k_max_squared_level = 32767 * 32767;
        sum = sum / (RAW_SAMPLE_DATA_SIZE / 2);
        float rms = sum / k_max_squared_level;
        float rms_db = 10 * log10(rms);

        return mp_obj_new_int((int)((rms_db + 96.0f) / 96.0f * 100.0f));
    } else {
        return mp_obj_new_int(0);
    }

    return mp_obj_new_int(0);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_recorder_volume_obj, audio_recorder_volume);


static mp_obj_t audio_recorder_is_running(mp_obj_t self_in) {
    audio_recorder_obj_t *self = self_in;
    return mp_obj_new_bool(self->pipeline != NULL);
}
static MP_DEFINE_CONST_FUN_OBJ_1(audio_recorder_is_running_obj, audio_recorder_is_running);


static mp_obj_t audio_recorder_config(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_sample, ARG_bits, ARG_stereo, };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_sample, MP_ARG_INT,  { .u_int = 8000 }   },
        { MP_QSTR_bits,   MP_ARG_INT,  { .u_int = 16 }     },
        { MP_QSTR_stereo, MP_ARG_BOOL, { .u_bool = false } },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    audio_recorder_obj_t *self = args_in[0];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    self->sample = args[ARG_sample].u_int;
    self->bits = args[ARG_bits].u_int;
    self->channels = args[ARG_stereo].u_bool ? 2 : 1;

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_recorder_config_obj, 0, audio_recorder_config);


static mp_obj_t audio_recorder_create_pcm_buf(size_t n_args, const mp_obj_t *args_in, mp_map_t *kw_args) {
    enum { ARG_time };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_time, MP_ARG_REQUIRED | MP_ARG_INT, { .u_int = 5 } },
        /* *FORMAT-ON* */
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    audio_recorder_obj_t *self = args_in[0];
    mp_arg_parse_all(n_args - 1, args_in + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    int time = args[ARG_time].u_int;
    int sample = self->sample;
    int bits = self->bits;
    int channels = self->channels;

    size_t len = time * sample * (bits / 8) * channels;
    ESP_LOGI("*", "len: %d", len);

    uint8_t *ptr = m_new(uint8_t, len);
    return mp_obj_new_bytearray_by_ref(len, ptr);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(audio_recorder_create_pcm_buf_obj, 1, audio_recorder_create_pcm_buf);


static const mp_rom_map_elem_t recorder_locals_dict_table[] = {
    /* *FORMAT-OFF* */
    // methods
    { MP_ROM_QSTR(MP_QSTR_record),         MP_ROM_PTR(&audio_recorder_record_obj)         },
    { MP_ROM_QSTR(MP_QSTR_record_into),    MP_ROM_PTR(&audio_recorder_record_into_obj)    },
    { MP_ROM_QSTR(MP_QSTR_pause),          MP_ROM_PTR(&audio_recorder_pause_obj)          },
    { MP_ROM_QSTR(MP_QSTR_resume),         MP_ROM_PTR(&audio_recorder_resume_obj)         },
    { MP_ROM_QSTR(MP_QSTR_stop),           MP_ROM_PTR(&audio_recorder_stop_obj)           },
    { MP_ROM_QSTR(MP_QSTR_rms),            MP_ROM_PTR(&audio_recorder_rms_obj)            },
    { MP_ROM_QSTR(MP_QSTR_volume),         MP_ROM_PTR(&audio_recorder_volume_obj)         },
    { MP_ROM_QSTR(MP_QSTR_is_running),     MP_ROM_PTR(&audio_recorder_is_running_obj)     },
    { MP_ROM_QSTR(MP_QSTR_is_recording),   MP_ROM_PTR(&audio_recorder_is_running_obj)     },
    { MP_ROM_QSTR(MP_QSTR_config),         MP_ROM_PTR(&audio_recorder_config_obj)         },
    { MP_ROM_QSTR(MP_QSTR_create_pcm_buf), MP_ROM_PTR(&audio_recorder_create_pcm_buf_obj) },

    // constants
    { MP_ROM_QSTR(MP_QSTR_PCM),        MP_ROM_INT(PCM) },
    { MP_ROM_QSTR(MP_QSTR_AMR),        MP_ROM_INT(AMR) },
    { MP_ROM_QSTR(MP_QSTR_WAV),        MP_ROM_INT(WAV) },
    { MP_ROM_QSTR(MP_QSTR_MP3),        MP_ROM_INT(MP3) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(recorder_locals_dict, recorder_locals_dict_table);


MP_DEFINE_CONST_OBJ_TYPE(
    audio_recorder_type,
    MP_QSTR_audio_recorder,
    MP_TYPE_FLAG_NONE,
    make_new, audio_recorder_make_new,
    locals_dict, &recorder_locals_dict
    );
