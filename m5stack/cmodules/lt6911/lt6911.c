/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdbool.h>
#include <inttypes.h>
#include <stdint.h>

#include "esp_cache.h"
#include "esp_private/esp_cache_private.h"
#include "esp_cam_ctlr.h"
#include "esp_cam_ctlr_csi.h"
#include "esp_err.h"
#include "esp_heap_caps.h"
#include "esp_ldo_regulator.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "driver/i2c_master.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "driver/isp.h"
#include "img_converters.h"
#include "soc/mipi_csi_host_struct.h"
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
#define LT6911_HS_FREQ_SEL        0x18
#define LT6911_CSI_STARTUP_MS      200
#define LT6911_CSI_RECOVERY_MS     500
#define LT6911_I2C_ADDRESS        0x2B
#define LT6911_I2C_PORT           I2C_NUM_1
#define LT6911_I2C_FREQ_HZ        (100 * 1000)
#define LT6911_I2C_TIMEOUT_MS     100
#define LT6911_CSI_PHY_LDO_CHAN     3
#define LT6911_CSI_PHY_LDO_MV    2500

static esp_cam_ctlr_handle_t s_camera = NULL;
static isp_proc_handle_t s_isp = NULL;
static QueueHandle_t s_finished_frames = NULL;
static i2c_master_dev_handle_t s_lt6911_i2c = NULL;
static esp_ldo_channel_handle_t s_csi_phy_ldo = NULL;
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
    if (s_csi_phy_ldo) {
        (void)esp_ldo_release_channel(s_csi_phy_ldo);
        s_csi_phy_ldo = NULL;
    }
    if (s_finished_frames) {
        vQueueDelete(s_finished_frames);
        s_finished_frames = NULL;
    }
    if (s_lt6911_i2c) {
        (void)i2c_master_bus_rm_device(s_lt6911_i2c);
        s_lt6911_i2c = NULL;
    }
    for (size_t i = 0; i < LT6911_BUFFER_COUNT; ++i) {
        heap_caps_free(s_frame_buffers[i]);
        s_frame_buffers[i] = NULL;
    }
    s_next_buffer = 0;
}

static esp_err_t lt6911_i2c_init(void) {
    if (s_lt6911_i2c) {
        return ESP_OK;
    }

    i2c_master_bus_handle_t bus = NULL;
    esp_err_t err = i2c_master_get_bus_handle(LT6911_I2C_PORT, &bus);
    if (err != ESP_OK) {
        return err;
    }

    const i2c_device_config_t config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = LT6911_I2C_ADDRESS,
        .scl_speed_hz = LT6911_I2C_FREQ_HZ,
    };
    return i2c_master_bus_add_device(bus, &config, &s_lt6911_i2c);
}

static esp_err_t lt6911_enable_csi_phy_power(void) {
    if (s_csi_phy_ldo) {
        return ESP_OK;
    }

    const esp_ldo_channel_config_t config = {
        .chan_id = LT6911_CSI_PHY_LDO_CHAN,
        .voltage_mv = LT6911_CSI_PHY_LDO_MV,
    };
    return esp_ldo_acquire_channel(&config, &s_csi_phy_ldo);
}

static esp_err_t lt6911_select_bank(uint8_t bank) {
    const uint8_t command[] = {0xFF, bank};
    return i2c_master_transmit(s_lt6911_i2c, command, sizeof(command), LT6911_I2C_TIMEOUT_MS);
}

static esp_err_t lt6911_read_register(uint8_t reg, uint8_t *value) {
    esp_err_t err = lt6911_select_bank(0xE0);
    if (err != ESP_OK) {
        return err;
    }
    return i2c_master_transmit_receive(s_lt6911_i2c, &reg, 1, value, 1, LT6911_I2C_TIMEOUT_MS);
}

