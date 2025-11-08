/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <stdio.h>

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objlist.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "mphalport.h"

#include "max30100.h"

typedef struct _cdriver_max30100_obj_t {
    mp_obj_base_t base;
    mp_obj_t i2c_obj;
    uint8_t address;
    mp_obj_t readfrom_mem_method[2];
    mp_obj_t writeto_mem_method[2];
    max30100_config_t *max30100;
    int heart_bpm;
    int spo2;
    int ir;
    int red;
} cdriver_max30100_obj_t;

extern const mp_obj_type_t cdriver_max30100_type;

static int8_t i2c_bus_read(uint8_t addr, uint8_t reg, uint8_t *out_data, uint32_t len, void *intf_ptr) {
    cdriver_max30100_obj_t *self = (cdriver_max30100_obj_t *)intf_ptr;
    mp_obj_t args[3];
    const char *buf;
    size_t out_len = 0;

    args[0] = mp_obj_new_int(addr);
    args[1] = mp_obj_new_int(reg);
    args[2] = mp_obj_new_int(len);

    // mp_printf(&mp_plat_print, "addr: 0x%x, reg: 0x%x\n", addr, reg);

    mp_obj_t ret = mp_call_method_self_n_kw(
        self->readfrom_mem_method[0],
        self->readfrom_mem_method[1],
        3,
        0,
        args
        );

    buf = mp_obj_str_get_data(ret, &out_len);
    memcpy(out_data, buf, out_len);

    return 0;
}

static int8_t i2c_bus_write(uint8_t addr, uint8_t reg, const uint8_t *in_data, uint32_t len, void *intf_ptr) {
    cdriver_max30100_obj_t *self = (cdriver_max30100_obj_t *)intf_ptr;
    mp_obj_t args[3];
    const char *buf;
    size_t l = 0;

    args[0] = mp_obj_new_int(addr);
    args[1] = mp_obj_new_int(reg);
    args[2] = mp_obj_new_bytes(in_data, len);

    mp_obj_t ret = mp_call_method_self_n_kw(
        self->writeto_mem_method[0],
        self->writeto_mem_method[1],
        3,
        0,
        args
        );

    return 0;
}

static mp_obj_t cdriver_max30100_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args_in) {
    enum { ARG_i2c, ARG_address, };
    mp_map_t kw_args;

    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);
    mp_map_init_fixed_table(&kw_args, n_kw, args_in + n_args);
    static const mp_arg_t allowed_args[] = {
        /* *FORMAT-OFF* */
        { MP_QSTR_i2c,     MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_address, MP_ARG_KW_ONLY | MP_ARG_INT,  {.u_int = 0x57}        },
        /* *FORMAT-ON* */
    };
    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, args_in, &kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    cdriver_max30100_obj_t *self = mp_obj_malloc(cdriver_max30100_obj_t, &cdriver_max30100_type);
    self->i2c_obj = args[ARG_i2c].u_obj;
    self->address = args[ARG_address].u_int;
    mp_load_method_maybe(self->i2c_obj, MP_QSTR_writeto_mem, self->writeto_mem_method);
    mp_load_method_maybe(self->i2c_obj, MP_QSTR_readfrom_mem, self->readfrom_mem_method);
    self->max30100 = (max30100_config_t *)m_malloc(sizeof(max30100_config_t));
    self->max30100->intf_ptr = self;
    self->max30100->i2c_bus_read = i2c_bus_read;
    self->max30100->i2c_bus_write = i2c_bus_write;

    ESP_ERROR_CHECK(max30100_init(
        self->max30100,
        self->address,
        MAX30100_DEFAULT_OPERATING_MODE,
        MAX30100_DEFAULT_SAMPLING_RATE,
        MAX30100_DEFAULT_LED_PULSE_WIDTH,
        MAX30100_DEFAULT_IR_LED_CURRENT,
        MAX30100_DEFAULT_START_RED_LED_CURRENT,
        MAX30100_DEFAULT_MEAN_FILTER_SIZE,
        MAX30100_DEFAULT_PULSE_BPM_SAMPLE_SIZE,
        true, false));

    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t cdriver_max30100_get_heart_rate(mp_obj_t self_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    return mp_obj_new_int(self->heart_bpm);
}
MP_DEFINE_CONST_FUN_OBJ_1(cdriver_max30100_get_heart_rate_obj, cdriver_max30100_get_heart_rate);

static mp_obj_t cdriver_max30100_get_spo2(mp_obj_t self_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    return mp_obj_new_int(self->spo2);
}
MP_DEFINE_CONST_FUN_OBJ_1(cdriver_max30100_get_spo2_obj, cdriver_max30100_get_spo2);

