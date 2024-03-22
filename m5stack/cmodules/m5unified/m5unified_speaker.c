/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

// -------- Speaker wrapper
MAKE_METHOD_KW(spk, config, 0);
MAKE_METHOD_0(spk, begin);
MAKE_METHOD_0(spk, end);
MAKE_METHOD_0(spk, isRunning);
MAKE_METHOD_0(spk, isEnabled);
MAKE_METHOD_V(spk, isPlaying, 1, 2);
MAKE_METHOD_0(spk, getPlayingChannels);
MAKE_METHOD_KW(spk, setVolume, 1);
MAKE_METHOD_0(spk, getVolume);
MAKE_METHOD_1(spk, setVolumePercentage);
MAKE_METHOD_0(spk, getVolumePercentage);
MAKE_METHOD_KW(spk, setAllChannelVolume, 1);
MAKE_METHOD_KW(spk, setChannelVolume, 1);
MAKE_METHOD_1(spk, getChannelVolume);
MAKE_METHOD_KW(spk, stop, 1);
MAKE_METHOD_KW(spk, tone, 1);
MAKE_METHOD_KW(spk, playRaw, 1);
MAKE_METHOD_KW(spk, playWav, 1);

STATIC const mp_rom_map_elem_t spk_member_table[] = {
    MAKE_TABLE(spk, config),
    MAKE_TABLE(spk, begin),
    MAKE_TABLE(spk, end),
    MAKE_TABLE(spk, isRunning),
    MAKE_TABLE(spk, isEnabled),
    MAKE_TABLE(spk, isPlaying),
    MAKE_TABLE(spk, getPlayingChannels),
    MAKE_TABLE(spk, setVolume),
    MAKE_TABLE(spk, getVolume),
    MAKE_TABLE(spk, setVolumePercentage),
    MAKE_TABLE(spk, getVolumePercentage),
    MAKE_TABLE(spk, setAllChannelVolume),
    MAKE_TABLE(spk, setChannelVolume),
    MAKE_TABLE(spk, getChannelVolume),
    MAKE_TABLE(spk, stop),
    MAKE_TABLE(spk, tone),
    MAKE_TABLE(spk, playRaw),
    MAKE_TABLE(spk, playWav),
};
STATIC MP_DEFINE_CONST_DICT(spk_member, spk_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_spk_type,
    MP_QSTR_Speaker,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&spk_member
    );
#else
const mp_obj_type_t mp_spk_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Speaker,
    .locals_dict = (mp_obj_dict_t *)&spk_member,
};
#endif
