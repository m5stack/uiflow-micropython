/*
 * SPDX-License-Identifier: MIT
 *
 * Copyright (C) 2013-2025 OpenMV, LLC.
 * Copyright (c) 2025 M5Stack Technology CO LTD
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Image Python module.
 */
#include "py_image.h"
#include <stdio.h>
#include <string.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "py/objlist.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include "py/objtype.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "imlib.h"
#include "py_helper.h"
#include "py_assert.h"
#include "quirc.h"
#include <math.h>


#define PY_ASSERT_TYPE(obj, type)                            \
    do {                                                     \
        __typeof__ (obj) _a = (obj);                         \
        __typeof__ (type) _b = (type);                       \
        if (!MP_OBJ_IS_TYPE(_a, _b)) {                       \
            mp_raise_msg_varg(&mp_type_TypeError,            \
    MP_ERROR_TEXT(                 \
    "Can't convert %s to %s"), \
    mp_obj_get_type_str(_a),       \
    mp_obj_get_type_str(_b));      \
        }                                                    \
    } while (0)

size_t image_size(image_t *img) {
    return img->size;
}


// ==================================================================================
// class: image.Image
// ==================================================================================


// ==================================================================================
// Basic Methods
// ==================================================================================
const mp_obj_type_t py_image_type;


void *py_image_cobj(mp_obj_t img_obj) {
    PY_ASSERT_TYPE(img_obj, &py_image_type);
    return &((py_image_obj_t *)img_obj)->_cobj;
}


static mp_obj_t py_image_width(mp_obj_t img_obj) {
    return mp_obj_new_int(((image_t *)py_image_cobj(img_obj))->w);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_image_width_obj, py_image_width);

static mp_obj_t py_image_height(mp_obj_t img_obj) {
    return mp_obj_new_int(((image_t *)py_image_cobj(img_obj))->h);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_image_height_obj, py_image_height);

