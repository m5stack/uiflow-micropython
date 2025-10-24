/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>

typedef struct _led_obj_t {
    mp_obj_base_t base;
    void *led;
} led_obj_t;

extern const mp_obj_type_t mp_led_type;
