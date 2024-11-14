/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"


// board type
static const mp_rom_map_elem_t m5_board_member_table[] = {
    /* *FORMAT-OFF* */
    // with display boards
    { MP_ROM_QSTR(MP_QSTR_unknown),                  MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_SEEED_XIAO_ESP32S3),       MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_ESPRESSIF_ESP32_S3_BOX_3), MP_ROM_INT(2) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(m5_board_member, m5_board_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    m5_board_type,
    MP_QSTR_BOARD,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&m5_board_member
    );
#else
const mp_obj_type_t m5_board_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_BOARD,
    .locals_dict = (mp_obj_dict_t *)&m5_board_member,
};
#endif


// -------- M5 wrapper
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(m5_begin_obj, 0, 1, m5_begin);
static MP_DEFINE_CONST_FUN_OBJ_0(m5_update_obj, m5_update);
static MP_DEFINE_CONST_FUN_OBJ_0(m5_end_obj, m5_end);
static MP_DEFINE_CONST_FUN_OBJ_0(m5_getBoard_obj, m5_getBoard);


static const mp_rom_map_elem_t mp_module_m5_globals_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR___name__),          MP_ROM_QSTR(MP_QSTR_M5) },
    { MP_ROM_QSTR(MP_QSTR_BOARD),             MP_ROM_PTR(&m5_board_type) },
    { MP_ROM_QSTR(MP_QSTR_Lcd),               MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_Display),           MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_Touch),             MP_OBJ_FROM_PTR(&m5_touch) },
    { MP_ROM_QSTR(MP_QSTR_Widgets),           MP_OBJ_FROM_PTR(&m5_widgets) },

    { MP_ROM_QSTR(MP_QSTR_begin),             MP_ROM_PTR(&m5_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_update),            MP_ROM_PTR(&m5_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_end),               MP_ROM_PTR(&m5_end_obj) },
    { MP_ROM_QSTR(MP_QSTR_getBoard),          MP_ROM_PTR(&m5_getBoard_obj) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(mp_module_m5_globals, mp_module_m5_globals_table);

// Define module object.
const mp_obj_module_t mp_module_m5 = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_m5_globals,
};

MP_REGISTER_MODULE(MP_QSTR_M5, mp_module_m5);