static mp_obj_t py_image_format(mp_obj_t img_obj) {
    image_t *image = py_image_cobj(img_obj);
    switch (image->pixfmt) {
        case OMV_PIXFORMAT_BINARY:
            return mp_obj_new_int(OMV_PIXFORMAT_BINARY);
        case OMV_PIXFORMAT_GRAYSCALE:
            return mp_obj_new_int(OMV_PIXFORMAT_GRAYSCALE);
        case OMV_PIXFORMAT_RGB565:
            return mp_obj_new_int(OMV_PIXFORMAT_RGB565);
        case OMV_PIXFORMAT_BAYER_ANY:
            return mp_obj_new_int(OMV_PIXFORMAT_BAYER);
        case OMV_PIXFORMAT_YUV_ANY:
            return mp_obj_new_int(OMV_PIXFORMAT_YUV422);
        case OMV_PIXFORMAT_JPEG:
            return mp_obj_new_int(OMV_PIXFORMAT_JPEG);
        case OMV_PIXFORMAT_PNG:
            return mp_obj_new_int(OMV_PIXFORMAT_PNG);
        default:
            return mp_obj_new_int(OMV_PIXFORMAT_INVALID);
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_image_format_obj, py_image_format);

static mp_obj_t py_image_size(mp_obj_t img_obj) {
    return mp_obj_new_int(image_size((image_t *)py_image_cobj(img_obj)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_image_size_obj, py_image_size);

static mp_obj_t py_image_bytearray(mp_obj_t img_obj) {
    image_t *arg_img = (image_t *)py_image_cobj(img_obj);
    return mp_obj_new_bytearray_by_ref(image_size(arg_img), arg_img->data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_image_bytearray_obj, py_image_bytearray);


// ====================================================================================
// Drawings Methods
// ====================================================================================
static mp_obj_t py_image_clear(mp_obj_t img_obj) {
    image_t *arg_img = (image_t *)py_image_cobj(img_obj);
    memset(arg_img->pixels, 0, image_size(arg_img));
    return img_obj;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_image_clear_obj, py_image_clear);

static mp_obj_t py_image_draw_line(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 0, 4, &arg_vec);

    image_t *arg_img = (image_t *)py_image_cobj(arg_vec[0]);
    int arg_x0 = mp_obj_get_int(arg_vec[1]);
    int arg_y0 = mp_obj_get_int(arg_vec[2]);
    int arg_x1 = mp_obj_get_int(arg_vec[3]);
    int arg_y1 = mp_obj_get_int(arg_vec[4]);
    // int arg_c = py_helper_keyword_color(n_args, args, offset + 0, kw_args, -1);
    int arg_c = py_helper_keyword_color(arg_img, n_args, args, offset + 0, kw_args, -1); // White.
    int arg_thickness = py_helper_keyword_int(n_args, args, offset + 1, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);

    imlib_draw_line(arg_img, arg_x0, arg_y0, arg_x1, arg_y1, arg_c, arg_thickness);

    return arg_vec[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_line_obj, 3, py_image_draw_line);

static mp_obj_t py_image_draw_rectangle(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 0, 4, &arg_vec);

    image_t *arg_img = (image_t *)py_image_cobj(arg_vec[0]);
    int arg_rx = mp_obj_get_int(arg_vec[1]);
    int arg_ry = mp_obj_get_int(arg_vec[2]);
    int arg_rw = mp_obj_get_int(arg_vec[3]);
    int arg_rh = mp_obj_get_int(arg_vec[4]);
    // int arg_c = py_helper_keyword_color(n_args, args, offset + 0, kw_args, -1);
    int arg_c = py_helper_keyword_color(arg_img, n_args, args, offset + 0, kw_args, -1); // White.
    int arg_thickness = py_helper_keyword_int(n_args, args, offset + 1, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);
    int arg_fill = py_helper_keyword_int(n_args, args, offset + 2, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_fill), 1);

    imlib_draw_rectangle(arg_img, arg_rx, arg_ry, arg_rw, arg_rh, arg_c, arg_thickness, arg_fill);

    return arg_vec[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_rectangle_obj, 4, py_image_draw_rectangle);

static mp_obj_t py_image_draw_circle(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 0, 3, &arg_vec);

    image_t *arg_img = (image_t *)py_image_cobj(arg_vec[0]);
    int arg_cx = mp_obj_get_int(arg_vec[1]);
    int arg_cy = mp_obj_get_int(arg_vec[2]);
    int arg_radius = mp_obj_get_int(arg_vec[3]);
    // int arg_c = py_helper_keyword_color(n_args, args, offset + 0, kw_args, -1);
    int arg_c = py_helper_keyword_color(arg_img, n_args, args, offset + 0, kw_args, -1); // White.
    int arg_thickness = py_helper_keyword_int(n_args, args, offset + 1, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);
    int arg_fill = py_helper_keyword_int(n_args, args, offset + 2, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_fill), 1);

    imlib_draw_circle(arg_img, arg_cx, arg_cy, arg_radius, arg_c, arg_thickness, arg_fill);

    return arg_vec[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_circle_obj, 4, py_image_draw_circle);

static mp_obj_t py_image_draw_ellipse(uint n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    image_t *arg_img = py_helper_arg_to_image(args[0], ARG_IMAGE_MUTABLE);

    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 1, 5, &arg_vec);
    int arg_cx = mp_obj_get_int(arg_vec[0]);
    int arg_cy = mp_obj_get_int(arg_vec[1]);
    int arg_rx = mp_obj_get_int(arg_vec[2]);
    int arg_ry = mp_obj_get_int(arg_vec[3]);
    int arg_r = mp_obj_get_int(arg_vec[4]);

    int arg_c =
        py_helper_keyword_color(arg_img, n_args, args, offset + 1, kw_args, -1); // White.
    int arg_thickness =
        py_helper_keyword_int(n_args, args, offset + 2, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);
    bool arg_fill =
        py_helper_keyword_int(n_args, args, offset + 3, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_fill), false);

    imlib_draw_ellipse(arg_img, arg_cx, arg_cy, arg_rx, arg_ry, arg_r, arg_c, arg_thickness, arg_fill);
    return args[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_ellipse_obj, 2, py_image_draw_ellipse);

static mp_obj_t py_image_draw_string(uint n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    image_t *arg_img = py_helper_arg_to_image(args[0], ARG_IMAGE_MUTABLE);

    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 1, 3, &arg_vec);
    int arg_x_off = mp_obj_get_int(arg_vec[0]);
    int arg_y_off = mp_obj_get_int(arg_vec[1]);
    const char *arg_str = mp_obj_str_get_str(arg_vec[2]);

    int arg_c =
        py_helper_keyword_color(arg_img, n_args, args, offset + 0, kw_args, -1); // White.
    float arg_scale =
        py_helper_keyword_float(n_args, args, offset + 1, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_scale), 1.0);
    PY_ASSERT_TRUE_MSG(0 < arg_scale, "Error: 0 < scale!");
    int arg_x_spacing =
        py_helper_keyword_int(n_args, args, offset + 2, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_x_spacing), 0);
    int arg_y_spacing =
        py_helper_keyword_int(n_args, args, offset + 3, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_y_spacing), 0);
    bool arg_mono_space =
        py_helper_keyword_int(n_args, args, offset + 4, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_mono_space), true);
    int arg_char_rotation =
        py_helper_keyword_int(n_args, args, offset + 5, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_char_rotation), 0);
    int arg_char_hmirror =
        py_helper_keyword_int(n_args, args, offset + 6, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_char_hmirror), false);
    int arg_char_vflip =
        py_helper_keyword_int(n_args, args, offset + 7, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_char_vflip), false);
    int arg_string_rotation =
        py_helper_keyword_int(n_args, args, offset + 8, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_string_rotation), 0);
    int arg_string_hmirror =
        py_helper_keyword_int(n_args, args, offset + 9, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_string_hmirror), false);
    int arg_string_vflip =
        py_helper_keyword_int(n_args, args, offset + 10, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_string_vflip), false);

    imlib_draw_string(arg_img, arg_x_off, arg_y_off, arg_str,
        arg_c, arg_scale, arg_x_spacing, arg_y_spacing, arg_mono_space,
        arg_char_rotation, arg_char_hmirror, arg_char_vflip,
        arg_string_rotation, arg_string_hmirror, arg_string_vflip);
    return args[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_string_obj, 2, py_image_draw_string);

