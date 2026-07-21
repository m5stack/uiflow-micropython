/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdbool.h>
#include <stdint.h>

#include "esp_cache.h"
#include "esp_private/esp_cache_private.h"
#include "esp_cam_ctlr.h"
#include "esp_cam_ctlr_csi.h"
#include "esp_err.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "driver/isp.h"
#include "img_converters.h"
#include "soc/mipi_csi_bridge_struct.h"

#include "py/mperrno.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/stream.h"
#include "extmod/vfs.h"

#define LT6911_WIDTH              1280
#define LT6911_HEIGHT             720
#define LT6911_FRAME_BYTES        (LT6911_WIDTH * LT6911_HEIGHT * 2)
#define LT6911_BUFFER_COUNT       2
#define LT6911_LANE_BIT_RATE_MBPS 714

static const char *TAG = "lt6911";

static esp_cam_ctlr_handle_t s_camera = NULL;
static isp_proc_handle_t s_isp = NULL;
static QueueHandle_t s_finished_frames = NULL;
static uint8_t *s_frame_buffers[LT6911_BUFFER_COUNT] = {NULL};
static volatile uint8_t s_next_buffer = 0;
static bool s_capturing = false;

static void lt6911_raise_esp_error(esp_err_t err, const char *operation) {
    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("lt6911 %s: %s"), operation, esp_err_to_name(err));
}

static void lt6911_deinit_internal(void) {
    if (s_capturing && s_camera) {
        (void)esp_cam_ctlr_stop(s_camera);
        s_capturing = false;
    }
    if (s_camera) {
        (void)esp_cam_ctlr_disable(s_camera);
        (void)esp_cam_ctlr_del(s_camera);
        s_camera = NULL;
    }
    if (s_isp) {
        (void)esp_isp_del_processor(s_isp);
        s_isp = NULL;
    }
    if (s_finished_frames) {
        vQueueDelete(s_finished_frames);
        s_finished_frames = NULL;
    }
    for (size_t i = 0; i < LT6911_BUFFER_COUNT; ++i) {
        heap_caps_free(s_frame_buffers[i]);
        s_frame_buffers[i] = NULL;
    }
    s_next_buffer = 0;
}

static bool IRAM_ATTR lt6911_get_new_transaction(esp_cam_ctlr_handle_t handle, esp_cam_ctlr_trans_t *trans,
    void *user_data) {
    uint8_t index = s_next_buffer;
    s_next_buffer = (index + 1) % LT6911_BUFFER_COUNT;
    trans->buffer = s_frame_buffers[index];
    trans->buflen = LT6911_FRAME_BYTES;
    return false;
}

static bool IRAM_ATTR lt6911_frame_finished(esp_cam_ctlr_handle_t handle, esp_cam_ctlr_trans_t *trans, void *user_data) {
    uint8_t index = trans->buffer == s_frame_buffers[0] ? 0 : 1;
    BaseType_t task_woken = pdFALSE;
    xQueueOverwriteFromISR(s_finished_frames, &index, &task_woken);
    return task_woken == pdTRUE;
}

