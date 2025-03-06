/*
 * SPDX-License-Identifier: MIT
 *
 * Copyright (C) 2013-2024 OpenMV, LLC.
 * Copyright (c) 2024 M5Stack Technology CO LTD
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
    {MP_ROM_QSTR(MP_QSTR_width),               MP_ROM_PTR(&py_image_width_obj)},
    {MP_ROM_QSTR(MP_QSTR_height),              MP_ROM_PTR(&py_image_height_obj)},
    {MP_ROM_QSTR(MP_QSTR_format),              MP_ROM_PTR(&py_image_format_obj)},
    {MP_ROM_QSTR(MP_QSTR_size),                MP_ROM_PTR(&py_image_size_obj)},
    {MP_ROM_QSTR(MP_QSTR_bytearray),           MP_ROM_PTR(&py_image_bytearray_obj)},
    /* Drawing Methods */
    {MP_ROM_QSTR(MP_QSTR_clear),               MP_ROM_PTR(&py_image_clear_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_line),           MP_ROM_PTR(&py_image_draw_line_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_rectangle),      MP_ROM_PTR(&py_image_draw_rectangle_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_circle),         MP_ROM_PTR(&py_image_draw_circle_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_ellipse),        MP_ROM_PTR(&py_image_draw_ellipse_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_string),         MP_ROM_PTR(&py_image_draw_string_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_cross),          MP_ROM_PTR(&py_image_draw_cross_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_arrow),          MP_ROM_PTR(&py_image_draw_arrow_obj)},
    {MP_ROM_QSTR(MP_QSTR_draw_edges),          MP_ROM_PTR(&py_image_draw_edges_obj)},
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