static mp_obj_t py_image_draw_cross(uint n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    image_t *arg_img = py_helper_arg_to_image(args[0], ARG_IMAGE_MUTABLE);

    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 1, 2, &arg_vec);
    int arg_x = mp_obj_get_int(arg_vec[0]);
    int arg_y = mp_obj_get_int(arg_vec[1]);

    int arg_c =
        py_helper_keyword_color(arg_img, n_args, args, offset + 0, kw_args, -1); // White.
    int arg_s =
        py_helper_keyword_int(n_args, args, offset + 1, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_size), 5);
    int arg_thickness =
        py_helper_keyword_int(n_args, args, offset + 2, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);

    imlib_draw_line(arg_img, arg_x - arg_s, arg_y, arg_x + arg_s, arg_y, arg_c, arg_thickness);
    imlib_draw_line(arg_img, arg_x, arg_y - arg_s, arg_x, arg_y + arg_s, arg_c, arg_thickness);
    return args[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_cross_obj, 2, py_image_draw_cross);

static mp_obj_t py_image_draw_arrow(uint n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    image_t *arg_img = py_helper_arg_to_image(args[0], ARG_IMAGE_MUTABLE);

    const mp_obj_t *arg_vec;
    uint offset = py_helper_consume_array(n_args, args, 1, 4, &arg_vec);
    int arg_x0 = mp_obj_get_int(arg_vec[0]);
    int arg_y0 = mp_obj_get_int(arg_vec[1]);
    int arg_x1 = mp_obj_get_int(arg_vec[2]);
    int arg_y1 = mp_obj_get_int(arg_vec[3]);

    int arg_c =
        py_helper_keyword_color(arg_img, n_args, args, offset + 0, kw_args, -1); // White.
    int arg_s =
        py_helper_keyword_int(n_args, args, offset + 1, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_size), 10);
    int arg_thickness =
        py_helper_keyword_int(n_args, args, offset + 2, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);

    int dx = (arg_x1 - arg_x0);
    int dy = (arg_y1 - arg_y0);
    float length = fast_sqrtf((dx * dx) + (dy * dy));

    float ux = IM_DIV(dx, length);
    float uy = IM_DIV(dy, length);
    float vx = -uy;
    float vy = ux;

    int a0x = fast_roundf(arg_x1 - (arg_s * ux) + (arg_s * vx * 0.5));
    int a0y = fast_roundf(arg_y1 - (arg_s * uy) + (arg_s * vy * 0.5));
    int a1x = fast_roundf(arg_x1 - (arg_s * ux) - (arg_s * vx * 0.5));
    int a1y = fast_roundf(arg_y1 - (arg_s * uy) - (arg_s * vy * 0.5));

    imlib_draw_line(arg_img, arg_x0, arg_y0, arg_x1, arg_y1, arg_c, arg_thickness);
    imlib_draw_line(arg_img, arg_x1, arg_y1, a0x, a0y, arg_c, arg_thickness);
    imlib_draw_line(arg_img, arg_x1, arg_y1, a1x, a1y, arg_c, arg_thickness);
    return args[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_arrow_obj, 2, py_image_draw_arrow);

