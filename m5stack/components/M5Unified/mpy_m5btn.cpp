/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <utility/Button_Class.hpp>

extern "C"
{
#include "mpy_m5btn.h"

namespace m5
{
    static inline Button_Class *getBtn(const mp_obj_t& self) {
        return (Button_Class *)(((btn_obj_t *)MP_OBJ_TO_PTR(self))->btn);
    }

    mp_obj_t btn_isHolding(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->isHolding());
    }
    mp_obj_t btn_isPressed(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->isPressed());
    }
    mp_obj_t btn_isReleased(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->isReleased());
    }
    mp_obj_t btn_wasChangePressed(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasChangePressed());
    }
    mp_obj_t btn_wasClicked(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasClicked());
    }
    mp_obj_t btn_wasHold(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasHold());
    }
    mp_obj_t btn_wasPressed(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasPressed());
    }
    mp_obj_t btn_wasReleased(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasReleased());
    }
    mp_obj_t btn_lastChange(mp_obj_t self) {
        return mp_obj_new_int(getBtn(self)->lastChange());
    }
    mp_obj_t btn_wasSingleClicked(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasSingleClicked());
    }
    mp_obj_t btn_wasDoubleClicked(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasDoubleClicked());
    }
    mp_obj_t btn_wasDeciedClickCount(mp_obj_t self) {
        return mp_obj_new_bool(getBtn(self)->wasDeciedClickCount());
    }
    mp_obj_t btn_getClickCount(mp_obj_t self) {
        return mp_obj_new_int(getBtn(self)->getClickCount());
    }
    mp_obj_t btn_pressedFor(mp_obj_t self, mp_obj_t msec) {
        return mp_obj_new_bool(getBtn(self)->pressedFor(mp_obj_get_int(msec)));
    }
    mp_obj_t btn_releasedFor(mp_obj_t self, mp_obj_t msec) {
        return mp_obj_new_bool(getBtn(self)->releasedFor(mp_obj_get_int(msec)));
    }
    mp_obj_t btn_setDebounceThresh(mp_obj_t self, mp_obj_t msec) {
        getBtn(self)->setDebounceThresh(mp_obj_get_int(msec));
        return mp_const_none;
    }
    mp_obj_t btn_setHoldThresh(mp_obj_t self, mp_obj_t msec) {
        getBtn(self)->setHoldThresh(mp_obj_get_int(msec));
        return mp_const_none;
    }
    mp_obj_t btn_setCallback(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_type, ARG_cb};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_type, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
            { MP_QSTR_cb,   MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        switch ((btn_cb_type_t)args[ARG_type].u_int)
        {
            case BTN_TYPE_WAS_CLICKED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasClicked = 1;
                *((btn_obj_t *)pos_args[0])->callbacks.wasClicked_cb = args[ARG_cb].u_obj;
                break;
            case BTN_TYPE_WAS_DOUBLECLICKED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasDoubleClicked = 1;
                *((btn_obj_t *)pos_args[0])->callbacks.wasDoubleClicked_cb = args[ARG_cb].u_obj;
                break;
            case BTN_TYPE_WAS_HOLD:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasHold = 1;
                *((btn_obj_t *)pos_args[0])->callbacks.wasHold_cb = args[ARG_cb].u_obj;
                break;
            case BTN_TYPE_WAS_PRESSED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasPressed = 1;
                *((btn_obj_t *)pos_args[0])->callbacks.wasPressed_cb = args[ARG_cb].u_obj;
                break;
            case BTN_TYPE_WAS_RELEASED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasReleased = 1;
                *((btn_obj_t *)pos_args[0])->callbacks.wasReleased_cb = args[ARG_cb].u_obj;
                break;
            default:
                break;
        }
        return mp_const_none;
    }
    mp_obj_t btn_removeCallback(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_type};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_type, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        switch ((btn_cb_type_t)args[ARG_type].u_int)
        {
            case BTN_TYPE_WAS_CLICKED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasClicked = 0;
                *((btn_obj_t *)pos_args[0])->callbacks.wasClicked_cb = NULL;
                break;
            case BTN_TYPE_WAS_DOUBLECLICKED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasDoubleClicked = 0;
                *((btn_obj_t *)pos_args[0])->callbacks.wasDoubleClicked_cb = NULL;
                break;
            case BTN_TYPE_WAS_HOLD:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasHold = 0;
                *((btn_obj_t *)pos_args[0])->callbacks.wasHold_cb = NULL;
                break;
            case BTN_TYPE_WAS_PRESSED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasPressed = 0;
                *((btn_obj_t *)pos_args[0])->callbacks.wasPressed_cb = NULL;
                break;
            case BTN_TYPE_WAS_RELEASED:
                ((btn_obj_t *)pos_args[0])->callbacks.flag_bit.wasReleased = 0;
                *((btn_obj_t *)pos_args[0])->callbacks.wasReleased_cb = NULL;
                break;
            default:
                break;
        }
        return mp_const_none;
    }
}
}