static mp_obj_t cdriver_max30100_get_ir(mp_obj_t self_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    return mp_obj_new_int(self->ir);
}
MP_DEFINE_CONST_FUN_OBJ_1(cdriver_max30100_get_ir_obj, cdriver_max30100_get_ir);

static mp_obj_t cdriver_max30100_get_red(mp_obj_t self_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    return mp_obj_new_int(self->red);
}
MP_DEFINE_CONST_FUN_OBJ_1(cdriver_max30100_get_red_obj, cdriver_max30100_get_red);

static mp_obj_t cdriver_max30100_set_mode(mp_obj_t self_in, mp_obj_t mode_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint8_t mode = mp_obj_get_int(mode_in);

    max30100_set_mode(self->max30100, mode);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(cdriver_max30100_set_mode_obj, cdriver_max30100_set_mode);

static mp_obj_t cdriver_max30100_set_led_current(mp_obj_t self_in, mp_obj_t red, mp_obj_t ir) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint8_t red_current = mp_obj_get_int(red);
    uint8_t ir_current = mp_obj_get_int(ir);

    max30100_set_led_current(self->max30100, red_current, ir_current);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_3(cdriver_max30100_set_led_current_obj, cdriver_max30100_set_led_current);

static mp_obj_t cdriver_max30100_update(mp_obj_t self_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    max30100_data_t result = {};

    esp_err_t ret = max30100_update(self->max30100, &result);

    if (ret != ESP_OK) {
        printf("error\n");
    }

    self->ir = result.ir_raw;
    self->red = result.red_raw;

    if (result.pulse_detected) {
        self->heart_bpm = (int)result.heart_bpm;
        self->spo2 = (int)result.spO2;
        if (self->spo2 < 95) {
            self->spo2 += 5;
        }
    } else {
        if ((self->ir == 0) && (self->red == 0)) {
            self->heart_bpm = 0;
            self->spo2 = 0;
        }
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(cdriver_max30100_update_obj, cdriver_max30100_update);

static mp_obj_t cdriver_max30100_set_pulse_width(mp_obj_t self_in, mp_obj_t pw) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint8_t pulse_width = mp_obj_get_int(pw);

    max30100_set_pulse_width(self->max30100, pulse_width);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(cdriver_max30100_set_pulse_width_obj, cdriver_max30100_set_pulse_width);

static mp_obj_t cdriver_max30100_set_sampling_rate(mp_obj_t self_in, mp_obj_t rate) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint8_t sampling_rate = mp_obj_get_int(rate);

    max30100_set_sampling_rate(self->max30100, sampling_rate);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(cdriver_max30100_set_sampling_rate_obj, cdriver_max30100_set_sampling_rate);


static mp_obj_t cdriver_max30100_deinit(mp_obj_t self_in) {
    cdriver_max30100_obj_t *self = MP_OBJ_TO_PTR(self_in);
    self->heart_bpm = 0;
    self->spo2 = 0;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(cdriver_max30100_deinit_obj, cdriver_max30100_deinit);


static const mp_rom_map_elem_t cdriver_max30100_globals_dict_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_get_heart_rate),    MP_ROM_PTR(&cdriver_max30100_get_heart_rate_obj)    },
    { MP_ROM_QSTR(MP_QSTR_get_spo2),          MP_ROM_PTR(&cdriver_max30100_get_spo2_obj)          },
    { MP_ROM_QSTR(MP_QSTR_get_ir),            MP_ROM_PTR(&cdriver_max30100_get_ir_obj)            },
    { MP_ROM_QSTR(MP_QSTR_get_red),           MP_ROM_PTR(&cdriver_max30100_get_red_obj)           },

    { MP_ROM_QSTR(MP_QSTR_set_mode),          MP_ROM_PTR(&cdriver_max30100_set_mode_obj)          },
    { MP_ROM_QSTR(MP_QSTR_set_led_current),   MP_ROM_PTR(&cdriver_max30100_set_led_current_obj)   },

    { MP_ROM_QSTR(MP_QSTR_update),            MP_ROM_PTR(&cdriver_max30100_update_obj)            },
    { MP_ROM_QSTR(MP_QSTR_set_pulse_width),   MP_ROM_PTR(&cdriver_max30100_set_pulse_width_obj)   },
    { MP_ROM_QSTR(MP_QSTR_set_sampling_rate), MP_ROM_PTR(&cdriver_max30100_set_sampling_rate_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit),            MP_ROM_PTR(&cdriver_max30100_deinit_obj)            },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(cdriver_max30100_locals_dict, cdriver_max30100_globals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    cdriver_max30100_type,
    MP_QSTR_MAX30100,
    MP_TYPE_FLAG_NONE,
    make_new, cdriver_max30100_make_new,
    locals_dict, &cdriver_max30100_locals_dict
    );
