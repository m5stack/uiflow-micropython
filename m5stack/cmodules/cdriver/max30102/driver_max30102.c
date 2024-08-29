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

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "driver/gpio.h"
#include "esp_system.h"
#include "esp_err.h"
#include "esp_log.h"

#include "esp_task.h"

#include "include/max30102/max30102.h"

// static volatile TaskHandle_t max30102_handle = NULL;

static max30102_config_t max30102 = {};

static volatile int _heart_bpm, previous_heart_bpm, previous_spo2, _spo2, _ir, _red, _curr_mode;

typedef struct _max30102_hw_i2c_obj_t {
    mp_obj_base_t base;
    uint8_t pos;
    i2c_port_t port;
} max30102_hw_i2c_obj_t;

STATIC mp_obj_t mp_MAX30102_get_heart_rate(void) {
    if (_heart_bpm > 0) {
        if (_heart_bpm > 60 && _heart_bpm < 120) {
            previous_heart_bpm = _heart_bpm;
        }
        if (_heart_bpm < 60 || _heart_bpm > 120) {
            _heart_bpm = previous_heart_bpm;
        }
    }
    return mp_obj_new_int(_heart_bpm);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30102_get_heart_rate_obj, mp_MAX30102_get_heart_rate);

STATIC mp_obj_t mp_MAX30102_get_spo2(void) {
    if (_curr_mode == MAX30102_MODE_SPO2_HR && _spo2 > 0) {
        if (_spo2 >= 80 && _spo2 <= 100) {
            previous_spo2 = _spo2;
        }
        if (_spo2 < 80 || _spo2 > 100) {
            _spo2 = previous_spo2;
        }
    } else {
        _spo2 = 0;
    }
    return mp_obj_new_int(_spo2);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30102_get_spo2_obj, mp_MAX30102_get_spo2);

STATIC mp_obj_t mp_MAX30102_get_ir(void) {
    return mp_obj_new_int(_ir);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30102_get_ir_obj, mp_MAX30102_get_ir);


STATIC mp_obj_t mp_MAX30102_get_red(void) {
    return mp_obj_new_int(_red);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30102_get_red_obj, mp_MAX30102_get_red);


STATIC mp_obj_t mp_MAX30102_update(void) {
    max30102_data_t result = {};

    esp_err_t ret = max30102_update(&max30102, &result);

    if (ret != ESP_OK) {
        printf("error\n");
    }

    _ir = result.ir_raw;
    _red = result.red_raw;

    if ((_ir > 2000) && (_red > 2000)) {
        if (result.pulse_detected) {
            _heart_bpm = (int)result.heart_bpm;
            _spo2 = (int)result.spO2;
            if (_spo2 < 95) {
                _spo2 += 5;
            }
        }
    } else {
        _heart_bpm = 0;
        _spo2 = 0;
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30102_update_obj, mp_MAX30102_update);

STATIC mp_obj_t mp_MAX30102_init(mp_obj_t i2c_bus_in, mp_obj_t addr_in) {
    max30102_hw_i2c_obj_t *i2c_bus = (max30102_hw_i2c_obj_t *)i2c_bus_in;
    max30102.i2c_num = i2c_bus->port;
    max30102.device_pos = i2c_bus->pos;

    max30102.i2c_addr = mp_obj_get_int(addr_in);
    // printf("id :%d, pos: %d\n", max30102.i2c_num, max30102.device_pos);

    ESP_ERROR_CHECK(max30102_init(&max30102, max30102.i2c_num,
        MAX30102_DEFAULT_OPERATING_MODE,
        MAX30102_DEFAULT_SAMPLING_RATE,
        MAX30102_DEFAULT_LED_PULSE_WIDTH,
        MAX30102_DEFAULT_IR_LED_CURRENT,
        MAX30102_DEFAULT_START_RED_LED_CURRENT,
        MAX30102_ADC_RANGE_16384,
        MAX30102_DEFAULT_MEAN_FILTER_SIZE,
        MAX30102_DEFAULT_PULSE_BPM_SAMPLE_SIZE,
        false));
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mp_MAX30102_init_obj, mp_MAX30102_init);

STATIC mp_obj_t mp_MAX30102_set_mode(mp_obj_t mode_in) {

    uint8_t mode = mp_obj_get_int(mode_in);
    _curr_mode = mode;
    max30102_set_mode(&max30102, mode);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mp_MAX30102_set_mode_obj, mp_MAX30102_set_mode);

STATIC mp_obj_t mp_MAX30102_set_led_current(mp_obj_t red, mp_obj_t ir) {

    uint8_t red_current = mp_obj_get_int(red);
    uint8_t ir_current = mp_obj_get_int(ir);

    max30102_set_led_current(&max30102, red_current, ir_current);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mp_MAX30102_set_led_current_obj, mp_MAX30102_set_led_current);


STATIC mp_obj_t mp_MAX30102_set_plus_width(mp_obj_t pw) {

    uint8_t plus_width = mp_obj_get_int(pw);

    max30102_set_pulse_width(&max30102, plus_width);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mp_MAX30102_set_plus_width_obj, mp_MAX30102_set_plus_width);

STATIC mp_obj_t mp_MAX30102_set_sampling_rate(mp_obj_t rate) {

    uint8_t sampling_rate = mp_obj_get_int(rate);

    max30102_set_sampling_rate(&max30102, sampling_rate);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mp_MAX30102_set_sampling_rate_obj, mp_MAX30102_set_sampling_rate);


STATIC mp_obj_t mp_MAX30102_deinit(void) {
    _heart_bpm = 0;
    _spo2 = 0;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30102_deinit_obj, mp_MAX30102_deinit);


STATIC const mp_rom_map_elem_t max30102_globals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_init),           (mp_obj_t)&mp_MAX30102_init_obj },
    { MP_ROM_QSTR(MP_QSTR_get_heart_rate),  (mp_obj_t)&mp_MAX30102_get_heart_rate_obj },
    { MP_ROM_QSTR(MP_QSTR_get_spo2),       (mp_obj_t)&mp_MAX30102_get_spo2_obj },
    { MP_ROM_QSTR(MP_QSTR_get_ir),         (mp_obj_t)&mp_MAX30102_get_ir_obj },
    { MP_ROM_QSTR(MP_QSTR_get_red),        (mp_obj_t)&mp_MAX30102_get_red_obj },

    { MP_ROM_QSTR(MP_QSTR_set_mode),       (mp_obj_t)&mp_MAX30102_set_mode_obj },
    { MP_ROM_QSTR(MP_QSTR_set_led_current),(mp_obj_t)&mp_MAX30102_set_led_current_obj },

    { MP_ROM_QSTR(MP_QSTR_update),         (mp_obj_t)&mp_MAX30102_update_obj },
    { MP_ROM_QSTR(MP_QSTR_set_plus_width), (mp_obj_t)&mp_MAX30102_set_plus_width_obj},
    { MP_ROM_QSTR(MP_QSTR_set_sampling_rate), (mp_obj_t)&mp_MAX30102_set_sampling_rate_obj},
    { MP_ROM_QSTR(MP_QSTR_deinit),         (mp_obj_t)&mp_MAX30102_deinit_obj}
};

STATIC MP_DEFINE_CONST_DICT(max30102_globals_dict, max30102_globals_dict_table);

const mp_obj_module_t mp_module_max30102 = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&max30102_globals_dict,
};
