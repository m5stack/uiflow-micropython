#include "m5unified.h"

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
MAKE_METHOD_1(btn, pressedFor);
MAKE_METHOD_1(btn, releasedFor);
MAKE_METHOD_1(btn, setDebounceThresh);
MAKE_METHOD_1(btn, setHoldThresh);
MAKE_METHOD_1(btn, wasSingleClicked);
MAKE_METHOD_1(btn, wasDoubleClicked);
MAKE_METHOD_1(btn, wasDeciedClickCount);
MAKE_METHOD_1(btn, getClickCount);

STATIC const mp_rom_map_elem_t btn_member_table[] = {
    MAKE_TABLE(btn, isHolding),
    MAKE_TABLE(btn, isPressed),
    MAKE_TABLE(btn, isReleased),
    MAKE_TABLE(btn, wasChangePressed),
    MAKE_TABLE(btn, wasClicked),
    MAKE_TABLE(btn, wasHold),
    MAKE_TABLE(btn, wasPressed),
    MAKE_TABLE(btn, wasReleased),
    MAKE_TABLE(btn, lastChange),
    MAKE_TABLE(btn, pressedFor),
    MAKE_TABLE(btn, releasedFor),
    MAKE_TABLE(btn, setDebounceThresh),
    MAKE_TABLE(btn, setHoldThresh),
    MAKE_TABLE(btn, wasSingleClicked),
    MAKE_TABLE(btn, wasDoubleClicked),
    MAKE_TABLE(btn, wasDeciedClickCount),
    MAKE_TABLE(btn, getClickCount),
};
STATIC MP_DEFINE_CONST_DICT(btn_member, btn_member_table);

const mp_obj_type_t mp_btn_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Button,
    .locals_dict = (mp_obj_dict_t *)&btn_member,
};
