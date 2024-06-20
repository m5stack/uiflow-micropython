/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>
#include <py/stream.h>
#include <py/builtin.h>

#include "mpy_m5gfx.h"
#include "mpy_m5touch.h"


extern mp_obj_t m5_begin(size_t n_args, const mp_obj_t *args);
extern mp_obj_t m5_update(void);
extern mp_obj_t m5_end(void);
extern mp_obj_t m5_getBoard(void);

extern gfx_obj_t m5_display;
extern touch_obj_t m5_touch;