static esp_err_t lt6911_write_register(uint8_t reg, uint8_t value) {
    const uint8_t command[] = {reg, value};
    esp_err_t err = lt6911_select_bank(0xE0);
    if (err != ESP_OK) {
        return err;
    }
    return i2c_master_transmit(s_lt6911_i2c, command, sizeof(command), LT6911_I2C_TIMEOUT_MS);
}

static void lt6911_report_mipi_stream(void) {
    esp_err_t err = lt6911_i2c_init();
    if (err != ESP_OK) {
        mp_printf(&mp_plat_print, "lt6911: cannot access bridge I2C: %s\n", esp_err_to_name(err));
        return;
    }

    uint8_t lanes = 0;
    uint8_t tx = 0;
    uint8_t format = 0;
    uint8_t video_ready = 0;
    err = lt6911_read_register(0x95, &lanes);
    if (err == ESP_OK) {
        err = lt6911_read_register(0xB0, &tx);
    }
    if (err == ESP_OK) {
        err = lt6911_read_register(0x96, &format);
    }
    if (err == ESP_OK) {
        err = lt6911_read_register(0x84, &video_ready);
    }
    if (err != ESP_OK) {
        mp_printf(&mp_plat_print, "lt6911: bridge I2C read failed: %s\n", esp_err_to_name(err));
        return;
    }

    mp_printf(&mp_plat_print,
        "lt6911: bridge tx=0x%02x lanes=%u format=0x%02x video=0x%02x\n",
        tx, lanes & 0x0F, format, video_ready);
}