static mp_obj_t py_image_draw_edges(uint n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    image_t *arg_img = py_helper_arg_to_image(args[0], ARG_IMAGE_MUTABLE);

    mp_obj_t *corners, *p0, *p1, *p2, *p3;
    mp_obj_get_array_fixed_n(args[1], 4, &corners);
    mp_obj_get_array_fixed_n(corners[0], 2, &p0);
    mp_obj_get_array_fixed_n(corners[1], 2, &p1);
    mp_obj_get_array_fixed_n(corners[2], 2, &p2);
    mp_obj_get_array_fixed_n(corners[3], 2, &p3);

    int x0, y0, x1, y1, x2, y2, x3, y3;
    x0 = mp_obj_get_int(p0[0]);
    y0 = mp_obj_get_int(p0[1]);
    x1 = mp_obj_get_int(p1[0]);
    y1 = mp_obj_get_int(p1[1]);
    x2 = mp_obj_get_int(p2[0]);
    y2 = mp_obj_get_int(p2[1]);
    x3 = mp_obj_get_int(p3[0]);
    y3 = mp_obj_get_int(p3[1]);

    int arg_c =
        py_helper_keyword_color(arg_img, n_args, args, 2, kw_args, -1); // White.
    int arg_s =
        py_helper_keyword_int(n_args, args, 3, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_size), 0);
    int arg_thickness =
        py_helper_keyword_int(n_args, args, 4, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_thickness), 1);
    bool arg_fill =
        py_helper_keyword_int(n_args, args, 5, kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_fill), false);

    imlib_draw_line(arg_img, x0, y0, x1, y1, arg_c, arg_thickness);
    imlib_draw_line(arg_img, x1, y1, x2, y2, arg_c, arg_thickness);
    imlib_draw_line(arg_img, x2, y2, x3, y3, arg_c, arg_thickness);
    imlib_draw_line(arg_img, x3, y3, x0, y0, arg_c, arg_thickness);

    if (arg_s >= 1) {
        imlib_draw_circle(arg_img, x0, y0, arg_s, arg_c, arg_thickness, arg_fill);
        imlib_draw_circle(arg_img, x1, y1, arg_s, arg_c, arg_thickness, arg_fill);
        imlib_draw_circle(arg_img, x2, y2, arg_s, arg_c, arg_thickness, arg_fill);
        imlib_draw_circle(arg_img, x3, y3, arg_s, arg_c, arg_thickness, arg_fill);
    }

    return args[0];
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_draw_edges_obj, 2, py_image_draw_edges);

