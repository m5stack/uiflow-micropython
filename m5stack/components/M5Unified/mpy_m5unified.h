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
#include "mpy_m5btn.h"
#include "mpy_m5gfx.h"
#include "mpy_m5imu.h"
#include "mpy_m5spk.h"
#include "mpy_m5power.h"
#include "mpy_m5widgets.h"
#include "mpy_m5touch.h"
#include "mpy_m5als.h"
#include "mpy_m5mic.h"
#include "mic_config_t.h"

extern mp_obj_t m5_begin(size_t n_args, const mp_obj_t *args);
extern mp_obj_t m5_add_display(mp_obj_t dict);
extern mp_obj_t m5_update(void);
extern mp_obj_t m5_end(void);
extern mp_obj_t m5_getBoard(void);
extern mp_obj_t m5_getDisplayCount(void);

extern const spk_obj_t m5_speaker;
extern const pwr_obj_t m5_power;
extern const pwr_obj_t m5_imu;
extern btn_obj_t m5_btnA;
extern btn_obj_t m5_btnB;
extern btn_obj_t m5_btnC;
extern btn_obj_t m5_btnPWR;
extern btn_obj_t m5_btnEXT;
extern gfx_obj_t m5_display;
extern touch_obj_t m5_touch;
extern als_obj_t m5_als;
extern const mic_obj_t m5_mic;
