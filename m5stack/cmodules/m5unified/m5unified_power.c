#include "m5unified.h"

// -------- Power wrapper
// power port mask
STATIC const mp_rom_map_elem_t power_port_masks_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_A),   MP_ROM_INT(0b00000001) },
    { MP_ROM_QSTR(MP_QSTR_B1),  MP_ROM_INT(0b00000010) },
    { MP_ROM_QSTR(MP_QSTR_B2),  MP_ROM_INT(0b00000100) },
    { MP_ROM_QSTR(MP_QSTR_C1),  MP_ROM_INT(0b00001000) },
    { MP_ROM_QSTR(MP_QSTR_C2),  MP_ROM_INT(0b00010000) },
    { MP_ROM_QSTR(MP_QSTR_USB), MP_ROM_INT(0b00100000) },
    { MP_ROM_QSTR(MP_QSTR_HAT), MP_ROM_INT(0b01000000) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(power_port_masks, power_port_masks_table);

const mp_obj_type_t mp_power_port_mask_enum = {
    .base = { &mp_type_type },
    .name = MP_QSTR_PORT,
    .locals_dict = (mp_obj_dict_t *)&power_port_masks,
};

MAKE_METHOD_KW(power, setExtPower, 1);
MAKE_METHOD_KW(power, setLed, 1);
MAKE_METHOD_0(power, powerOff);

STATIC const mp_rom_map_elem_t power_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR_PORT),        MP_ROM_PTR(&mp_power_port_mask_enum) },
    // control functions
    MAKE_TABLE(power, setExtPower),
    MAKE_TABLE(power, setLed),
    MAKE_TABLE(power, powerOff),
};

STATIC MP_DEFINE_CONST_DICT(power_member, power_member_table);

const mp_obj_type_t mp_power_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Power,
    .locals_dict = (mp_obj_dict_t *)&power_member,
};
