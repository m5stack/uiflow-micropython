/*
 * Copyright [2021] Mauro Riva <info@lemariva.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <string.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/binary.h"
#include "mphalport.h"

#include "esp_system.h"
#include "esp_spi_flash.h"
#include "esp_camera.h"
#include "esp_log.h"

#define TAG "m5camera"

#define CORES3_CAMERA_POWER_DOWN_PIN -1
#define CORES3_CAMERA_RESET_PIN -1
#define CORES3_CAMERA_XCLK_PIN -1
#define CORES3_CAMERA_SDA_PIN 12
#define CORES3_CAMERA_SCL_PIN 11
#define CORES3_CAMERA_D7_PIN 47
#define CORES3_CAMERA_D6_PIN 48
#define CORES3_CAMERA_D5_PIN 16
#define CORES3_CAMERA_D4_PIN 15
#define CORES3_CAMERA_D3_PIN 42
#define CORES3_CAMERA_D2_PIN 41
#define CORES3_CAMERA_D1_PIN 40
#define CORES3_CAMERA_D0_PIN 39
#define CORES3_CAMERA_VSYNC_PIN 46
#define CORES3_CAMERA_HREF_PIN 38
#define CORES3_CAMERA_PCLK_PIN 45

static camera_config_t camera_config = {
    .pin_pwdn = CORES3_CAMERA_POWER_DOWN_PIN,
    .pin_reset = CORES3_CAMERA_RESET_PIN,
    .pin_xclk = CORES3_CAMERA_XCLK_PIN,
    .pin_sscb_sda = CORES3_CAMERA_SDA_PIN,
    .pin_sscb_scl = CORES3_CAMERA_SCL_PIN,
    .pin_d7 = CORES3_CAMERA_D7_PIN,
    .pin_d6 = CORES3_CAMERA_D6_PIN,
    .pin_d5 = CORES3_CAMERA_D5_PIN,
    .pin_d4 = CORES3_CAMERA_D4_PIN,
    .pin_d3 = CORES3_CAMERA_D3_PIN,
    .pin_d2 = CORES3_CAMERA_D2_PIN,
    .pin_d1 = CORES3_CAMERA_D1_PIN,
    .pin_d0 = CORES3_CAMERA_D0_PIN,
    .pin_vsync = CORES3_CAMERA_VSYNC_PIN,
    .pin_href = CORES3_CAMERA_HREF_PIN,
    .pin_pclk = CORES3_CAMERA_PCLK_PIN,

    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,

    .pixel_format = PIXFORMAT_RGB565,  // YUV422,RGB565
    .frame_size = FRAMESIZE_QVGA,  // Max is VGA
    .fb_count = 2,
    .fb_location = CAMERA_FB_IN_PSRAM,
    .grab_mode = CAMERA_GRAB_LATEST,
};

static enum {
    E_CAMERA_INIT,
    E_CAMERA_DEINIT
} status = E_CAMERA_DEINIT;

// STATIC camera_obj_t camera_obj;
STATIC bool camera_init_helper(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_pixformat, ARG_framesize, ARG_fb_count, ARG_fb_location};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_pixformat,      MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = PIXFORMAT_RGB565 } },
        { MP_QSTR_framesize,      MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = FRAMESIZE_QVGA } },
        { MP_QSTR_fb_count,       MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = 2 } },
        { MP_QSTR_fb_location,    MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = CAMERA_FB_IN_PSRAM } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    int format = args[ARG_pixformat].u_int;
    if ((format < 0) || (format > 1)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Pixelformat is not valid"));
    }
    camera_config.pixel_format = format;

    int size = args[ARG_framesize].u_int;
    if ((size < 0) || (size > 8)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Image framesize is not valid"));
    }
    camera_config.frame_size = size;

    int fb_count = args[ARG_fb_count].u_int;
    if ((fb_count < 0) || (fb_count > 3)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Framebuffer count is not valid"));
    }
    camera_config.fb_count = fb_count;

    int fb_location = args[ARG_fb_location].u_int;
    if ((fb_location != 0) && (fb_location != 1)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Framebuffer location is not valid"));
    }
    camera_config.fb_location = fb_location;

    if (status == E_CAMERA_INIT) {
        esp_camera_deinit();
    }
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) {
        status = E_CAMERA_DEINIT;
        return false;
    }
    status = E_CAMERA_INIT;
    return true;
}

STATIC mp_obj_t camera_init(mp_uint_t n_pos_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    bool init = camera_init_helper(n_pos_args, pos_args, kw_args);
    if (init) {
        return mp_const_true;
    } else {
        ESP_LOGE(TAG, "Camera init Failed");
        return mp_const_false;
    }
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(camera_init_obj, 0, camera_init);

STATIC mp_obj_t camera_deinit() {
    esp_err_t err = esp_camera_deinit();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Camera deinit Failed");
        return mp_const_false;
    }
    status = E_CAMERA_DEINIT;
    return mp_const_true;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(camera_deinit_obj, camera_deinit);

STATIC mp_obj_t camera_skip_frames(uint n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    mp_map_elem_t *kw_arg = mp_map_lookup(kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_time), MP_MAP_LOOKUP);
    mp_int_t time = 300; // OV Recommended.

    if (kw_arg != NULL) {
        time = mp_obj_get_int(kw_arg->value);
    }

    uint32_t millis = mp_hal_ticks_us() / 1000;

    if (!n_args) {
        while ((mp_hal_ticks_us() / 1000 - millis) < time) { // 32-bit math handles wrap around...
            camera_fb_t *fb = esp_camera_fb_get();
            if (fb == NULL) {
                continue;
            }
            esp_camera_fb_return(fb);
        }
    } else {
        for (int i = 0, j = mp_obj_get_int(args[0]); i < j; i++) {
            if ((kw_arg != NULL) && ((mp_hal_ticks_us() / 1000 - millis) >= time)) {
                break;
            }

            camera_fb_t *fb = esp_camera_fb_get();
            if (fb == NULL) {
                continue;
            }
            esp_camera_fb_return(fb);
        }
    }

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(camera_skip_frames_obj, 0, camera_skip_frames);

STATIC mp_obj_t camera_capture() {
    // acquire a frame
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        ESP_LOGE(TAG, "Camera capture Failed");
        return mp_const_false;
    }
    mp_obj_t image = mp_obj_new_bytes(fb->buf, fb->len);

    esp_camera_fb_return(fb);
    return image;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(camera_capture_obj, camera_capture);

STATIC mp_obj_t camera_capture_to_jpg(mp_obj_t quality_in) {
    // acquire a frame
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        ESP_LOGE(TAG, "Camera capture Failed");
        return mp_const_false;
    }

    mp_obj_t image = mp_const_none;
    if (fb->format == PIXFORMAT_JPEG) {
        image = mp_obj_new_bytes(fb->buf, fb->len);
    } else {
        uint8_t quality = mp_obj_get_int(quality_in);
        uint8_t *out = NULL;
        size_t out_len = 0;
        if (frame2jpg(fb, quality, &out, &out_len)) {
            image = mp_obj_new_bytes(out, out_len);
            free(out);
        }
    }

    esp_camera_fb_return(fb);
    return image;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_capture_to_jpg_obj, camera_capture_to_jpg);

STATIC mp_obj_t camera_capture_to_bmp() {
    // acquire a frame
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        ESP_LOGE(TAG, "Camera capture Failed");
        return mp_const_false;
    }

    mp_obj_t image = mp_const_none;
    uint8_t *out = NULL;
    size_t out_len = 0;
    if (frame2bmp(fb, &out, &out_len)) {
        image = mp_obj_new_bytes(out, out_len);
        free(out);
    }

    esp_camera_fb_return(fb);
    return image;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(camera_capture_to_bmp_obj, camera_capture_to_bmp);

STATIC mp_obj_t camera_pixformat(mp_obj_t pixformat) {
    int format = mp_obj_get_int(pixformat);
    if ((format < 0) || (format > 1)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Pixelformat is not valid"));
    }

    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Pixelformat Failed");
        return mp_const_false;
    }

    s->set_pixformat(s, format);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_pixformat_obj, camera_pixformat);

STATIC mp_obj_t camera_framesize(mp_obj_t framesize) {
    int size = mp_obj_get_int(framesize);
    if ((size < 0) || (size > 8)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Image framesize is not valid"));
    }

    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Framesize Failed");
        return mp_const_false;
    }

    s->set_framesize(s, size);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_framesize_obj, camera_framesize);

STATIC mp_obj_t camera_contrast(mp_obj_t contrast) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Contrast Failed");
        return mp_const_false;
    }

    int val = mp_obj_get_int(contrast); // -2,2 (default 0). 2 highcontrast
    s->set_contrast(s, val);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_contrast_obj, camera_contrast);

STATIC mp_obj_t camera_global_gain(mp_obj_t gain_level) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Contrast Failed");
        return mp_const_false;
    }

    int val = mp_obj_get_int(gain_level); // -2,2 (default 0). 2 highcontrast
    s->set_gain_ctrl(s, val);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_global_gain_obj, camera_global_gain);

STATIC mp_obj_t camera_hmirror(mp_obj_t direction) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Mirroring Failed");
        return mp_const_false;
    }
    int dir = mp_obj_get_int(direction);
    s->set_hmirror(s, dir);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_hmirror_obj, camera_hmirror);

STATIC mp_obj_t camera_vflip(mp_obj_t direction) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Flipping Failed");
        return mp_const_false;
    }
    int dir = mp_obj_get_int(direction);
    s->set_vflip(s, dir);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_vflip_obj, camera_vflip);

STATIC mp_obj_t camera_colorbar(mp_obj_t enable) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Colorbar Failed");
        return mp_const_false;
    }
    int val = mp_obj_get_int(enable);
    s->set_colorbar(s, (bool)val);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(camera_colorbar_obj, camera_colorbar);

STATIC const mp_rom_map_elem_t m5_camera_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_camera) },

    // functions
    { MP_ROM_QSTR(MP_QSTR_init),            MP_ROM_PTR(&camera_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit),          MP_ROM_PTR(&camera_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_skip_frames),     MP_ROM_PTR(&camera_skip_frames_obj) },
    { MP_ROM_QSTR(MP_QSTR_capture),         MP_ROM_PTR(&camera_capture_obj) },
    { MP_ROM_QSTR(MP_QSTR_capture_to_jpg),  MP_ROM_PTR(&camera_capture_to_jpg_obj) },
    { MP_ROM_QSTR(MP_QSTR_capture_to_bmp),  MP_ROM_PTR(&camera_capture_to_bmp_obj) },
    { MP_ROM_QSTR(MP_QSTR_pixformat),       MP_ROM_PTR(&camera_pixformat_obj) },
    { MP_ROM_QSTR(MP_QSTR_framesize),       MP_ROM_PTR(&camera_framesize_obj) },
    { MP_ROM_QSTR(MP_QSTR_contrast),        MP_ROM_PTR(&camera_contrast_obj) },
    { MP_ROM_QSTR(MP_QSTR_global_gain),     MP_ROM_PTR(&camera_global_gain_obj) },
    { MP_ROM_QSTR(MP_QSTR_hmirror),         MP_ROM_PTR(&camera_hmirror_obj) },
    { MP_ROM_QSTR(MP_QSTR_vflip),           MP_ROM_PTR(&camera_vflip_obj) },
    { MP_ROM_QSTR(MP_QSTR_colorbar),        MP_ROM_PTR(&camera_colorbar_obj) },

    // output format
    { MP_ROM_QSTR(MP_QSTR_YUV422),          MP_ROM_INT(PIXFORMAT_YUV422) },
    { MP_ROM_QSTR(MP_QSTR_GRAYSCALE),       MP_ROM_INT(PIXFORMAT_GRAYSCALE) },
    { MP_ROM_QSTR(MP_QSTR_RGB565),          MP_ROM_INT(PIXFORMAT_RGB565) },

    // resolution
    { MP_ROM_QSTR(MP_QSTR_FRAME_96X96),     MP_ROM_INT(FRAMESIZE_96X96) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QQVGA),     MP_ROM_INT(FRAMESIZE_QQVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QCIF),      MP_ROM_INT(FRAMESIZE_QCIF) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_HQVGA),     MP_ROM_INT(FRAMESIZE_HQVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_240X240),   MP_ROM_INT(FRAMESIZE_240X240) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_QVGA),      MP_ROM_INT(FRAMESIZE_QVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_CIF),       MP_ROM_INT(FRAMESIZE_CIF) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_HVGA),      MP_ROM_INT(FRAMESIZE_HVGA) },
    { MP_ROM_QSTR(MP_QSTR_FRAME_VGA),       MP_ROM_INT(FRAMESIZE_VGA) },

    { MP_ROM_QSTR(MP_QSTR_DRAM),            MP_ROM_INT(CAMERA_FB_IN_DRAM) },
    { MP_ROM_QSTR(MP_QSTR_PSRAM),           MP_ROM_INT(CAMERA_FB_IN_PSRAM) },
};

STATIC MP_DEFINE_CONST_DICT(mp_module_m5_camera_globals, m5_camera_globals_table);

// Define module object.
const mp_obj_module_t m5camera_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_m5_camera_globals,
};

MP_REGISTER_MODULE(MP_QSTR_camera, m5camera_user_cmodule);
