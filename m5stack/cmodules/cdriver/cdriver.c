/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objlist.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "mphalport.h"

extern const mp_obj_module_t cdriver_max30100_type;
extern const mp_obj_module_t cdriver_max30102_type;
extern const mp_obj_module_t mp_module_esp_dmx;

static const mp_rom_map_elem_t mp_module_cdriver_globals_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cdriver)            },
    { MP_ROM_QSTR(MP_QSTR_MAX30100), MP_OBJ_FROM_PTR(&cdriver_max30100_type) },
    { MP_ROM_QSTR(MP_QSTR_MAX30102), MP_OBJ_FROM_PTR(&cdriver_max30102_type) },
    { MP_ROM_QSTR(MP_QSTR_esp_dmx),  MP_OBJ_FROM_PTR(&mp_module_esp_dmx)     },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(mp_module_cdriver_globals, mp_module_cdriver_globals_table);

// Define module object.
const mp_obj_module_t mp_module_cdriver = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_cdriver_globals,
};

MP_REGISTER_MODULE(MP_QSTR_cdriver, mp_module_cdriver);
