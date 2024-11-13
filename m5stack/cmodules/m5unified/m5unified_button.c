/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

static const mp_rom_map_elem_t btn_callback_types_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_WAS_CLICKED),       MP_ROM_INT(BTN_TYPE_WAS_CLICKED) },
    { MP_ROM_QSTR(MP_QSTR_WAS_DOUBLECLICKED), MP_ROM_INT(BTN_TYPE_WAS_DOUBLECLICKED) },
    { MP_ROM_QSTR(MP_QSTR_WAS_HOLD),          MP_ROM_INT(BTN_TYPE_WAS_HOLD) },
    { MP_ROM_QSTR(MP_QSTR_WAS_PRESSED),       MP_ROM_INT(BTN_TYPE_WAS_PRESSED) },
    { MP_ROM_QSTR(MP_QSTR_WAS_RELEASED),      MP_ROM_INT(BTN_TYPE_WAS_RELEASED) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(btn_callback_types, btn_callback_types_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_btn_cb_type,
    MP_QSTR_Callback_Type,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&btn_callback_types
    );
#else
const mp_obj_type_t mp_btn_cb_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Callback_Type,
    .locals_dict = (mp_obj_dict_t *)&btn_callback_types,
};
#endif

// -------- Button wrapper
MAKE_METHOD_0(btn, isHolding);
MAKE_METHOD_0(btn, isPressed);
MAKE_METHOD_0(btn, isReleased);
MAKE_METHOD_0(btn, wasChangePressed);
MAKE_METHOD_0(btn, wasClicked);
MAKE_METHOD_0(btn, wasHold);
MAKE_METHOD_0(btn, wasPressed);
MAKE_METHOD_0(btn, wasReleased);
MAKE_METHOD_0(btn, lastChange);
MAKE_METHOD_0(btn, wasSingleClicked);
MAKE_METHOD_0(btn, wasDoubleClicked);
MAKE_METHOD_0(btn, wasDeciedClickCount);
MAKE_METHOD_0(btn, getClickCount);
MAKE_METHOD_1(btn, pressedFor);
MAKE_METHOD_1(btn, releasedFor);
MAKE_METHOD_1(btn, setDebounceThresh);
MAKE_METHOD_1(btn, setHoldThresh);
MAKE_METHOD_KW(btn, setCallback, 1);
MAKE_METHOD_KW(btn, removeCallback, 1);

static const mp_rom_map_elem_t btn_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR_CB_TYPE), MP_ROM_PTR(&mp_btn_cb_type) },
    MAKE_TABLE(btn, isHolding),
    MAKE_TABLE(btn, isPressed),
    MAKE_TABLE(btn, isReleased),
    MAKE_TABLE(btn, wasChangePressed),
    MAKE_TABLE(btn, wasClicked),
    MAKE_TABLE(btn, wasHold),
    MAKE_TABLE(btn, wasPressed),
    MAKE_TABLE(btn, wasReleased),
    MAKE_TABLE(btn, lastChange),
    MAKE_TABLE(btn, wasSingleClicked),
    MAKE_TABLE(btn, wasDoubleClicked),
    MAKE_TABLE(btn, wasDeciedClickCount),
    MAKE_TABLE(btn, getClickCount),
    MAKE_TABLE(btn, pressedFor),
    MAKE_TABLE(btn, releasedFor),
    MAKE_TABLE(btn, setDebounceThresh),
    MAKE_TABLE(btn, setHoldThresh),
    MAKE_TABLE(btn, setCallback),
    MAKE_TABLE(btn, removeCallback),
};
static MP_DEFINE_CONST_DICT(btn_member, btn_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_btn_type,
    MP_QSTR_Button,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&btn_member
    );
#else
const mp_obj_type_t mp_btn_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Button,
    .locals_dict = (mp_obj_dict_t *)&btn_member,
};
#endif
