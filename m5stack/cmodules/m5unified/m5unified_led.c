/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

// -------- Led wrapper
MAKE_METHOD_0(led, display);
MAKE_METHOD_0(led, getCount);
MAKE_METHOD_KW(led, setBrightness, 1);
MAKE_METHOD_V(led, setAllColor, 1, 3);
MAKE_METHOD_V(led, setColor, 2, 4);

static const mp_rom_map_elem_t led_member_table[] = {
    // control functions
    MAKE_TABLE(led, display),
    MAKE_TABLE(led, getCount),
    MAKE_TABLE(led, setBrightness),
    MAKE_TABLE(led, setAllColor),
    MAKE_TABLE(led, setColor),
};

static MP_DEFINE_CONST_DICT(led_member, led_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_led_type,
    MP_QSTR_Led,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&led_member
    );
#else
const mp_obj_type_t mp_led_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Led,
    .locals_dict = (mp_obj_dict_t *)&led_member,
};
#endif