// ====================================================================================
// Find Methods
// ====================================================================================

// QRCode Object
#define py_qrcode2_obj_size 10
typedef struct py_qrcode2_obj {
    mp_obj_base_t base;
    mp_obj_t corners;
    mp_obj_t x, y, w, h, payload, version, ecc_level, mask, data_type, eci;
} py_qrcode_obj_t;

static void py_qrcode_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    py_qrcode_obj_t *self = self_in;
    mp_printf(print,
        "{\"x\":%d, \"y\":%d, \"w\":%d, \"h\":%d, \"payload\":\"%s\","
        " \"version\":%d, \"ecc_level\":%d, \"mask\":%d, \"data_type\":%d, \"eci\":%d}",
        mp_obj_get_int(self->x),
        mp_obj_get_int(self->y),
        mp_obj_get_int(self->w),
        mp_obj_get_int(self->h),
        mp_obj_str_get_str(self->payload),
        mp_obj_get_int(self->version),
        mp_obj_get_int(self->ecc_level),
        mp_obj_get_int(self->mask),
        mp_obj_get_int(self->data_type),
        mp_obj_get_int(self->eci));
}

static mp_obj_t py_qrcode_subscr(mp_obj_t self_in, mp_obj_t index, mp_obj_t value) {
    if (value == MP_OBJ_SENTINEL) {
        py_qrcode_obj_t *self = self_in;
        if (MP_OBJ_IS_TYPE(index, &mp_type_slice)) {
            mp_bound_slice_t slice;
            if (!mp_seq_get_fast_slice_indexes(py_qrcode2_obj_size, index, &slice)) {
                mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("only slices with step=1 (aka None) are supported"));
            }
            mp_obj_tuple_t *result = mp_obj_new_tuple(slice.stop - slice.start, NULL);
            mp_seq_copy(result->items, &(self->x) + slice.start, result->len, mp_obj_t);
            return result;
        }
        switch (mp_get_index(self->base.type, py_qrcode2_obj_size, index, false)) {
            case 0:
                return self->x;
            case 1:
                return self->y;
            case 2:
                return self->w;
            case 3:
                return self->h;
            case 4:
                return self->payload;
            case 5:
                return self->version;
            case 6:
                return self->ecc_level;
            case 7:
                return self->mask;
            case 8:
                return self->data_type;
            case 9:
                return self->eci;
        }
    }
    return MP_OBJ_NULL; // op not supported
}

mp_obj_t py_qrcode_corners(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->corners;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_corners_obj, py_qrcode_corners);

mp_obj_t py_qrcode_rect(mp_obj_t self_in) {
    return mp_obj_new_tuple(4, (mp_obj_t []) {((py_qrcode_obj_t *)self_in)->x,
                                              ((py_qrcode_obj_t *)self_in)->y,
                                              ((py_qrcode_obj_t *)self_in)->w,
                                              ((py_qrcode_obj_t *)self_in)->h});
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_rect_obj, py_qrcode_rect);

mp_obj_t py_qrcode_x(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->x;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_x_obj, py_qrcode_x);

mp_obj_t py_qrcode_y(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->y;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_y_obj, py_qrcode_y);

mp_obj_t py_qrcode_w(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->w;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_w_obj, py_qrcode_w);

mp_obj_t py_qrcode_h(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->h;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_h_obj, py_qrcode_h);

mp_obj_t py_qrcode_payload(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->payload;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_payload_obj, py_qrcode_payload);

mp_obj_t py_qrcode_version(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->version;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_version_obj, py_qrcode_version);

mp_obj_t py_qrcode_ecc_level(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->ecc_level;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_ecc_level_obj, py_qrcode_ecc_level);

mp_obj_t py_qrcode_mask(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->mask;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_mask_obj, py_qrcode_mask);

mp_obj_t py_qrcode_data_type(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->data_type;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_data_type_obj, py_qrcode_data_type);

mp_obj_t py_qrcode_eci(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->eci;
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_eci_obj, py_qrcode_eci);