static mp_obj_t lt6911_init(void) {
    if (s_camera) {
        return mp_const_none;
    }

    esp_err_t err;
    size_t alignment = 0;
    err = esp_cache_get_alignment(MALLOC_CAP_SPIRAM | MALLOC_CAP_DMA, &alignment);
    if (err != ESP_OK) {
        lt6911_raise_esp_error(err, "get cache alignment");
    }

    for (size_t i = 0; i < LT6911_BUFFER_COUNT; ++i) {
        s_frame_buffers[i] = heap_caps_aligned_calloc(alignment, 1, LT6911_FRAME_BYTES,
            MALLOC_CAP_SPIRAM | MALLOC_CAP_DMA | MALLOC_CAP_8BIT);
        if (!s_frame_buffers[i]) {
            lt6911_deinit_internal();
            mp_raise_msg(&mp_type_MemoryError, MP_ERROR_TEXT("lt6911 frame buffer allocation failed"));
        }
        err = esp_cache_msync(s_frame_buffers[i], LT6911_FRAME_BYTES, ESP_CACHE_MSYNC_FLAG_DIR_C2M);
        if (err != ESP_OK) {
            lt6911_deinit_internal();
            lt6911_raise_esp_error(err, "prepare frame buffer");
        }
    }

    s_finished_frames = xQueueCreate(1, sizeof(uint8_t));
    if (!s_finished_frames) {
        lt6911_deinit_internal();
        mp_raise_msg(&mp_type_MemoryError, MP_ERROR_TEXT("lt6911 frame queue allocation failed"));
    }

    esp_cam_ctlr_csi_config_t csi_config = {
        .ctlr_id = 0,
        .h_res = LT6911_WIDTH,
        .v_res = LT6911_HEIGHT,
        .lane_bit_rate_mbps = LT6911_LANE_BIT_RATE_MBPS,
        .input_data_color_type = CAM_CTLR_COLOR_YUV422,
        .output_data_color_type = CAM_CTLR_COLOR_YUV422,
        .data_lane_num = 2,
        .byte_swap_en = false,
        .queue_items = 1,
        .bk_buffer_dis = true,
    };
    err = esp_cam_new_csi_ctlr(&csi_config, &s_camera);
    if (err != ESP_OK) {
        lt6911_deinit_internal();
        lt6911_raise_esp_error(err, "create CSI controller");
    }

    // LT6911D sends YUYV data without CSI line-start/line-end packets.
    MIPI_CSI_BRIDGE.frame_cfg.has_hsync_e = 0;

    esp_cam_ctlr_evt_cbs_t callbacks = {
        .on_get_new_trans = lt6911_get_new_transaction,
        .on_trans_finished = lt6911_frame_finished,
    };
    err = esp_cam_ctlr_register_event_callbacks(s_camera, &callbacks, NULL);
    if (err != ESP_OK) {
        lt6911_deinit_internal();
        lt6911_raise_esp_error(err, "register CSI callbacks");
    }
    err = esp_cam_ctlr_enable(s_camera);
    if (err != ESP_OK) {
        lt6911_deinit_internal();
        lt6911_raise_esp_error(err, "enable CSI controller");
    }

    esp_isp_processor_cfg_t isp_config = {
        .clk_hz = 80 * 1000 * 1000,
        .input_data_source = ISP_INPUT_DATA_SOURCE_CSI,
        .input_data_color_type = ISP_COLOR_YUV422,
        .output_data_color_type = ISP_COLOR_YUV422,
        .has_line_start_packet = false,
        .has_line_end_packet = false,
        .h_res = LT6911_WIDTH,
        .v_res = LT6911_HEIGHT,
        .flags.bypass_isp = true,
    };
    err = esp_isp_new_processor(&isp_config, &s_isp);
    if (err != ESP_OK) {
        lt6911_deinit_internal();
        lt6911_raise_esp_error(err, "create ISP bypass");
    }

    ESP_LOGI(TAG, "ready for 1280x720 YUYV HDMI input");
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_0(lt6911_init_obj, lt6911_init);

typedef struct {
    mp_obj_t file;
    size_t bytes_written;
    bool write_failed;
} lt6911_jpeg_writer_t;

static size_t lt6911_write_jpeg(void *arg, size_t index, const void *data, size_t len) {
    lt6911_jpeg_writer_t *writer = arg;
    int written = mp_stream_posix_write(writer->file, data, len);
    if (written != (int)len) {
        writer->write_failed = true;
        return 0;
    }
    writer->bytes_written += len;
    return len;
}

static void lt6911_yvyu_to_yuyv(uint8_t *frame) {
    // The LT6911 delivers Y0 V Y1 U while esp32-camera's JPEG path expects Y0 U Y1 V.
    for (size_t i = 0; i < LT6911_FRAME_BYTES; i += 4) {
        uint8_t u = frame[i + 3];
        frame[i + 3] = frame[i + 1];
        frame[i + 1] = u;
    }
}

static mp_obj_t lt6911_capture(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_path, ARG_quality, ARG_timeout_ms };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_path, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = MP_OBJ_NULL}},
        {MP_QSTR_quality, MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = 75}},
        {MP_QSTR_timeout_ms, MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = 1000}},
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (!s_camera || !s_isp) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("lt6911 is not initialized"));
    }
    if (!mp_obj_is_str(args[ARG_path].u_obj)) {
        mp_raise_TypeError(MP_ERROR_TEXT("path must be a string"));
    }
    if (args[ARG_quality].u_int < 1 || args[ARG_quality].u_int > 100) {
        mp_raise_ValueError(MP_ERROR_TEXT("quality must be from 1 to 100"));
    }
    if (args[ARG_timeout_ms].u_int < 1) {
        mp_raise_ValueError(MP_ERROR_TEXT("timeout_ms must be positive"));
    }
    if (s_capturing) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("lt6911 capture is already running"));
    }

    uint8_t completed_index;
    while (xQueueReceive(s_finished_frames, &completed_index, 0) == pdTRUE) {
    }

    esp_err_t err = esp_cam_ctlr_start(s_camera);
    if (err != ESP_OK) {
        lt6911_raise_esp_error(err, "start CSI controller");
    }
    s_capturing = true;

    TickType_t timeout = pdMS_TO_TICKS(args[ARG_timeout_ms].u_int);
    if (xQueueReceive(s_finished_frames, &completed_index, timeout) != pdTRUE) {
        (void)esp_cam_ctlr_stop(s_camera);
        s_capturing = false;
        mp_raise_OSError(MP_ETIMEDOUT);
    }

    err = esp_cam_ctlr_stop(s_camera);
    s_capturing = false;
    if (err != ESP_OK) {
        lt6911_raise_esp_error(err, "stop CSI controller");
    }
    err = esp_cache_msync(s_frame_buffers[completed_index], LT6911_FRAME_BYTES, ESP_CACHE_MSYNC_FLAG_DIR_M2C);
    if (err != ESP_OK) {
        lt6911_raise_esp_error(err, "synchronize captured frame");
    }
    lt6911_yvyu_to_yuyv(s_frame_buffers[completed_index]);

    mp_obj_t open_args[2] = {
        args[ARG_path].u_obj,
        mp_obj_new_str("wb", 2),
    };
    mp_obj_t file = mp_vfs_open(2, open_args, (mp_map_t *)&mp_const_empty_map);
    if (file == mp_const_none) {
        mp_raise_OSError(MP_EIO);
    }

    lt6911_jpeg_writer_t writer = {
        .file = file,
        .bytes_written = 0,
        .write_failed = false,
    };
    bool encoded = fmt2jpg_cb(s_frame_buffers[completed_index], LT6911_FRAME_BYTES, LT6911_WIDTH, LT6911_HEIGHT,
        PIXFORMAT_YUV422, args[ARG_quality].u_int, lt6911_write_jpeg, &writer);
    mp_stream_close(file);

    if (!encoded || writer.write_failed) {
        mp_raise_OSError(MP_EIO);
    }
    return mp_obj_new_int_from_uint(writer.bytes_written);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(lt6911_capture_obj, 1, lt6911_capture);

static mp_obj_t lt6911_deinit(void) {
    lt6911_deinit_internal();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_0(lt6911_deinit_obj, lt6911_deinit);

static const mp_rom_map_elem_t lt6911_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_lt6911)},
    {MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&lt6911_init_obj)},
    {MP_ROM_QSTR(MP_QSTR_capture), MP_ROM_PTR(&lt6911_capture_obj)},
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&lt6911_deinit_obj)},
};
static MP_DEFINE_CONST_DICT(lt6911_module_globals, lt6911_module_globals_table);

const mp_obj_module_t mp_module_lt6911 = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&lt6911_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_lt6911, mp_module_lt6911);
