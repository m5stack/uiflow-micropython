/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

// -------- Power wrapper
// power port mask
static const mp_rom_map_elem_t power_port_masks_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_A),   MP_ROM_INT(0b00000001) },
    { MP_ROM_QSTR(MP_QSTR_B1),  MP_ROM_INT(0b00000010) },
    { MP_ROM_QSTR(MP_QSTR_B2),  MP_ROM_INT(0b00000100) },
    { MP_ROM_QSTR(MP_QSTR_C1),  MP_ROM_INT(0b00001000) },
    { MP_ROM_QSTR(MP_QSTR_C2),  MP_ROM_INT(0b00010000) },
    { MP_ROM_QSTR(MP_QSTR_USB), MP_ROM_INT(0b00100000) },
    { MP_ROM_QSTR(MP_QSTR_MAIN), MP_ROM_INT(0b10000000) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(power_port_masks, power_port_masks_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_power_port_mask_enum,
    MP_QSTR_PORT,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&power_port_masks
    );
#else
const mp_obj_type_t mp_power_port_mask_enum = {
    .base = { &mp_type_type },
    .name = MP_QSTR_PORT,
    .locals_dict = (mp_obj_dict_t *)&power_port_masks,
};
#endif

MAKE_METHOD_KW(power, setExtOutput, 1);
MAKE_METHOD_0(power, getExtOutput);
MAKE_METHOD_KW(power, setUsbOutput, 1);
MAKE_METHOD_0(power, getUsbOutput);
MAKE_METHOD_KW(power, setLed, 1);
MAKE_METHOD_0(power, powerOff);
MAKE_METHOD_V(power, timerSleep, 2, 5);
MAKE_METHOD_KW(power, deepSleep, 1);
MAKE_METHOD_KW(power, lightSleep, 1);
MAKE_METHOD_0(power, getBatteryLevel);
MAKE_METHOD_KW(power, setBatteryCharge, 1);
MAKE_METHOD_KW(power, setChargeCurrent, 1);
MAKE_METHOD_1(power, setChargeVoltage);
MAKE_METHOD_0(power, isCharging);
MAKE_METHOD_0(power, getBatteryVoltage);
MAKE_METHOD_0(power, getBatteryCurrent);
MAKE_METHOD_0(power, getKeyState);
MAKE_METHOD_1(power, setVibration);
MAKE_METHOD_0(power, getType);
MAKE_METHOD_1(power, getPortVbus);
MAKE_METHOD_1(power, getPortCurrent);

static const mp_rom_map_elem_t power_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR_PORT),        MP_ROM_PTR(&mp_power_port_mask_enum) },
    // control functions
    MAKE_TABLE(power, setExtOutput),
    MAKE_TABLE(power, getExtOutput),
    MAKE_TABLE(power, setUsbOutput),
    MAKE_TABLE(power, getUsbOutput),
    MAKE_TABLE(power, setLed),
    MAKE_TABLE(power, powerOff),
    MAKE_TABLE(power, timerSleep),
    MAKE_TABLE(power, deepSleep),
    MAKE_TABLE(power, lightSleep),
    MAKE_TABLE(power, getBatteryLevel),
    MAKE_TABLE(power, setBatteryCharge),
    MAKE_TABLE(power, setChargeCurrent),
    MAKE_TABLE(power, setChargeVoltage),
    MAKE_TABLE(power, isCharging),
    MAKE_TABLE(power, getBatteryVoltage),
    MAKE_TABLE(power, getBatteryCurrent),
    MAKE_TABLE(power, getKeyState),
    MAKE_TABLE(power, setVibration),
    MAKE_TABLE(power, getType),
    MAKE_TABLE(power, getPortVbus),
    MAKE_TABLE(power, getPortCurrent),
};

static MP_DEFINE_CONST_DICT(power_member, power_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_power_type,
    MP_QSTR_Power,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&power_member
    );
#else
const mp_obj_type_t mp_power_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Power,
    .locals_dict = (mp_obj_dict_t *)&power_member,
};
#endif
