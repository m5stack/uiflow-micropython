/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2017 "Eric Poulsen" <eric@zyxod.com>
 * Copyright (c) 2017 "Tom Manning" <tom@manningetal.com>
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

#include <time.h>
#include <sys/time.h>
#include "driver/gpio.h"

#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "extmod/modmachine.h"
#include "shared/timeutils/timeutils.h"
#include "machine_rtc.h"
#include "uiflow_utility.h"

#ifndef NO_HAVE_RTC_SYNC
#define NO_HAVE_RTC_SYNC 0
#endif

#if NO_HAVE_RTC_SYNC == 0
#include "mpy_m5unified.h"
#endif

typedef struct _machine_rtc_obj_t {
    mp_obj_base_t base;
} machine_rtc_obj_t;

/* There is 8K of rtc_slow_memory, but some is used by the system software
    If the MICROPY_HW_RTC_USER_MEM_MAX is set too high, the following compile error will happen:
        region `rtc_slow_seg' overflowed by N bytes
    The current system software allows almost 4096 to be used.
    To avoid running into issues if the system software uses more, 2048 was picked as a max length

    You can also change this max length at compile time by defining MICROPY_HW_RTC_USER_MEM_MAX
    either on your make line, or in your board config.

    If MICROPY_HW_RTC_USER_MEM_MAX is set to 0, the RTC.memory() functionality will be not
    be compiled which frees some extra flash and RTC memory.
*/
#ifndef MICROPY_HW_RTC_USER_MEM_MAX
#define MICROPY_HW_RTC_USER_MEM_MAX     2048
#endif

// A board can enable MICROPY_HW_RTC_MEM_INIT_ALWAYS to always clear out RTC memory on boot.
// Defaults to RTC_NOINIT_ATTR so the user memory survives WDT resets and the like.
#if MICROPY_HW_RTC_MEM_INIT_ALWAYS
#define _USER_MEM_ATTR RTC_DATA_ATTR
#else
#define _USER_MEM_ATTR RTC_NOINIT_ATTR
#endif

// Optionally compile user memory functionality if the size of memory is greater than 0
#if MICROPY_HW_RTC_USER_MEM_MAX > 0
#define MEM_MAGIC           0x75507921
_USER_MEM_ATTR uint32_t rtc_user_mem_magic;
_USER_MEM_ATTR uint16_t rtc_user_mem_len;
_USER_MEM_ATTR uint8_t rtc_user_mem_data[MICROPY_HW_RTC_USER_MEM_MAX];
#endif

#undef _USER_MEM_ATTR

// singleton RTC object
static const machine_rtc_obj_t machine_rtc_obj = {{&machine_rtc_type}};

machine_rtc_config_t machine_rtc_config = {
    .ext1_pins = 0,
    .ext0_pin = -1
};

static mp_obj_t machine_rtc_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    // check arguments
    mp_arg_check_num(n_args, n_kw, 0, 0, false);

    #if MICROPY_HW_RTC_USER_MEM_MAX > 0
    if (rtc_user_mem_magic != MEM_MAGIC) {
        rtc_user_mem_magic = MEM_MAGIC;
        rtc_user_mem_len = 0;
    }
    #endif

    // return constant object
    return (mp_obj_t)&machine_rtc_obj;
}