mp_obj_t py_qrcode_is_numeric(mp_obj_t self_in) {
    return mp_obj_new_bool(mp_obj_get_int(((py_qrcode_obj_t *)self_in)->data_type) == 1);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_is_numeric_obj, py_qrcode_is_numeric);

mp_obj_t py_qrcode_is_alphanumeric(mp_obj_t self_in) {
    return mp_obj_new_bool(mp_obj_get_int(((py_qrcode_obj_t *)self_in)->data_type) == 2);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_is_alphanumeric_obj, py_qrcode_is_alphanumeric);

mp_obj_t py_qrcode_is_binary(mp_obj_t self_in) {
    return mp_obj_new_bool(mp_obj_get_int(((py_qrcode_obj_t *)self_in)->data_type) == 4);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_is_binary_obj, py_qrcode_is_binary);

mp_obj_t py_qrcode_is_kanji(mp_obj_t self_in) {
    return mp_obj_new_bool(mp_obj_get_int(((py_qrcode_obj_t *)self_in)->data_type) == 8);
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_is_kanji_obj, py_qrcode_is_kanji);

static const mp_rom_map_elem_t py_qrcode_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_corners),         MP_ROM_PTR(&py_qrcode_corners_obj) },
    { MP_ROM_QSTR(MP_QSTR_rect),            MP_ROM_PTR(&py_qrcode_rect_obj) },
    { MP_ROM_QSTR(MP_QSTR_x),               MP_ROM_PTR(&py_qrcode_x_obj) },
    { MP_ROM_QSTR(MP_QSTR_y),               MP_ROM_PTR(&py_qrcode_y_obj) },
    { MP_ROM_QSTR(MP_QSTR_w),               MP_ROM_PTR(&py_qrcode_w_obj) },
    { MP_ROM_QSTR(MP_QSTR_h),               MP_ROM_PTR(&py_qrcode_h_obj) },
    { MP_ROM_QSTR(MP_QSTR_payload),         MP_ROM_PTR(&py_qrcode_payload_obj) },
    { MP_ROM_QSTR(MP_QSTR_version),         MP_ROM_PTR(&py_qrcode_version_obj) },
    { MP_ROM_QSTR(MP_QSTR_ecc_level),       MP_ROM_PTR(&py_qrcode_ecc_level_obj) },
    { MP_ROM_QSTR(MP_QSTR_mask),            MP_ROM_PTR(&py_qrcode_mask_obj) },
    { MP_ROM_QSTR(MP_QSTR_data_type),       MP_ROM_PTR(&py_qrcode_data_type_obj) },
    { MP_ROM_QSTR(MP_QSTR_eci),             MP_ROM_PTR(&py_qrcode_eci_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_numeric),      MP_ROM_PTR(&py_qrcode_is_numeric_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_alphanumeric), MP_ROM_PTR(&py_qrcode_is_alphanumeric_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_binary),       MP_ROM_PTR(&py_qrcode_is_binary_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_kanji),        MP_ROM_PTR(&py_qrcode_is_kanji_obj) }
};

static MP_DEFINE_CONST_DICT(py_qrcode_locals_dict, py_qrcode_locals_dict_table);

static MP_DEFINE_CONST_OBJ_TYPE(
    py_qrcode_type,
    MP_QSTR_qrcode,
    MP_TYPE_FLAG_NONE,
    print, py_qrcode_print,
    subscr, py_qrcode_subscr,
    locals_dict, &py_qrcode_locals_dict
    );


typedef union {
    uint16_t val;
    struct {
        uint16_t b : 5;
        uint16_t g : 6;
        uint16_t r : 5;
    };
} rgb565_t;

static uint8_t rgb565_to_grayscale(const uint8_t *img) {
    uint16_t *img_16 = (uint16_t *)img;
    rgb565_t rgb = {.val = __builtin_bswap16(*img_16)};
    uint16_t val = (rgb.r * 8 + rgb.g * 4 + rgb.b * 8) / 3;
    return (uint8_t)MIN(255, val);
}

