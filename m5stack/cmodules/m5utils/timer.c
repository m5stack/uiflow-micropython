/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/
#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>

#include "freertos/FreeRTOS.h"
#include "freertos/timers.h"

typedef struct _mp_m5utils_timer_t {
    mp_obj_base_t base;
    TimerHandle_t timer_handler;
    mp_uint_t period_ms;
    mp_uint_t repeat;
    mp_obj_t callback;
} mp_m5utils_timer_t;

extern const mp_obj_type_t mp_m5utils_timer_type;

static void vTimerCallback(TimerHandle_t timer) {
    mp_m5utils_timer_t *self = pvTimerGetTimerID(timer);
    if (self->callback != mp_const_none) {
        mp_sched_schedule(self->callback, self);
    }
}

static mp_obj_t mp_m5utils_timer_init_helper(mp_m5utils_timer_t *self, mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {
        ARG_mode,
        ARG_period,
        ARG_callback,
    };
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_mode,         MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 1} },
        { MP_QSTR_period,       MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0xffffffff} },
        { MP_QSTR_callback,     MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = mp_const_none} },
        /* *FORMAT-ON* */
    };

    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    self->repeat = args[ARG_mode].u_int;
    self->period_ms = args[ARG_period].u_int;
    self->callback = args[ARG_callback].u_obj;

    return mp_const_none;
}


static void mp_m5utils_timer_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    mp_m5utils_timer_t *self = MP_OBJ_TO_PTR(self_in);
    qstr mode = self->repeat ? MP_QSTR_PERIODIC : MP_QSTR_ONE_SHOT;

    mp_printf(print, "Timer(mode=%q, period=%lu)", mode, self->period_ms);
}

static mp_obj_t mp_m5utils_timer_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);

    mp_m5utils_timer_t *self = m_new_obj(mp_m5utils_timer_t);
    self->base.type = &mp_m5utils_timer_type;

    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    mp_m5utils_timer_init_helper(self, n_args - 1, args + 1, &kw_args);

    self->timer_handler = xTimerCreate("freertos timer", pdMS_TO_TICKS(self->period_ms), self->repeat, self, vTimerCallback);
    if (self->timer_handler == NULL) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("Failed creating FreeRTOS timer"));
    }
    if (xTimerStart(self->timer_handler, 0) != pdPASS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("Failed starting FreeRTOS timer"));
    }
    return self;
}


static mp_obj_t mp_m5utils_timer_init(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    mp_m5utils_timer_t *self = args[0];
    mp_m5utils_timer_init_helper(self, n_args - 1, args + 1, kw_args);
    if (self->timer_handler) {
        xTimerDelete(self->timer_handler, portMAX_DELAY);
        self->timer_handler = NULL;
    }
    self->timer_handler = xTimerCreate("freertos timer", pdMS_TO_TICKS(self->period_ms), self->repeat, self, vTimerCallback);
    if (self->timer_handler == NULL) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("Failed creating FreeRTOS timer"));
    }
    if (xTimerStart(self->timer_handler, 0) != pdPASS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("Failed starting FreeRTOS timer"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(mp_m5utils_timer_init_obj, 1, mp_m5utils_timer_init);

static mp_obj_t mp_m5utils_timer_deinit(mp_obj_t self_in) {
    mp_m5utils_timer_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->timer_handler) {
        xTimerDelete(self->timer_handler, portMAX_DELAY);
        self->timer_handler = NULL;
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mp_m5utils_timer_deinit_obj, mp_m5utils_timer_deinit);



static const mp_rom_map_elem_t mp_m5utils_timer_locals_dict_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_init),     MP_ROM_PTR(&mp_m5utils_timer_init_obj)   },
    { MP_ROM_QSTR(MP_QSTR_deinit),   MP_ROM_PTR(&mp_m5utils_timer_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR___del__),  MP_ROM_PTR(&mp_m5utils_timer_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_ONE_SHOT), MP_ROM_INT(false)                        },
    { MP_ROM_QSTR(MP_QSTR_PERIODIC), MP_ROM_INT(true)                         },
    /* *FORMAT-ON* */
};

static MP_DEFINE_CONST_DICT(mp_m5utils_timer_locals_dict, mp_m5utils_timer_locals_dict_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_m5utils_timer_type,
    MP_QSTR_Timer,
    MP_TYPE_FLAG_NONE,
    make_new, mp_m5utils_timer_make_new,
    print, mp_m5utils_timer_print,
    locals_dict, &mp_m5utils_timer_locals_dict
    );
#else
const mp_obj_type_t mp_m5utils_timer_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Timer,
    .make_new = mp_m5utils_timer_make_new,
    .print = mp_m5utils_timer_print,
    .locals_dict = &mp_m5utils_timer_locals_dict,
};
#endif
