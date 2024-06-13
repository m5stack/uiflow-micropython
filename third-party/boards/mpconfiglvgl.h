/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#if MICROPY_PY_LVGL
#ifndef MICROPY_INCLUDED_PY_MPSTATE_H
#define MICROPY_INCLUDED_PY_MPSTATE_H
#include "./../../../m5stack/components/lv_bindings/lvgl/src/misc/lv_gc.h"
#undef MICROPY_INCLUDED_PY_MPSTATE_H
#else
#include "./../../../m5stack/components/lv_bindings/lvgl/src/misc/lv_gc.h"
#endif
#else
#define LV_ROOTS
#endif

#if MICROPY_PY_LVGL
extern void lvgl_deinit();
#define MICROPY_PORT_DEINIT_FUNC lvgl_deinit()
#endif

#if MICROPY_PY_LVGL
#define MICROPY_PORT_ROOT_POINTERS \
    LV_ROOTS \
    void *mp_lv_user_data; \
    const char *readline_hist[8]; \
    mp_obj_t machine_pin_irq_handler[40]; \
    struct _machine_timer_obj_t *machine_timer_obj_head; \
    struct _machine_i2s_obj_t *machine_i2s_obj[I2S_NUM_MAX]; \
    mp_obj_t native_code_pointers; \
    MICROPY_PORT_ROOT_POINTER_BLUETOOTH_NIMBLE
#endif