static void rgb565_to_grayscale_buf(const uint8_t *src, uint8_t *dst, int qr_width, int qr_height) {
    for (size_t y = 0; y < qr_height; y++) {
        for (size_t x = 0; x < qr_width; x++) {
            dst[y * qr_width + x] = rgb565_to_grayscale(&src[(y * qr_width + x) * 2]);
        }
    }
}

static struct quirc *qr_decoder;
struct quirc_code code = {};
struct quirc_data qr_data = {};
static mp_obj_t py_image_find_qrcodes(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    image_t *img = py_image_cobj(args[0]);

    qr_decoder = quirc_new();
    if (!qr_decoder) {
        return mp_const_none;
    }

    if (quirc_resize(qr_decoder, img->w, img->h) < 0) {
        return mp_const_none;
    }

    uint8_t *qr_buf = quirc_begin(qr_decoder, NULL, NULL);

    // Convert the frame to grayscale. We could have asked the camera for a grayscale frame,
    // but then the image on the display would be grayscale too.
    rgb565_to_grayscale_buf(img->data, qr_buf, img->w, img->h);

    // Process the frame. This step find the corners of the QR code (capstones)
    quirc_end(qr_decoder);

    int count = quirc_count(qr_decoder);
    quirc_decode_error_t err = QUIRC_ERROR_DATA_UNDERFLOW;

    mp_obj_list_t *objects_list = mp_obj_new_list(count, NULL);
    for (size_t i = 0; i < count; i++) {
        // Extract raw QR code binary data (values of black/white modules)
        quirc_extract(qr_decoder, i, &code);

        // Decode the raw data. This step also performs error correction.
        err = quirc_decode(&code, &qr_data);
        if (err == QUIRC_ERROR_DATA_ECC) {
            quirc_flip(&code);
            err = quirc_decode(&code, &qr_data);
        }
        if (err != 0) {
            continue;
        }

        py_qrcode_obj_t *o = m_new_obj(py_qrcode_obj_t);
        o->base.type = &py_qrcode_type;
        o->corners = mp_obj_new_tuple(4, (mp_obj_t []) {
            mp_obj_new_tuple(2, (mp_obj_t []) { mp_obj_new_int(code.corners[0].x), mp_obj_new_int(code.corners[0].y) }),
            mp_obj_new_tuple(2, (mp_obj_t []) { mp_obj_new_int(code.corners[1].x), mp_obj_new_int(code.corners[1].y) }),
            mp_obj_new_tuple(2, (mp_obj_t []) { mp_obj_new_int(code.corners[2].x), mp_obj_new_int(code.corners[2].y) }),
            mp_obj_new_tuple(2, (mp_obj_t []) { mp_obj_new_int(code.corners[3].x), mp_obj_new_int(code.corners[3].y) })
        });
        int min_x = code.corners[0].x;
        int min_y = code.corners[0].y;
        int max_x = code.corners[0].x;
        int max_y = code.corners[0].y;
        for (int i = 1; i < 4; i++) {
            if (code.corners[i].x < min_x) {
                min_x = code.corners[i].x;
            }
            if (code.corners[i].y < min_y) {
                min_y = code.corners[i].y;
            }
            if (code.corners[i].x > max_x) {
                max_x = code.corners[i].x;
            }
            if (code.corners[i].y > max_y) {
                max_y = code.corners[i].y;
            }
        }
        o->x = mp_obj_new_int(min_x);
        o->y = mp_obj_new_int(min_y);
        o->w = mp_obj_new_int(max_x - min_x + 1);
        o->h = mp_obj_new_int(max_y - min_y + 1);
        o->payload = mp_obj_new_str((const char *)qr_data.payload, strlen((const char *)qr_data.payload));
        o->version = mp_obj_new_int(qr_data.version);
        o->ecc_level = mp_obj_new_int(qr_data.ecc_level);
        o->mask = mp_obj_new_int(qr_data.mask);
        o->data_type = mp_obj_new_int(qr_data.data_type);
        o->eci = mp_obj_new_int(qr_data.eci);
        objects_list->items[i] = o;
    }

    quirc_destroy(qr_decoder);

    return objects_list;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(py_image_find_qrcodes_obj, 1, py_image_find_qrcodes);

mp_obj_t py_image(int w, int h, omv_pixformat_t pixfmt, uint32_t size, void *pixels) {
    py_image_obj_t *o = m_new_obj(py_image_obj_t);
    o->base.type = &py_image_type;
    o->_cobj.w = w;
    o->_cobj.h = h;
    o->_cobj.size = size;
    o->_cobj.pixfmt = pixfmt;
    o->_cobj.pixels = pixels;
    return o;
}

mp_obj_t py_image_from_struct(image_t *img) {
    py_image_obj_t *o = m_new_obj(py_image_obj_t);
    o->base.type = &py_image_type;
    o->_cobj = *img;
    return o;
}

static const mp_rom_map_elem_t locals_dict_table[] = {
    /* Basic Methods */
    {MP_ROM_QSTR(MP_QSTR_width),          MP_ROM_PTR(&py_image_width_obj)},
    {MP_ROM_QSTR(MP_QSTR_height),         MP_ROM_PTR(&py_image_height_obj)},
    {MP_ROM_QSTR(MP_QSTR_format),         MP_ROM_PTR(&py_image_format_obj)},
    {MP_ROM_QSTR(MP_QSTR_size),           MP_ROM_PTR(&py_image_size_obj)},
    {MP_ROM_QSTR(MP_QSTR_bytearray),      MP_ROM_PTR(&py_image_bytearray_obj)},
    /* Drawing Methods */
    {MP_ROM_QSTR(MP_QSTR_clear),          MP_ROM_PTR(&py_image_clear_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_line),      MP_ROM_PTR(&py_image_draw_line_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_rectangle), MP_ROM_PTR(&py_image_draw_rectangle_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_circle),    MP_ROM_PTR(&py_image_draw_circle_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_ellipse),   MP_ROM_PTR(&py_image_draw_ellipse_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_string),    MP_ROM_PTR(&py_image_draw_string_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_cross),     MP_ROM_PTR(&py_image_draw_cross_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_arrow),     MP_ROM_PTR(&py_image_draw_arrow_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_edges),     MP_ROM_PTR(&py_image_draw_edges_obj)},
    /* Find Methods */
    {MP_ROM_QSTR(MP_QSTR_find_qrcodes),   MP_ROM_PTR(&py_image_find_qrcodes_obj)},
};

static MP_DEFINE_CONST_DICT(py_image_locals_dict, locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    py_image_type,
    MP_QSTR_Image,
    MP_TYPE_FLAG_NONE,
    locals_dict, &py_image_locals_dict
    );

// ==================================================================================
// module: image
// ==================================================================================
static const mp_rom_map_elem_t globals_dict_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__),  MP_OBJ_NEW_QSTR(MP_QSTR_image)},
    // Pixel formats
    {MP_ROM_QSTR(MP_QSTR_GRAYSCALE), MP_ROM_INT(OMV_PIXFORMAT_GRAYSCALE)},/* 1BPP/GRAYSCALE*/
    {MP_ROM_QSTR(MP_QSTR_RGB565),    MP_ROM_INT(OMV_PIXFORMAT_RGB565)},   /* 2BPP/RGB565*/
    {MP_ROM_QSTR(MP_QSTR_YUV422),    MP_ROM_INT(OMV_PIXFORMAT_YUV422)},   /* 2BPP/YUV422*/
    {MP_ROM_QSTR(MP_QSTR_JPEG),      MP_ROM_INT(OMV_PIXFORMAT_JPEG)},     /* JPEG/COMPRESSED*/
    //
    {MP_ROM_QSTR(MP_QSTR_Image),     MP_ROM_PTR(&py_image_type)},
};

static MP_DEFINE_CONST_DICT(globals_dict, globals_dict_table);

const mp_obj_module_t image_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_t)&globals_dict
};

MP_REGISTER_MODULE(MP_QSTR_image, image_module);
