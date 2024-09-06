// SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
//
// SPDX-License-Identifier: MIT

#include <stdio.h>
#include <string.h>
#include <sys/time.h>

#include "py/runtime.h"

STATIC mp_obj_t m5_utils_remap(size_t n_args, const mp_obj_t *args) {
    mp_float_t x = mp_obj_get_float(args[0]);
    mp_float_t in_min = mp_obj_get_float(args[1]);
    mp_float_t in_max = mp_obj_get_float(args[2]);
    mp_float_t out_min = mp_obj_get_float(args[3]);
    mp_float_t out_max = mp_obj_get_float(args[4]);

    if (in_max == in_min) {
        // 抛出异常或返回错误
        mp_raise_ValueError("Input range cannot be zero");
        return mp_const_none;
    }

    mp_float_t result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
    return mp_obj_new_float(result);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(m5_utils_remap_obj, 5, 5, m5_utils_remap);


STATIC const mp_rom_map_elem_t m5utils_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_m5utils) },

    { MP_ROM_QSTR(MP_QSTR_remap), MP_ROM_PTR(&m5_utils_remap_obj) },
};

STATIC MP_DEFINE_CONST_DICT(m5utils_module_globals, m5utils_module_globals_table);

const mp_obj_module_t m5utils_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&m5utils_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_m5utils, m5utils_module);
