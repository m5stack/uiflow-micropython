/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objstr.h"
#include "py/stream.h"
#include "extmod/vfs.h"
#include "extmod/vfs_fat.h"

#include "esp_camera.h"
#include "imlib.h"
#include "py_image.h"



static mp_obj_t py_jpg_encode(size_t n_args, const mp_obj_t *args) {
    image_t *img = (image_t *)py_image_cobj(args[0]);
    uint8_t quality = 30;

    if (img->pixfmt == OMV_PIXFORMAT_JPEG) {
        return args[0];
    }

    if (n_args > 1) {
        quality = mp_obj_get_int(args[1]);
        if (quality > 100) {
            quality = 100;
        }
    }

    static image_t img_jpg;
    img_jpg.w = img->w;
    img_jpg.h = img->h;
    img_jpg.pixfmt = OMV_PIXFORMAT_JPEG;
    if (img_jpg.data) {
        free(img_jpg.data);
    }
    fmt2jpg(img->data, img->size, img->w, img->h, PIXFORMAT_RGB565, quality, &img_jpg.data, (size_t *)&img_jpg.size);

    return py_image_from_struct(&img_jpg);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(py_jpg_encode_obj, 1, 2, py_jpg_encode);

static mp_obj_t py_jpg_decode(mp_obj_t img_obj) {
    image_t *img_jpg = (image_t *)py_image_cobj(img_obj);
    static image_t img_rgb565;

    if (img_rgb565.w != img_jpg->w || img_rgb565.h != img_jpg->h) {
        img_rgb565.pixfmt = OMV_PIXFORMAT_RGB565;
        img_rgb565.w = img_jpg->w;
        img_rgb565.h = img_jpg->h;
        img_rgb565.size = img_rgb565.w * img_rgb565.h * sizeof(uint16_t); // RGB565
        if (img_rgb565.data == NULL) {
            img_rgb565.data = (uint8_t *)heap_caps_malloc(img_rgb565.size, MALLOC_CAP_8BIT | MALLOC_CAP_SPIRAM);
        } else {
            // TODO:
            // img_rgb565.data = (uint8_t *)heap_caps_realloc(img_rgb565.data, img_rgb565.size, MALLOC_CAP_8BIT | MALLOC_CAP_SPIRAM);
        }
        if (img_rgb565.data == NULL) {
            mp_raise_msg(&mp_type_MemoryError, MP_ERROR_TEXT("Failed to allocate memory for image buffer"));
        }
    }
    jpg2rgb565(img_jpg->data, img_jpg->size, img_rgb565.data, JPG_SCALE_NONE);

    return py_image_from_struct(&img_rgb565);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_jpg_decode_obj, py_jpg_decode);


static const mp_rom_map_elem_t globals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jpg)       },
    { MP_ROM_QSTR(MP_QSTR_encode),   MP_ROM_PTR(&py_jpg_encode_obj) },
    { MP_ROM_QSTR(MP_QSTR_decode),   MP_ROM_PTR(&py_jpg_decode_obj) },
};
static MP_DEFINE_CONST_DICT(globals_dict, globals_dict_table);

const mp_obj_module_t mp_module_jpg = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&globals_dict,
};

MP_REGISTER_MODULE(MP_QSTR_jpg, mp_module_jpg);