static esp_err_t lt6911_enable_mipi_stream(void) {
    esp_err_t err = lt6911_i2c_init();
    if (err != ESP_OK) {
        return err;
    }

    uint8_t tx = 0;
    err = lt6911_read_register(0xB0, &tx);
    if (err != ESP_OK || tx == 0x01) {
        return err;
    }

    err = lt6911_write_register(0xB0, 0x01);
    if (err != ESP_OK) {
        return err;
    }
    vTaskDelay(pdMS_TO_TICKS(200));
    err = lt6911_read_register(0xB0, &tx);
    return err == ESP_OK && tx == 0x01 ? ESP_OK : ESP_FAIL;
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

    esp_err_t err = lt6911_enable_mipi_stream();
    if (err != ESP_OK) {
        lt6911_deinit_internal();
        lt6911_raise_esp_error(err, "enable bridge MIPI TX");
    }

    err = lt6911_enable_csi_phy_power();
    if (err != ESP_OK) {
        lt6911_deinit_internal();
        lt6911_raise_esp_error(err, "power CSI PHY");
    }

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
        // Normalize the ECO2 DMA order in software before JPEG encoding; the
        // required component permutation is not a global byte swap.
        .byte_swap_en = false,
        .queue_items = 4,
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

    lt6911_report_mipi_stream();
    mp_printf(&mp_plat_print, "lt6911: ready for 1280x720 YUYV HDMI input\n");
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

static void lt6911_fix_eco2_yuv422_order(uint8_t *frame) {
    // This LT6911/ESP32-P4 ECO2 path produces Y1 V Y0 U, while esp32-camera's
    // JPEG path expects Y0 U Y1 V.
    for (size_t i = 0; i < LT6911_FRAME_BYTES; i += 4) {
        uint8_t y1 = frame[i];
        uint8_t v = frame[i + 1];
        frame[i] = frame[i + 2];
        frame[i + 1] = frame[i + 3];
        frame[i + 2] = y1;
        frame[i + 3] = v;
    }
}

static void lt6911_phy_write_register(uint8_t address, uint8_t value) {
    MIPI_CSI_HOST.phy_test_ctrl0.val = 0;
    MIPI_CSI_HOST.phy_test_ctrl1.val = (1U << 16) | address;
    MIPI_CSI_HOST.phy_test_ctrl0.val = 1U << 1;
    MIPI_CSI_HOST.phy_test_ctrl0.val = 0;
    MIPI_CSI_HOST.phy_test_ctrl1.val = value;
    MIPI_CSI_HOST.phy_test_ctrl0.val = 1U << 1;
    MIPI_CSI_HOST.phy_test_ctrl0.val = 0;
}

static void lt6911_reinit_csi_host(void) {
    MIPI_CSI_HOST.csi2_resetn.csi2_resetn = 0;
    MIPI_CSI_HOST.phy_shutdownz.phy_shutdownz = 0;
    MIPI_CSI_HOST.dphy_rstz.dphy_rstz = 0;
    esp_rom_delay_us(50);

    MIPI_CSI_HOST.phy_test_ctrl0.val = 1;
    esp_rom_delay_us(10);
    MIPI_CSI_HOST.phy_test_ctrl0.val = 0;
    lt6911_phy_write_register(0x44, LT6911_HS_FREQ_SEL << 1);

    MIPI_CSI_HOST.phy_shutdownz.phy_shutdownz = 1;
    esp_rom_delay_us(100);
    MIPI_CSI_HOST.dphy_rstz.dphy_rstz = 1;

    for (uint32_t ms = 0; ms < LT6911_CSI_RECOVERY_MS; ++ms) {
        if ((MIPI_CSI_HOST.phy_stopstate.val & 0x00010003U) == 0x00010003U) {
            break;
        }
        vTaskDelay(pdMS_TO_TICKS(1));
    }

    MIPI_CSI_HOST.csi2_resetn.csi2_resetn = 1;
    MIPI_CSI_HOST.n_lanes.n_lanes = 1;
    MIPI_CSI_HOST.vc_extension.vcx = 1;
    MIPI_CSI_HOST.scrambling.scramble_enable = 0;
    MIPI_CSI_BRIDGE.frame_cfg.has_hsync_e = 0;
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

    int startup_ms = args[ARG_timeout_ms].u_int < LT6911_CSI_STARTUP_MS ? args[ARG_timeout_ms].u_int
                                                                         : LT6911_CSI_STARTUP_MS;
    bool frame_ready = xQueueReceive(s_finished_frames, &completed_index, pdMS_TO_TICKS(startup_ms)) == pdTRUE;
    if (!frame_ready && args[ARG_timeout_ms].u_int > startup_ms) {
        mp_printf(&mp_plat_print,
            "lt6911: no completed frame after %d ms (host=0x%08" PRIx32 ", bridge=0x%08" PRIx32
            ", depth=%" PRIu32 ", phy_rx=0x%08" PRIx32 ", stop=0x%08" PRIx32 ")\n",
            startup_ms, MIPI_CSI_HOST.int_st_main.val, MIPI_CSI_BRIDGE.int_raw.val,
            MIPI_CSI_BRIDGE.buf_flow_ctl.csi_buf_depth, MIPI_CSI_HOST.phy_rx.val, MIPI_CSI_HOST.phy_stopstate.val);
        mp_printf(&mp_plat_print, "lt6911: reinitializing CSI host while bridge TX remains enabled\n");
        lt6911_reinit_csi_host();
        err = lt6911_write_register(0xB0, 0x01);
        if (err != ESP_OK) {
            (void)esp_cam_ctlr_stop(s_camera);
            s_capturing = false;
            lt6911_raise_esp_error(err, "restore bridge MIPI TX");
        }
        vTaskDelay(pdMS_TO_TICKS(LT6911_CSI_RECOVERY_MS));
    }

    if (!frame_ready) {
        int remaining_ms = args[ARG_timeout_ms].u_int - startup_ms;
        if (remaining_ms > 0) {
            frame_ready = xQueueReceive(s_finished_frames, &completed_index, pdMS_TO_TICKS(remaining_ms)) == pdTRUE;
        }
    }

    if (!frame_ready) {
        (void)esp_cam_ctlr_stop(s_camera);
        s_capturing = false;
        mp_printf(&mp_plat_print, "lt6911: capture timed out waiting for a CSI frame\n");
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
    lt6911_fix_eco2_yuv422_order(s_frame_buffers[completed_index]);

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
