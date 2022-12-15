#include "m5unified.h"

// -------- Speaker wrapper
MAKE_METHOD_0(spk, getVolume);
MAKE_METHOD_1(spk, getChannelVolume);
MAKE_METHOD_KW(spk, setVolume, 1);
MAKE_METHOD_KW(spk, setChannelVolume, 1);
MAKE_METHOD_KW(spk, setAllChannelVolume, 1);
MAKE_METHOD_KW(spk, stop, 1);
MAKE_METHOD_KW(spk, tone, 1);
MAKE_METHOD_KW(spk, playWav, 1);

STATIC const mp_rom_map_elem_t spk_member_table[] = {
    MAKE_TABLE(spk, getVolume),
    MAKE_TABLE(spk, getChannelVolume),
    MAKE_TABLE(spk, setVolume),
    MAKE_TABLE(spk, setChannelVolume),
    MAKE_TABLE(spk, setAllChannelVolume),
    MAKE_TABLE(spk, stop),
    MAKE_TABLE(spk, tone),
    MAKE_TABLE(spk, playWav),
};
STATIC MP_DEFINE_CONST_DICT(spk_member, spk_member_table);

const mp_obj_type_t mp_spk_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Speaker,
    .locals_dict = (mp_obj_dict_t *)&spk_member,
};
