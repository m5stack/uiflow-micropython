/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

// #include <utility/Power_Class.hpp>
#include <utility/LED_Class.hpp>

extern "C"
{
#include <py/obj.h>
#include "mpy_m5led.h"
#include "uiflow_utility.h"


namespace m5
{
    static inline LED_Class *getLED(const mp_obj_t& self) {
        return (LED_Class *)(((led_obj_t *)MP_OBJ_TO_PTR(self))->led);
    }

    mp_obj_t led_display(mp_obj_t self) {
        getLED(self)->display();
        return mp_const_none;
    }

    mp_obj_t led_getCount(mp_obj_t self) {
        return mp_obj_new_int(getLED(self)->getCount());
    }

    mp_obj_t led_setBrightness(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_br};
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_br, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} },
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getLED(pos_args[0])->setBrightness(args[ARG_br].u_int);
        return mp_const_none;
    }

    mp_obj_t led_setAllColor(size_t n_args, const mp_obj_t *args) {
        if (n_args == 2) {
            getLED(args[0])->setAllColor((uint32_t)mp_obj_get_int(args[1]));
        } else if (n_args == 4) {
            getLED(args[0])->setAllColor(mp_obj_get_int(args[1]), mp_obj_get_int(args[2]), mp_obj_get_int(args[3]));
        }
        return mp_const_none;
    }

    mp_obj_t led_setColor(size_t n_args, const mp_obj_t *args) {
        if (n_args == 3) {
            getLED(args[0])->setColor(mp_obj_get_int(args[1]), (uint32_t)mp_obj_get_int(args[2]));
        } else if (n_args == 5) {
            getLED(args[0])->setColor(mp_obj_get_int(args[1]), mp_obj_get_int(args[2]), mp_obj_get_int(args[3]), mp_obj_get_int(args[4]));
        }
        return mp_const_none;
    }
}
}
