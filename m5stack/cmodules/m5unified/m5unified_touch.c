#include "m5unified.h"

// -------- Touch wrapper
MAKE_METHOD_0(touch, getX);
MAKE_METHOD_0(touch, getY);
MAKE_METHOD_0(touch, getCount);
MAKE_METHOD_KW(touch, getTouchPointRaw, 1);

STATIC const mp_rom_map_elem_t touch_member_table[] = {
    MAKE_TABLE(touch, getX),
    MAKE_TABLE(touch, getY),
    MAKE_TABLE(touch, getCount),
    MAKE_TABLE(touch, getTouchPointRaw),
};
STATIC MP_DEFINE_CONST_DICT(touch_member, touch_member_table);

const mp_obj_type_t mp_touch_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Touch,
    .locals_dict = (mp_obj_dict_t *)&touch_member,
};
