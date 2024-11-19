/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <utility/Touch_Class.hpp>

extern "C"
{
#include <string.h>
#include "cJSON.h"
#include "mpy_m5touch.h"

namespace m5
{
    static inline Touch_Class *getTouch(const mp_obj_t *args) {
        return (Touch_Class *)(((touch_obj_t *)MP_OBJ_TO_PTR(args[0]))->touch);
    }

    mp_obj_t touch_getX(mp_obj_t self) {
        return mp_obj_new_int(getTouch(&self)->getTouchPointRaw(0).x);
    }

    mp_obj_t touch_getY(mp_obj_t self) {
        return mp_obj_new_int(getTouch(&self)->getTouchPointRaw(0).y);
    }

    mp_obj_t touch_getCount(mp_obj_t self) {
        return mp_obj_new_int(getTouch(&self)->getCount());
    }

    mp_obj_t touch_getDetail(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_i};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_i, MP_ARG_INT, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Touch object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        auto detail = getTouch(&pos_args[0])->getDetail(args[ARG_i].u_int);
        mp_obj_t tuple[11] = {
            mp_obj_new_int(detail.deltaX()), // 0
            mp_obj_new_int(detail.deltaY()),
            mp_obj_new_int(detail.distanceX()),
            mp_obj_new_int(detail.distanceY()),
            mp_obj_new_bool(detail.isPressed()),
            mp_obj_new_bool(detail.wasPressed()), // 5
            mp_obj_new_bool(detail.wasClicked()),
            mp_obj_new_bool(detail.isReleased()),
            mp_obj_new_bool(detail.wasReleased()),
            mp_obj_new_bool(detail.isHolding()),
            mp_obj_new_bool(detail.wasHold()), // 10
        };
        return mp_obj_new_tuple(11, tuple);
    }

    mp_obj_t touch_getTouchPointRaw(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_i};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_i, MP_ARG_INT, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Touch object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        m5gfx::touch_point_t point = getTouch(&pos_args[0])->getTouchPointRaw(args[ARG_i].u_int);
        mp_obj_t tuple[4] = { mp_obj_new_int(point.x)
                              , mp_obj_new_int(point.y)
                              , mp_obj_new_int(point.size)
                              , mp_obj_new_int(point.id)};
        return mp_obj_new_tuple(4, tuple);
    }
}
}
