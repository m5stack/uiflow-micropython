#include "m5unified.h"

MAKE_METHOD_KW(mic, config, 0);
MAKE_METHOD_0(mic, begin);
MAKE_METHOD_0(mic, end);
MAKE_METHOD_0(mic, isRunning);
MAKE_METHOD_0(mic, isEnabled);
MAKE_METHOD_0(mic, isRecording);
MAKE_METHOD_KW(mic, setSampleRate, 1);
MAKE_METHOD_KW(mic, record, 1);

STATIC const mp_rom_map_elem_t mic_member_table[] = {
    MAKE_TABLE(mic, config),
    MAKE_TABLE(mic, begin),
    MAKE_TABLE(mic, end),
    MAKE_TABLE(mic, isRunning),
    MAKE_TABLE(mic, isEnabled),
    MAKE_TABLE(mic, isRecording),
    MAKE_TABLE(mic, setSampleRate),
    MAKE_TABLE(mic, record),
};

STATIC MP_DEFINE_CONST_DICT(mic_member, mic_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_mic_type,
    MP_QSTR_MIC,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&mic_member
    );
#else
const mp_obj_type_t mp_mic_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_MIC,
    .locals_dict = (mp_obj_dict_t *)&mic_member,
};
#endif
