#include <utility/Power_Class.hpp>

extern "C"
{
#include <py/obj.h>
#include "mpy_m5power.h"


namespace m5
{
    static inline Power_Class *getPower(const mp_obj_t& self) {
        return (Power_Class *)(((pwr_obj_t *)MP_OBJ_TO_PTR(self))->btn);
    }

    mp_obj_t power_setExtOutput(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_enable, ARG_port_mask};
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_enable,    MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true} },
            { MP_QSTR_port_mask, MP_ARG_INT,                    {.u_int = 0xFF}  },
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->setExtOutput(args[ARG_enable].u_bool, (ext_port_mask_t)args[ARG_port_mask].u_int);
        return mp_const_none;
    }

    mp_obj_t power_getExtOutput(mp_obj_t self) {
        return mp_obj_new_bool(getPower(self)->getExtOutput());
    }

    mp_obj_t power_setUsbOutput(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_enable};
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_enable, MP_ARG_INT | MP_ARG_REQUIRED, {.u_bool = true} }
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->setUsbOutput(args[ARG_enable].u_bool);
        return mp_const_none;
    }

    mp_obj_t power_getUsbOutput(mp_obj_t self) {
        return mp_obj_new_bool(getPower(self)->getUsbOutput());
    }

    mp_obj_t power_setLed(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_br};
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_br, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} },
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->setLed(args[ARG_br].u_int);
        return mp_const_none;
    }

    mp_obj_t power_powerOff(mp_obj_t self) {
        getPower(self)->powerOff();
        return mp_const_none;
    }

    mp_obj_t power_timerSleep(size_t n_args, const mp_obj_t *args) {
        if (n_args == 2) {
            getPower(args[0])->timerSleep(mp_obj_get_int(args[1]));
        } else if (n_args == 3) {
            rtc_time_t time;
            time.minutes = mp_obj_get_int(args[1]);
            time.hours = mp_obj_get_int(args[2]);
            getPower(args[0])->timerSleep(time);
        } else if (n_args == 5) {
            rtc_time_t time;
            rtc_date_t date;
            time.minutes = mp_obj_get_int(args[1]);
            time.hours = mp_obj_get_int(args[2]);
            date.date = mp_obj_get_int(args[3]);
            date.weekDay = mp_obj_get_int(args[4]);
            getPower(args[0])->timerSleep(date, time);
        }
        return mp_const_none;
    }

    mp_obj_t power_deepSleep(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum { ARG_micro_seconds, ARG_touch_wakeup };
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_micro_seconds, MP_ARG_INT,  {.u_int = 0}     },
            { MP_QSTR_touch_wakeup,  MP_ARG_BOOL, {.u_bool = true} },
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->deepSleep(args[ARG_micro_seconds].u_int, args[ARG_touch_wakeup].u_bool);
        return mp_const_none;
    }

    mp_obj_t power_lightSleep(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum { ARG_micro_seconds, ARG_touch_wakeup };
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_micro_seconds, MP_ARG_INT,  {.u_int = 0}     },
            { MP_QSTR_touch_wakeup,  MP_ARG_BOOL, {.u_bool = true} },
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->lightSleep(args[ARG_micro_seconds].u_int, args[ARG_touch_wakeup].u_bool);
        return mp_const_none;
    }

    mp_obj_t power_getBatteryLevel(mp_obj_t self) {
        return mp_obj_new_int(getPower(self)->getBatteryLevel());
    }

    mp_obj_t power_setBatteryCharge(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_enable};
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_enable, MP_ARG_INT | MP_ARG_REQUIRED, {.u_bool = true} }
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->setBatteryCharge(args[ARG_enable].u_bool);
        return mp_const_none;
    }

    mp_obj_t power_setChargeCurrent(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_ma};
        const mp_arg_t allowed_args[] = {
            /* *FORMAT-OFF* */
            { MP_QSTR_ma, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = true} }
            /* *FORMAT-ON* */
        };
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getPower(pos_args[0])->setChargeCurrent(args[ARG_ma].u_int);
        return mp_const_none;
    }

    mp_obj_t power_setChargeVoltage(mp_obj_t self, mp_obj_t max_mv) {
        getPower(self)->setChargeVoltage(mp_obj_get_int(max_mv));
        return mp_const_none;
    }

    mp_obj_t power_isCharging(mp_obj_t self) {
        return mp_obj_new_bool(getPower(self)->isCharging());
    }

    mp_obj_t power_getBatteryVoltage(mp_obj_t self) {
        return mp_obj_new_int(getPower(self)->getBatteryVoltage());
    }

    mp_obj_t power_getBatteryCurrent(mp_obj_t self) {
        return mp_obj_new_int(getPower(self)->getBatteryCurrent());
    }

    mp_obj_t power_getKeyState(mp_obj_t self) {
        return mp_obj_new_int(getPower(self)->getKeyState());
    }

    mp_obj_t power_setVibration(mp_obj_t self, mp_obj_t level) {
        getPower(self)->setVibration(mp_obj_get_int(level));
        return mp_const_none;
    }

    mp_obj_t power_getType(mp_obj_t self) {
        return mp_obj_new_bool(getPower(self)->getType());
    }
}
}