static mp_obj_t machine_rtc_datetime_helper(mp_uint_t n_args, const mp_obj_t *args, int hour_index) {
    if (n_args == 1) {
        // Get time

        struct timeval tv;
        gettimeofday(&tv, NULL);

        struct tm tm;
        gmtime_r(&tv.tv_sec, &tm);

        mp_obj_t tuple[8] = {
            mp_obj_new_int(tm.tm_year + 1900),
            mp_obj_new_int(tm.tm_mon + 1),
            mp_obj_new_int(tm.tm_mday),
            mp_obj_new_int((tm.tm_wday + 6) % 7),
            mp_obj_new_int(tm.tm_hour),
            mp_obj_new_int(tm.tm_min),
            mp_obj_new_int(tm.tm_sec),
            mp_obj_new_int(tv.tv_usec)
        };

        return mp_obj_new_tuple(8, tuple);
    } else {
        // Set time

        mp_obj_t *items;
        mp_obj_get_array_fixed_n(args[1], 8, &items);

        // Get timezone info
        char timezone[64] = { 0 };
        char *tz = getenv("TZ");
        memcpy(timezone, tz, strlen(tz));

        // Set UTC timezone temporarily to set time correctly
        setenv("TZ", "UTC", 1);
        tzset();

        // Set utc time
        struct tm t;
        struct timeval tv = {0};
        memset(&t, 0, sizeof(struct tm));
        t.tm_year = mp_obj_get_int(items[0]) - 1900;
        t.tm_mon = mp_obj_get_int(items[1]) - 1;
        t.tm_mday = mp_obj_get_int(items[2]);
        t.tm_hour = mp_obj_get_int(items[hour_index]);
        t.tm_min = mp_obj_get_int(items[hour_index + 1]);
        t.tm_sec = mp_obj_get_int(items[hour_index + 2]);
        t.tm_isdst = 0; // Daylight Saving Time not implemented
        tv.tv_sec = mktime(&t);
        tv.tv_usec = mp_obj_get_int(items[6]);
        settimeofday(&tv, NULL);
        #if NO_HAVE_RTC_SYNC == 0
        rtc_sync(&tv);
        #endif

        // Restore previous timezone
        setenv("TZ", timezone, 1);
        tzset();

        return mp_const_none;
    }
}
static mp_obj_t machine_rtc_datetime(size_t n_args, const mp_obj_t *args) {
    return machine_rtc_datetime_helper(n_args, args, 4);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(machine_rtc_datetime_obj, 1, 2, machine_rtc_datetime);

static mp_obj_t machine_rtc_local_datetime_helper(mp_uint_t n_args, const mp_obj_t *args) {
    if (n_args == 1) {
        // Get time
        struct timeval tv;
        gettimeofday(&tv, NULL);

        struct tm tm;
        localtime_r(&tv.tv_sec, &tm);

        mp_obj_t tuple[8] = {
            mp_obj_new_int(tm.tm_year + 1900),
            mp_obj_new_int(tm.tm_mon + 1),
            mp_obj_new_int(tm.tm_mday),
            mp_obj_new_int((tm.tm_wday + 6) % 7),
            mp_obj_new_int(tm.tm_hour),
            mp_obj_new_int(tm.tm_min),
            mp_obj_new_int(tm.tm_sec),
            mp_obj_new_int(tv.tv_usec)
        };

        return mp_obj_new_tuple(8, tuple);
    } else {
        // Set time
        mp_obj_t *items;
        mp_obj_get_array_fixed_n(args[1], 8, &items);

        struct timeval tv = {0};
        #if MICROPY_EPOCH_IS_1970
        tv.tv_sec = timeutils_seconds_since_epoch(mp_obj_get_int(items[0]),
            mp_obj_get_int(items[1]), mp_obj_get_int(items[2]),
            mp_obj_get_int(items[4]), mp_obj_get_int(items[5]),
            mp_obj_get_int(items[6]));
        #else
        tv.tv_sec = timeutils_seconds_since_epoch(mp_obj_get_int(items[0]),
            mp_obj_get_int(items[1]), mp_obj_get_int(items[2]),
            mp_obj_get_int(items[4]), mp_obj_get_int(items[5]),
            mp_obj_get_int(items[6]) + TIMEUTILS_SECONDS_1970_TO_2000);
        #endif
        tv.tv_usec = mp_obj_get_int(items[7]);
        settimeofday(&tv, NULL);
        #if NO_HAVE_RTC_SYNC == 0
        rtc_sync(&tv);
        #endif

        return mp_const_none;
    }
}
static mp_obj_t machine_rtc_local_datetime(size_t n_args, const mp_obj_t *args) {
    return machine_rtc_local_datetime_helper(n_args, args);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(machine_rtc_local_datetime_obj, 1, 2, machine_rtc_local_datetime);

static mp_obj_t machine_rtc_timezone(size_t n_args, const mp_obj_t *args) {
    if (n_args == 1) {
        // Get timezone
        char *tz = getenv("TZ");
        if (tz == NULL) {
            return mp_const_none;
        } else {
            char timezone[64] = { 0 };
            memcpy(timezone, tz, strlen(tz));
            char *ptr = strchr(timezone, '+');
            if (ptr != NULL) {
                *ptr = '-';
            } else {
                ptr = strchr(timezone, '-');
                if (ptr != NULL) {
                    *ptr = '+';
                }
            }
            return mp_obj_new_str(timezone, strlen(timezone));
        }
    } else {
        // Set timezone
        char timezone[64] = { 0 };
        snprintf(timezone, sizeof(timezone) - 1, "%s", mp_obj_str_get_str(args[1]));

        char *ptr = strchr(timezone, '-');
        if (ptr != NULL) {
            *ptr = '+';
        } else {
            ptr = strchr(timezone, '+');
            if (ptr != NULL) {
                *ptr = '-';
            }
        }

        setenv("TZ", timezone, 1);
        tzset();

        nvs_write_str_helper(UIFLOW_NVS_NAMESPACE, "tz", timezone);
        return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(machine_rtc_timezone_obj, 1, 2, machine_rtc_timezone);

static mp_obj_t machine_rtc_init(mp_obj_t self_in, mp_obj_t date) {
    mp_obj_t args[2] = {self_in, date};
    machine_rtc_datetime_helper(2, args, 3);

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(machine_rtc_init_obj, machine_rtc_init);

#if MICROPY_HW_RTC_USER_MEM_MAX > 0
static mp_obj_t machine_rtc_memory(size_t n_args, const mp_obj_t *args) {
    if (n_args == 1) {
        // read RTC memory
        uint8_t rtcram[MICROPY_HW_RTC_USER_MEM_MAX];
        memcpy((char *)rtcram, (char *)rtc_user_mem_data, rtc_user_mem_len);
        return mp_obj_new_bytes(rtcram, rtc_user_mem_len);
    } else {
        // write RTC memory
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[1], &bufinfo, MP_BUFFER_READ);

        if (bufinfo.len > MICROPY_HW_RTC_USER_MEM_MAX) {
            mp_raise_ValueError(MP_ERROR_TEXT("buffer too long"));
        }
        memcpy((char *)rtc_user_mem_data, (char *)bufinfo.buf, bufinfo.len);
        rtc_user_mem_len = bufinfo.len;
        return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(machine_rtc_memory_obj, 1, 2, machine_rtc_memory);
#endif

static const mp_rom_map_elem_t machine_rtc_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&machine_rtc_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_datetime), MP_ROM_PTR(&machine_rtc_datetime_obj) },
    { MP_ROM_QSTR(MP_QSTR_local_datetime), MP_ROM_PTR(&machine_rtc_local_datetime_obj) },
    { MP_ROM_QSTR(MP_QSTR_timezone), MP_ROM_PTR(&machine_rtc_timezone_obj) },
    #if MICROPY_HW_RTC_USER_MEM_MAX > 0
    { MP_ROM_QSTR(MP_QSTR_memory), MP_ROM_PTR(&machine_rtc_memory_obj) },
    #endif
};
static MP_DEFINE_CONST_DICT(machine_rtc_locals_dict, machine_rtc_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    machine_rtc_type,
    MP_QSTR_RTC,
    MP_TYPE_FLAG_NONE,
    make_new, machine_rtc_make_new,
    locals_dict, &machine_rtc_locals_dict
    );
