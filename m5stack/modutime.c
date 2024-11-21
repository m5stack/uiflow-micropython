/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * Development of the code in this file was sponsored by Microbric Pty Ltd
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2016 Damien P. George
 * Copyright (c) 2024 M5Stack Technology CO LTD
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <stdio.h>
#include <string.h>
#include <sys/time.h>

#include "py/runtime.h"
#include "shared/timeutils/timeutils.h"
#include "extmod/modtime.h"
#include "uiflow_utility.h"

static mp_obj_t time_gmttime(size_t n_args, const mp_obj_t *args) {
    struct tm tm;
    time_t seconds;
    if (n_args == 0 || args[0] == mp_const_none) {
        struct timeval tv;
        gettimeofday(&tv, NULL);
        seconds = tv.tv_sec;
    } else {
        seconds = mp_obj_get_int(args[0]);
    }
    gmtime_r(&seconds, &tm);
    mp_obj_t tuple[8] = {
        tuple[0] = mp_obj_new_int(tm.tm_year + 1900),  // include the century
        tuple[1] = mp_obj_new_int(tm.tm_mon + 1),      // month is 1-12
        tuple[2] = mp_obj_new_int(tm.tm_mday),         // mday is 1-31
        tuple[3] = mp_obj_new_int(tm.tm_hour),         // hour is 0-23
        tuple[4] = mp_obj_new_int(tm.tm_min),          // minute is 0-59
        tuple[5] = mp_obj_new_int(tm.tm_sec),          // second is 0-59
        tuple[6] = mp_obj_new_int(tm.tm_wday),     // weekday is 0-6 for Mon-Sun
        tuple[7] = mp_obj_new_int(tm.tm_yday),         // yearday is 1-366
    };
    return mp_obj_new_tuple(8, tuple);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(time_gmttime_obj, 0, 1, time_gmttime);

static mp_obj_t time_localtime(size_t n_args, const mp_obj_t *args) {
    struct tm tm;
    time_t seconds;
    if (n_args == 0 || args[0] == mp_const_none) {
        struct timeval tv;
        gettimeofday(&tv, NULL);
        seconds = tv.tv_sec;
    } else {
        seconds = mp_obj_get_int(args[0]);
    }
    localtime_r(&seconds, &tm);
    mp_obj_t tuple[8] = {
        tuple[0] = mp_obj_new_int(tm.tm_year + 1900),  // include the century
        tuple[1] = mp_obj_new_int(tm.tm_mon + 1),      // month is 1-12
        tuple[2] = mp_obj_new_int(tm.tm_mday),         // mday is 1-31
        tuple[3] = mp_obj_new_int(tm.tm_hour),         // hour is 0-23
        tuple[4] = mp_obj_new_int(tm.tm_min),          // minute is 0-59
        tuple[5] = mp_obj_new_int(tm.tm_sec),          // second is 0-59
        tuple[6] = mp_obj_new_int(tm.tm_wday),     // weekday is 0-6 for Mon-Sun
        tuple[7] = mp_obj_new_int(tm.tm_yday),         // yearday is 1-366
    };
    return mp_obj_new_tuple(8, tuple);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(time_localtime_obj, 0, 1, time_localtime);

static mp_obj_t time_mktime(mp_obj_t tuple) {
    size_t len;
    mp_obj_t *elem;
    mp_obj_get_array(tuple, &len, &elem);

    // localtime generates a tuple of len 8. CPython uses 9, so we accept both.
    if (len < 8 || len > 9) {
        mp_raise_msg_varg(&mp_type_TypeError, MP_ERROR_TEXT("mktime needs a tuple of length 8 or 9 (%d given)"), len);
    }

    #if MICROPY_EPOCH_IS_1970
    return mp_obj_new_int_from_uint(timeutils_mktime(mp_obj_get_int(elem[0]),
        mp_obj_get_int(elem[1]), mp_obj_get_int(elem[2]), mp_obj_get_int(elem[3]),
        mp_obj_get_int(elem[4]), mp_obj_get_int(elem[5])));
    #else
    return mp_obj_new_int_from_uint(timeutils_mktime(mp_obj_get_int(elem[0]),
        mp_obj_get_int(elem[1]), mp_obj_get_int(elem[2]), mp_obj_get_int(elem[3]),
        mp_obj_get_int(elem[4]), mp_obj_get_int(elem[5])) + TIMEUTILS_SECONDS_1970_TO_2000);
    #endif
}
static MP_DEFINE_CONST_FUN_OBJ_1(time_mktime_obj, time_mktime);

static mp_obj_t time_time(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return mp_obj_new_int(tv.tv_sec);
}
MP_DEFINE_CONST_FUN_OBJ_0(time_time_obj, time_time);

static mp_obj_t time_timezone(size_t n_args, const mp_obj_t *args) {
    if (n_args == 0 || args[0] == mp_const_none) {
        char *tz = getenv("TZ");
        if (tz == NULL) {
            return mp_const_none;
        } else {
            return mp_obj_new_str(tz, strlen(tz));
        }
    } else {
        char tz[64];
        snprintf(tz, sizeof(tz), "%s", mp_obj_str_get_str(args[0]));
        setenv("TZ", tz, 1);
        tzset();

        nvs_write_str_helper(UIFLOW_NVS_NAMESPACE, "tz", tz);
        return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(time_timezone_obj, 0, 1, time_timezone);

static const mp_rom_map_elem_t time_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_utime) },

    { MP_ROM_QSTR(MP_QSTR_gmtime), MP_ROM_PTR(&time_gmttime_obj) },
    { MP_ROM_QSTR(MP_QSTR_localtime), MP_ROM_PTR(&time_localtime_obj) },
    { MP_ROM_QSTR(MP_QSTR_mktime), MP_ROM_PTR(&time_mktime_obj) },
    { MP_ROM_QSTR(MP_QSTR_time), MP_ROM_PTR(&time_time_obj) },
    { MP_ROM_QSTR(MP_QSTR_timezone), MP_ROM_PTR(&time_timezone_obj) },
    { MP_ROM_QSTR(MP_QSTR_sleep), MP_ROM_PTR(&mp_time_sleep_obj) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&mp_time_sleep_ms_obj) },
    { MP_ROM_QSTR(MP_QSTR_sleep_us), MP_ROM_PTR(&mp_time_sleep_us_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&mp_time_ticks_ms_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_us), MP_ROM_PTR(&mp_time_ticks_us_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_cpu), MP_ROM_PTR(&mp_time_ticks_cpu_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_add), MP_ROM_PTR(&mp_time_ticks_add_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_diff), MP_ROM_PTR(&mp_time_ticks_diff_obj) },
    { MP_ROM_QSTR(MP_QSTR_time_ns), MP_ROM_PTR(&mp_time_time_ns_obj) },
};

static MP_DEFINE_CONST_DICT(time_module_globals, time_module_globals_table);

const mp_obj_module_t utime_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&time_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_utime, utime_module);
