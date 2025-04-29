/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include "py/objstr.h"
#include "py/runtime.h"

extern const mp_obj_type_t audio2_player_type;
extern const mp_obj_type_t audio2_recorder_type;

static const mp_rom_map_elem_t m5audio2_module_globals_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_m5audio2)     },
    { MP_ROM_QSTR(MP_QSTR_Player),   MP_ROM_PTR(&audio2_player_type)   },
    { MP_ROM_QSTR(MP_QSTR_Recorder), MP_ROM_PTR(&audio2_recorder_type) },
    /* *FORMAT-ON* */
};

static MP_DEFINE_CONST_DICT(m5audio2_module_globals, m5audio2_module_globals_table);

const mp_obj_module_t m5audio2_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&m5audio2_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_m5audio2, m5audio2_module);
