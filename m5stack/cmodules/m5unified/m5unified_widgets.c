/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

// -------- M5Widgets Label
MAKE_METHOD_KW(m5widgets_label, setText, 1);
MAKE_METHOD_KW(m5widgets_label, setColor, 1);
MAKE_METHOD_KW(m5widgets_label, setCursor, 1);
MAKE_METHOD_KW(m5widgets_label, setSize, 1);
MAKE_METHOD_KW(m5widgets_label, setFont, 1);
MAKE_METHOD_KW(m5widgets_label, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_label_member_table[] = {
    MAKE_TABLE(m5widgets_label, setText),
    MAKE_TABLE(m5widgets_label, setColor),
    MAKE_TABLE(m5widgets_label, setCursor),
    MAKE_TABLE(m5widgets_label, setSize),
    MAKE_TABLE(m5widgets_label, setFont),
    MAKE_TABLE(m5widgets_label, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_label_member, m5widgets_label_member_table);
extern mp_obj_t m5widgets_label_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_label_type,
    MP_QSTR_Label,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_label_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_label_member
    );
#else
const mp_obj_type_t mp_widgets_label_type = {
    { &mp_type_type },
    .name = MP_QSTR_Label,
    .make_new = m5widgets_label_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_label_member,
};
#endif

// -------- M5Widgets Title
MAKE_METHOD_KW(m5widgets_title, setText, 1);
MAKE_METHOD_KW(m5widgets_title, setColor, 1);
MAKE_METHOD_KW(m5widgets_title, setSize, 1);
MAKE_METHOD_KW(m5widgets_title, setTextCursor, 1);
MAKE_METHOD_KW(m5widgets_title, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_title_member_table[] = {
    MAKE_TABLE(m5widgets_title, setText),
    MAKE_TABLE(m5widgets_title, setColor),
    MAKE_TABLE(m5widgets_title, setSize),
    MAKE_TABLE(m5widgets_title, setTextCursor),
    MAKE_TABLE(m5widgets_title, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_title_member, m5widgets_title_member_table);
extern mp_obj_t m5widgets_title_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_title_type,
    MP_QSTR_Label,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_title_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_title_member
    );
#else
const mp_obj_type_t mp_widgets_title_type = {
    { &mp_type_type },
    .name = MP_QSTR_Label,
    .make_new = m5widgets_title_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_title_member,
};
#endif

// -------- M5Widgets Image
MAKE_METHOD_KW(m5widgets_image, setImage, 1);
MAKE_METHOD_KW(m5widgets_image, setCursor, 1);
MAKE_METHOD_KW(m5widgets_image, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_image_member_table[] = {
    MAKE_TABLE(m5widgets_image, setImage),
    MAKE_TABLE(m5widgets_image, setCursor),
    MAKE_TABLE(m5widgets_image, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_image_member, m5widgets_image_member_table);
extern mp_obj_t m5widgets_image_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_image_type,
    MP_QSTR_Image,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_image_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_image_member
    );
#else
const mp_obj_type_t mp_widgets_image_type = {
    { &mp_type_type },
    .name = MP_QSTR_Image,
    .make_new = m5widgets_image_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_image_member,
};
#endif

// -------- M5Widgets Line
MAKE_METHOD_KW(m5widgets_line, setColor, 1);
MAKE_METHOD_KW(m5widgets_line, setPoints, 1);
MAKE_METHOD_KW(m5widgets_line, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_line_member_table[] = {
    MAKE_TABLE(m5widgets_line, setColor),
    MAKE_TABLE(m5widgets_line, setPoints),
    MAKE_TABLE(m5widgets_line, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_line_member, m5widgets_line_member_table);
extern mp_obj_t m5widgets_line_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_line_type,
    MP_QSTR_Line,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_line_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_line_member
    );
#else
const mp_obj_type_t mp_widgets_line_type = {
    { &mp_type_type },
    .name = MP_QSTR_Line,
    .make_new = m5widgets_line_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_line_member,
};
#endif

// -------- M5Widgets Circle
MAKE_METHOD_KW(m5widgets_circle, setRadius, 1);
MAKE_METHOD_KW(m5widgets_circle, setCursor, 1);
MAKE_METHOD_KW(m5widgets_circle, setColor, 1);
MAKE_METHOD_KW(m5widgets_circle, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_circle_member_table[] = {
    MAKE_TABLE(m5widgets_circle, setRadius),
    MAKE_TABLE(m5widgets_circle, setCursor),
    MAKE_TABLE(m5widgets_circle, setColor),
    MAKE_TABLE(m5widgets_circle, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_circle_member, m5widgets_circle_member_table);
extern mp_obj_t m5widgets_circle_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_circle_type,
    MP_QSTR_Circle,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_circle_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_circle_member
    );
#else
const mp_obj_type_t mp_widgets_circle_type = {
    { &mp_type_type },
    .name = MP_QSTR_Circle,
    .make_new = m5widgets_circle_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_circle_member,
};
#endif

// -------- M5Widgets Rectangle
MAKE_METHOD_KW(m5widgets_rectangle, setSize, 1);
MAKE_METHOD_KW(m5widgets_rectangle, setColor, 1);
MAKE_METHOD_KW(m5widgets_rectangle, setCursor, 1);
MAKE_METHOD_KW(m5widgets_rectangle, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_rectangle_member_table[] = {
    MAKE_TABLE(m5widgets_rectangle, setSize),
    MAKE_TABLE(m5widgets_rectangle, setColor),
    MAKE_TABLE(m5widgets_rectangle, setCursor),
    MAKE_TABLE(m5widgets_rectangle, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_rectangle_member, m5widgets_rectangle_member_table);
extern mp_obj_t m5widgets_rectangle_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_rectangle_type,
    MP_QSTR_Rectangle,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_rectangle_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_rectangle_member
    );
#else
const mp_obj_type_t mp_widgets_rectangle_type = {
    { &mp_type_type },
    .name = MP_QSTR_Rectangle,
    .make_new = m5widgets_rectangle_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_rectangle_member,
};
#endif

// -------- M5Widgets Triangle
MAKE_METHOD_KW(m5widgets_triangle, setColor, 1);
MAKE_METHOD_KW(m5widgets_triangle, setPoints, 1);
MAKE_METHOD_KW(m5widgets_triangle, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_triangle_member_table[] = {
    MAKE_TABLE(m5widgets_triangle, setColor),
    MAKE_TABLE(m5widgets_triangle, setPoints),
    MAKE_TABLE(m5widgets_triangle, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_triangle_member, m5widgets_triangle_member_table);
extern mp_obj_t m5widgets_triangle_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_triangle_type,
    MP_QSTR_Triangle,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_triangle_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_triangle_member
    );
#else
const mp_obj_type_t mp_widgets_triangle_type = {
    { &mp_type_type },
    .name = MP_QSTR_Triangle,
    .make_new = m5widgets_triangle_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_triangle_member,
};
#endif

// -------- M5Widgets QRCode
MAKE_METHOD_KW(m5widgets_qrcode, setText, 1);
MAKE_METHOD_KW(m5widgets_qrcode, setVersion, 1);
MAKE_METHOD_KW(m5widgets_qrcode, setSize, 1);
MAKE_METHOD_KW(m5widgets_qrcode, setCursor, 1);
MAKE_METHOD_KW(m5widgets_qrcode, setVisible, 1);
STATIC const mp_rom_map_elem_t m5widgets_qrcode_member_table[] = {
    MAKE_TABLE(m5widgets_qrcode, setText),
    MAKE_TABLE(m5widgets_qrcode, setVersion),
    MAKE_TABLE(m5widgets_qrcode, setSize),
    MAKE_TABLE(m5widgets_qrcode, setCursor),
    MAKE_TABLE(m5widgets_qrcode, setVisible)
};
STATIC MP_DEFINE_CONST_DICT(m5widgets_qrcode_member, m5widgets_qrcode_member_table);
extern mp_obj_t m5widgets_qrcode_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_widgets_qrcode_type,
    MP_QSTR_QRCode,
    MP_TYPE_FLAG_NONE,
    make_new, m5widgets_qrcode_make_new,
    locals_dict, (mp_obj_dict_t *)&m5widgets_qrcode_member
    );
#else
const mp_obj_type_t mp_widgets_qrcode_type = {
    { &mp_type_type },
    .name = MP_QSTR_QRCode,
    .make_new = m5widgets_qrcode_make_new,
    .locals_dict = (mp_obj_dict_t *)&m5widgets_qrcode_member,
};
#endif

// -------- M5Widgets common funciton
MAKE_METHOD_KW(m5widgets, fillScreen, 1);
MAKE_METHOD_KW(m5widgets, setRotation, 1);
MAKE_METHOD_KW(m5widgets, setBrightness, 1);
STATIC const mp_rom_map_elem_t widgets_module_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__),  MP_ROM_QSTR(MP_QSTR_Widgets) },
    // common funciton
    MAKE_TABLE(m5widgets, fillScreen),
    MAKE_TABLE(m5widgets, setRotation),
    MAKE_TABLE(m5widgets, setBrightness),
    // fonts
    { MP_ROM_QSTR(MP_QSTR_FONTS),     MP_OBJ_FROM_PTR(&mp_fonts_type) },
    // colors
    { MP_ROM_QSTR(MP_QSTR_COLOR),     MP_OBJ_FROM_PTR(&mp_color_type) },
    // widgets objects
    { MP_ROM_QSTR(MP_QSTR_Label),     MP_OBJ_FROM_PTR(&mp_widgets_label_type) },
    { MP_ROM_QSTR(MP_QSTR_Title),     MP_OBJ_FROM_PTR(&mp_widgets_title_type) },
    { MP_ROM_QSTR(MP_QSTR_Image),     MP_OBJ_FROM_PTR(&mp_widgets_image_type) },
    { MP_ROM_QSTR(MP_QSTR_Line),      MP_OBJ_FROM_PTR(&mp_widgets_line_type) },
    { MP_ROM_QSTR(MP_QSTR_Circle),    MP_OBJ_FROM_PTR(&mp_widgets_circle_type) },
    { MP_ROM_QSTR(MP_QSTR_Triangle),  MP_OBJ_FROM_PTR(&mp_widgets_triangle_type) },
    { MP_ROM_QSTR(MP_QSTR_Rectangle), MP_OBJ_FROM_PTR(&mp_widgets_rectangle_type) },
    { MP_ROM_QSTR(MP_QSTR_QRCode),    MP_OBJ_FROM_PTR(&mp_widgets_qrcode_type) }
};
STATIC MP_DEFINE_CONST_DICT(widgets_module_member, widgets_module_member_table);
const mp_obj_module_t m5_widgets = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&widgets_module_member,
};
