/*
 * Copyright [2021] Mauro Riva <info@lemariva.com>
 * Copyright (c) 2024 M5Stack Technology CO LTD
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
#include "driver/gpio.h"

#define TAG "camera"

#if BOARD_ID == 10  // CoreS3

#define CORES3_CAMERA_POWER_DOWN_PIN -1
#define CORES3_CAMERA_RESET_PIN      -1
#define CORES3_CAMERA_XCLK_PIN       2
#define CORES3_CAMERA_SDA_PIN        12
#define CORES3_CAMERA_SCL_PIN        11
#define CORES3_CAMERA_D7_PIN         47
#define CORES3_CAMERA_D6_PIN         48
#define CORES3_CAMERA_D5_PIN         16
#define CORES3_CAMERA_D4_PIN         15
#define CORES3_CAMERA_D3_PIN         42
#define CORES3_CAMERA_D2_PIN         41
#define CORES3_CAMERA_D1_PIN         40
#define CORES3_CAMERA_D0_PIN         39
#define CORES3_CAMERA_VSYNC_PIN      46
#define CORES3_CAMERA_HREF_PIN       38
#define CORES3_CAMERA_PCLK_PIN       45

static camera_config_t camera_config = {
    .pin_pwdn = CORES3_CAMERA_POWER_DOWN_PIN,
    .pin_reset = CORES3_CAMERA_RESET_PIN,
    .pin_xclk = CORES3_CAMERA_XCLK_PIN,
    .pin_sscb_sda = -1,   // CORES3_CAMERA_SDA_PIN, // 共用 I2C1 在其他地方初始化
    .pin_sscb_scl = -1,   // CORES3_CAMERA_SCL_PIN,
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
    .pixel_format = PIXFORMAT_RGB565,
    .frame_size = FRAMESIZE_QVGA,
    .fb_count = 2,
    .fb_location = CAMERA_FB_IN_PSRAM,
    .grab_mode = CAMERA_GRAB_LATEST,
    .sccb_i2c_port = 1,  // use I2C1
};

#elif BOARD_ID == 144  // AtomS3R_CAM

#define ATOMS3R_CAM_PIN_PWDN  -1
#define ATOMS3R_CAM_PIN_RESET -1
#define ATOMS3R_CAM_PIN_HREF  14  // 水平
#define ATOMS3R_CAM_PIN_VSYNC 10  // 垂直同步
#define ATOMS3R_CAM_PIN_XCLK  21  // 像素时钟
#define ATOMS3R_CAM_PIN_PCLK  40  // 时钟
#define ATOMS3R_CAM_PIN_SIOC  9   // 串行时钟
#define ATOMS3R_CAM_PIN_SIOD  12  // 串行数据
#define ATOMS3R_CAM_PIN_D0    3   // 数据0
#define ATOMS3R_CAM_PIN_D1    42  // 数据1
#define ATOMS3R_CAM_PIN_D2    46  // 数据2
#define ATOMS3R_CAM_PIN_D3    48  // 数据3
#define ATOMS3R_CAM_PIN_D4    4   // 数据4
#define ATOMS3R_CAM_PIN_D5    17  // 数据5
#define ATOMS3R_CAM_PIN_D6    11  // 数据6
#define ATOMS3R_CAM_PIN_D7    13  // 数据7
#define ATOMS3R_CAM_PIN_EN    18  // 电源控制

camera_config_t camera_config = {
    .pin_pwdn = ATOMS3R_CAM_PIN_PWDN,
    .pin_reset = ATOMS3R_CAM_PIN_RESET,
    .pin_sccb_scl = ATOMS3R_CAM_PIN_SIOC,
    .pin_sccb_sda = ATOMS3R_CAM_PIN_SIOD,
    .pin_d0 = ATOMS3R_CAM_PIN_D0,
    .pin_d1 = ATOMS3R_CAM_PIN_D1,
    .pin_d2 = ATOMS3R_CAM_PIN_D2,
    .pin_d3 = ATOMS3R_CAM_PIN_D3,
    .pin_d4 = ATOMS3R_CAM_PIN_D4,
    .pin_d5 = ATOMS3R_CAM_PIN_D5,
    .pin_d6 = ATOMS3R_CAM_PIN_D6,
    .pin_d7 = ATOMS3R_CAM_PIN_D7,
    .pin_vsync = ATOMS3R_CAM_PIN_VSYNC,
    .pin_href = ATOMS3R_CAM_PIN_HREF,
    .pin_pclk = ATOMS3R_CAM_PIN_PCLK,
    .pin_xclk = ATOMS3R_CAM_PIN_XCLK,
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,
    .pixel_format = PIXFORMAT_RGB565,
    .frame_size = FRAMESIZE_QVGA,
    .jpeg_quality = 6,
    .fb_count = 2,
    .fb_location = CAMERA_FB_IN_PSRAM,
    .grab_mode = CAMERA_GRAB_WHEN_EMPTY,
};

#endif

typedef struct {
    bool hmirror;
    bool vflip;
} cam_config_t;
cam_config_t g_cam_config;

static enum { E_CAMERA_INIT, E_CAMERA_DEINIT } status = E_CAMERA_DEINIT;

static bool camera_init_helper(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_pixformat, ARG_framesize, ARG_fb_count, ARG_fb_location };
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        {MP_QSTR_pixformat, MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = PIXFORMAT_RGB565}},
        {MP_QSTR_framesize, MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = FRAMESIZE_QVGA}},
        {MP_QSTR_fb_count, MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = 2}},
        {MP_QSTR_fb_location, MP_ARG_INT | MP_ARG_KW_ONLY, {.u_int = CAMERA_FB_IN_PSRAM}},
    };

#if BOARD_ID == 144
    gpio_reset_pin(ATOMS3R_CAM_PIN_EN);
    gpio_set_direction(ATOMS3R_CAM_PIN_EN, GPIO_MODE_OUTPUT);
    gpio_set_level(ATOMS3R_CAM_PIN_EN, 0);  // 拉低开启电源
    vTaskDelay(pdMS_TO_TICKS(300));
#endif

    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    int format = args[ARG_pixformat].u_int;
    if ((format < 0) || (format > PIXFORMAT_RGB555)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Pixelformat is not valid"));
    }
    camera_config.pixel_format = format;

    int size = args[ARG_framesize].u_int;
    if ((size < 0) || (size > FRAMESIZE_QXGA)) {
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

static mp_obj_t camera_init(size_t n_pos_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    bool init = camera_init_helper(n_pos_args, pos_args, kw_args);
    g_cam_config.hmirror = true;
    g_cam_config.vflip = false;
    if (init) {
        return mp_const_true;
    } else {
        ESP_LOGE(TAG, "Camera init Failed");
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_init_obj, 0, camera_init);

static mp_obj_t camera_deinit() {
    esp_err_t err = esp_camera_deinit();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Camera deinit Failed");
        return mp_const_false;
    }
    status = E_CAMERA_DEINIT;
    return mp_const_true;
}
static MP_DEFINE_CONST_FUN_OBJ_0(camera_deinit_obj, camera_deinit);

static mp_obj_t camera_skip_frames(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    mp_map_elem_t *kw_arg = mp_map_lookup(kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_time), MP_MAP_LOOKUP);
    mp_int_t time = 300;          // OV Recommended.

    if (kw_arg != NULL) {
        time = mp_obj_get_int(kw_arg->value);
    }

    uint32_t millis = mp_hal_ticks_us() / 1000;

    if (!n_args) {
        while ((mp_hal_ticks_us() / 1000 - millis) < time) {  // 32-bit math handles wrap around...
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
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_skip_frames_obj, 0, camera_skip_frames);

static mp_obj_t camera_capture() {
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
static MP_DEFINE_CONST_FUN_OBJ_0(camera_capture_obj, camera_capture);

static mp_obj_t camera_capture_to_jpg(mp_obj_t quality_in) {
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
static MP_DEFINE_CONST_FUN_OBJ_1(camera_capture_to_jpg_obj, camera_capture_to_jpg);

static mp_obj_t camera_capture_to_bmp() {
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
static MP_DEFINE_CONST_FUN_OBJ_0(camera_capture_to_bmp_obj, camera_capture_to_bmp);

static mp_obj_t camera_pixformat(mp_obj_t pixformat) {
    int format = mp_obj_get_int(pixformat);
    //  if ((format < 0) || (format > 1)) {
    //      mp_raise_ValueError(MP_ERROR_TEXT("Pixelformat is not valid"));
    //  }

    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Pixelformat Failed");
        return mp_const_false;
    }

    int ret = s->set_pixformat(s, format);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_pixformat_obj, camera_pixformat);

static mp_obj_t camera_framesize(mp_obj_t framesize) {
    int size = mp_obj_get_int(framesize);
    if ((size < 0) || (size > 8)) {
        mp_raise_ValueError(MP_ERROR_TEXT("Image framesize is not valid"));
    }

    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Framesize Failed");
        return mp_const_false;
    }

    int ret = s->set_framesize(s, size);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_framesize_obj, camera_framesize);

static mp_obj_t camera_contrast(mp_obj_t contrast) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Contrast Failed");
        return mp_const_false;
    }

    int val = mp_obj_get_int(contrast);  // -2,2 (default 0). 2 highcontrast
    int ret = s->set_contrast(s, val);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_contrast_obj, camera_contrast);

static mp_obj_t camera_global_gain(mp_obj_t gain_level) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Contrast Failed");
        return mp_const_false;
    }

    int val = mp_obj_get_int(gain_level);  // -2,2 (default 0). 2 highcontrast
    int ret = s->set_gain_ctrl(s, val);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_global_gain_obj, camera_global_gain);

static mp_obj_t camera_hmirror(mp_obj_t direction) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Mirroring Failed");
        return mp_const_false;
    }
    int dir = mp_obj_get_int(direction);
    int ret = s->set_hmirror(s, dir);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_hmirror_obj, camera_hmirror);

static mp_obj_t camera_vflip(mp_obj_t direction) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Flipping Failed");
        return mp_const_false;
    }
    int dir = mp_obj_get_int(direction);
    int ret = s->set_vflip(s, dir);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_vflip_obj, camera_vflip);

static mp_obj_t camera_colorbar(mp_obj_t enable) {
    sensor_t *s = esp_camera_sensor_get();
    if (!s) {
        ESP_LOGE(TAG, "Colorbar Failed");
        return mp_const_false;
    }
    int val = mp_obj_get_int(enable);
    int ret = s->set_colorbar(s, (bool)val);
    if (ret == 0) {
        return mp_const_true;
    } else {
        return mp_const_false;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_colorbar_obj, camera_colorbar);

// ====================================================================
// for omv
#include "esp_camera.h"
#include "py_image.h"
#include "imlib.h"
#include "utils.h"

static camera_fb_t *g_frame = NULL;

void swap_rgb565(uint16_t *pixel) {
    *pixel = (*pixel >> 8) | (*pixel << 8);
}

void image_endian_swap(image_t *img) {
    uint16_t *pixel = (uint16_t *)img->data;
    for (int i = 0; i < img->w * img->h; i++) {
        swap_rgb565(&pixel[i]);
    }
}

static mp_obj_t py_camera_snapshot() {
    if (g_frame != NULL) {
        esp_camera_fb_return(g_frame);
        g_frame = NULL;
    }
    g_frame = esp_camera_fb_get();

    image_t img;
    img.size = g_frame->len;
    img.w = g_frame->width;
    img.h = g_frame->height;
    if (g_frame->format == PIXFORMAT_RGB565) {
        img.pixfmt = OMV_PIXFORMAT_RGB565;
    } else if (g_frame->format == PIXFORMAT_GRAYSCALE) {
        img.pixfmt = OMV_PIXFORMAT_GRAYSCALE;
    } else if (g_frame->format == PIXFORMAT_JPEG) {
        img.pixfmt = OMV_PIXFORMAT_JPEG;
    }
    img.data = g_frame->buf;
    // image_endian_swap(&img);

    return py_image_from_struct(&img);
}
static MP_DEFINE_CONST_FUN_OBJ_0(py_camera_snapshot_obj, py_camera_snapshot);

static mp_obj_t py_camera_set_hmirror(mp_obj_t enable) {
    sensor_t *s = esp_camera_sensor_get();
    g_cam_config.hmirror = mp_obj_is_true(enable);
    s->set_hmirror(s, g_cam_config.hmirror);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_camera_set_hmirror_obj, py_camera_set_hmirror);

static mp_obj_t py_camera_set_vflip(mp_obj_t enable) {
    sensor_t *s = esp_camera_sensor_get();
    g_cam_config.vflip = mp_obj_is_true(enable);
    s->set_vflip(s, g_cam_config.vflip);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_camera_set_vflip_obj, py_camera_set_vflip);

static mp_obj_t py_camera_get_hmirror(void) {
    return mp_obj_new_bool(g_cam_config.hmirror);
}
static MP_DEFINE_CONST_FUN_OBJ_0(py_camera_get_hmirror_obj, py_camera_get_hmirror);

static mp_obj_t py_camera_get_vflip(void) {
    return mp_obj_new_bool(g_cam_config.vflip);
}
static MP_DEFINE_CONST_FUN_OBJ_0(py_camera_get_vflip_obj, py_camera_get_vflip);

static const mp_rom_map_elem_t camera_globals_dict_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_camera)},
    // functions
    {MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&camera_init_obj)},
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&camera_deinit_obj)},
    {MP_ROM_QSTR(MP_QSTR_skip_frames), MP_ROM_PTR(&camera_skip_frames_obj)},
    {MP_ROM_QSTR(MP_QSTR_capture), MP_ROM_PTR(&camera_capture_obj)},
    {MP_ROM_QSTR(MP_QSTR_capture_to_jpg), MP_ROM_PTR(&camera_capture_to_jpg_obj)},
    {MP_ROM_QSTR(MP_QSTR_capture_to_bmp), MP_ROM_PTR(&camera_capture_to_bmp_obj)},
    {MP_ROM_QSTR(MP_QSTR_pixformat), MP_ROM_PTR(&camera_pixformat_obj)},
    {MP_ROM_QSTR(MP_QSTR_framesize), MP_ROM_PTR(&camera_framesize_obj)},
    {MP_ROM_QSTR(MP_QSTR_contrast), MP_ROM_PTR(&camera_contrast_obj)},
    {MP_ROM_QSTR(MP_QSTR_global_gain), MP_ROM_PTR(&camera_global_gain_obj)},
    {MP_ROM_QSTR(MP_QSTR_hmirror), MP_ROM_PTR(&camera_hmirror_obj)},
    {MP_ROM_QSTR(MP_QSTR_vflip), MP_ROM_PTR(&camera_vflip_obj)},
    {MP_ROM_QSTR(MP_QSTR_colorbar), MP_ROM_PTR(&camera_colorbar_obj)},
    // output format
    {MP_ROM_QSTR(MP_QSTR_YUV422), MP_ROM_INT(PIXFORMAT_YUV422)},
    {MP_ROM_QSTR(MP_QSTR_GRAYSCALE), MP_ROM_INT(PIXFORMAT_GRAYSCALE)},
    {MP_ROM_QSTR(MP_QSTR_RGB565), MP_ROM_INT(PIXFORMAT_RGB565)},
    {MP_ROM_QSTR(MP_QSTR_JPEG), MP_ROM_INT(PIXFORMAT_JPEG)},
    // resolution
    {MP_ROM_QSTR(MP_QSTR_FRAME_96X96), MP_ROM_INT(FRAMESIZE_96X96)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_QQVGA), MP_ROM_INT(FRAMESIZE_QQVGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_QCIF), MP_ROM_INT(FRAMESIZE_QCIF)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_HQVGA), MP_ROM_INT(FRAMESIZE_HQVGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_240X240), MP_ROM_INT(FRAMESIZE_240X240)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_QVGA), MP_ROM_INT(FRAMESIZE_QVGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_CIF), MP_ROM_INT(FRAMESIZE_CIF)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_HVGA), MP_ROM_INT(FRAMESIZE_HVGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_VGA), MP_ROM_INT(FRAMESIZE_VGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_QVGA), MP_ROM_INT(FRAMESIZE_SVGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_CIF), MP_ROM_INT(FRAMESIZE_XGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_HVGA), MP_ROM_INT(FRAMESIZE_HD)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_VGA), MP_ROM_INT(FRAMESIZE_SXGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_QVGA), MP_ROM_INT(FRAMESIZE_UXGA)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_CIF), MP_ROM_INT(FRAMESIZE_FHD)},
    {MP_ROM_QSTR(MP_QSTR_FRAME_QXGA), MP_ROM_INT(FRAMESIZE_QXGA)},
    //
    {MP_ROM_QSTR(MP_QSTR_DRAM), MP_ROM_INT(CAMERA_FB_IN_DRAM)},
    {MP_ROM_QSTR(MP_QSTR_PSRAM), MP_ROM_INT(CAMERA_FB_IN_PSRAM)},
    // for omv
    {MP_ROM_QSTR(MP_QSTR_snapshot), MP_ROM_PTR(&py_camera_snapshot_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_hmirror), MP_ROM_PTR(&py_camera_set_hmirror_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_vflip), MP_ROM_PTR(&py_camera_set_vflip_obj)},
    {MP_ROM_QSTR(MP_QSTR_get_hmirror), MP_ROM_PTR(&py_camera_get_hmirror_obj)},
    {MP_ROM_QSTR(MP_QSTR_get_vflip), MP_ROM_PTR(&py_camera_get_vflip_obj)},
    {MP_ROM_QSTR(MP_QSTR_QQVGA), MP_ROM_INT(FRAMESIZE_QQVGA)},      // 160x120
    {MP_ROM_QSTR(MP_QSTR_QCIF), MP_ROM_INT(FRAMESIZE_QCIF)},        // 176x144
    {MP_ROM_QSTR(MP_QSTR_HQVGA), MP_ROM_INT(FRAMESIZE_HQVGA)},      // 240x176
    {MP_ROM_QSTR(MP_QSTR_240X240), MP_ROM_INT(FRAMESIZE_240X240)},  // 240x240
    {MP_ROM_QSTR(MP_QSTR_QVGA), MP_ROM_INT(FRAMESIZE_QVGA)},        // 320x240
    {MP_ROM_QSTR(MP_QSTR_VGA), MP_ROM_INT(FRAMESIZE_VGA)},          // 640x480
    {MP_ROM_QSTR(MP_QSTR_SVGA), MP_ROM_INT(FRAMESIZE_SVGA)},        // 800x600
    {MP_ROM_QSTR(MP_QSTR_XGA), MP_ROM_INT(FRAMESIZE_XGA)},          // 1024x768
    {MP_ROM_QSTR(MP_QSTR_HD), MP_ROM_INT(FRAMESIZE_HD)},            // 1280x720
    {MP_ROM_QSTR(MP_QSTR_SXGA), MP_ROM_INT(FRAMESIZE_SXGA)},        // 1280x1024
    {MP_ROM_QSTR(MP_QSTR_UXGA), MP_ROM_INT(FRAMESIZE_UXGA)},        // 1600x1200
    {MP_ROM_QSTR(MP_QSTR_FHD), MP_ROM_INT(FRAMESIZE_FHD)},          // 1920x1080
    {MP_ROM_QSTR(MP_QSTR_QXGA), MP_ROM_INT(FRAMESIZE_QXGA)},        // 2048x1536
};

static MP_DEFINE_CONST_DICT(camera_globals_dict, camera_globals_dict_table);

// Define module object.
const mp_obj_module_t py_module_camera = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&camera_globals_dict,
};

MP_REGISTER_MODULE(MP_QSTR_camera, py_module_camera);
