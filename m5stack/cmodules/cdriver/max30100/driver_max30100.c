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

#include "include/max30100/max30100.h"

// static volatile TaskHandle_t max30100_handle = NULL;

static max30100_config_t max30100 = {};

static volatile int _heart_bpm, _spo2, _ir, _red;

typedef struct _max30100_hw_i2c_obj_t {
    mp_obj_base_t base;
    uint8_t pos;
    i2c_port_t port;
} max30100_hw_i2c_obj_t;

STATIC mp_obj_t mp_MAX30100_get_HeartRate(void) {
    return mp_obj_new_int(_heart_bpm);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30100_get_HeartRate_obj, mp_MAX30100_get_HeartRate);

STATIC mp_obj_t mp_MAX30100_get_SpO2(void) {
    return mp_obj_new_int(_spo2);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30100_get_SpO2_obj, mp_MAX30100_get_SpO2);

STATIC mp_obj_t mp_MAX30100_get_ir(void) {
    return mp_obj_new_int(_ir);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30100_get_ir_obj, mp_MAX30100_get_ir);


STATIC mp_obj_t mp_MAX30100_get_red(void) {
    return mp_obj_new_int(_red);
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30100_get_red_obj, mp_MAX30100_get_red);


STATIC mp_obj_t mp_MAX30100_update(void) {
    max30100_data_t result = {};

    esp_err_t ret = max30100_update(&max30100, &result);

    if (ret != ESP_OK) {
        printf("error\n");
    }

    _ir = result.ir_raw;
    _red = result.red_raw;

    if (result.pulse_detected) {
        _heart_bpm = (int)result.heart_bpm;
        _spo2 = (int)result.spO2;
        if (_spo2 < 95) {
            _spo2 += 5;
        }
    } else {
        if ((_ir == 0) && (_red == 0)) {
            _heart_bpm = 0;
            _spo2 = 0;
        }
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30100_update_obj, mp_MAX30100_update);

STATIC mp_obj_t mp_MAX30100_init(mp_obj_t i2c_bus_in, mp_obj_t addr_in) {
    max30100_hw_i2c_obj_t *i2c_bus = (max30100_hw_i2c_obj_t *)i2c_bus_in;
    max30100.device_pos = i2c_bus->pos;
    max30100.i2c_num = i2c_bus->port;

    max30100.i2c_addr = mp_obj_get_int(addr_in);
    // printf("id :%d, pos: %d, addr: %02X\n", max30100.i2c_num, max30100.device_pos, max30100.i2c_addr);

    ESP_ERROR_CHECK(max30100_init(&max30100, max30100.i2c_num,
        MAX30100_DEFAULT_OPERATING_MODE,
        MAX30100_DEFAULT_SAMPLING_RATE,
        MAX30100_DEFAULT_LED_PULSE_WIDTH,
        MAX30100_DEFAULT_IR_LED_CURRENT,
        MAX30100_DEFAULT_START_RED_LED_CURRENT,
        MAX30100_DEFAULT_MEAN_FILTER_SIZE,
        MAX30100_DEFAULT_PULSE_BPM_SAMPLE_SIZE,
        true, false));
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mp_MAX30100_init_obj, mp_MAX30100_init);

STATIC mp_obj_t mp_MAX30100_set_mode(mp_obj_t mode_in) {

    uint8_t mode = mp_obj_get_int(mode_in);

    max30100_set_mode(&max30100, mode);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mp_MAX30100_set_mode_obj, mp_MAX30100_set_mode);

STATIC mp_obj_t mp_MAX30100_set_led_current(mp_obj_t red, mp_obj_t ir) {

    uint8_t red_current = mp_obj_get_int(red);
    uint8_t ir_current = mp_obj_get_int(ir);

    max30100_set_led_current(&max30100, red_current, ir_current);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mp_MAX30100_set_led_current_obj, mp_MAX30100_set_led_current);


STATIC mp_obj_t mp_MAX30100_set_pulse_width(mp_obj_t pw) {

    uint8_t plus_width = mp_obj_get_int(pw);

    max30100_set_pulse_width(&max30100, plus_width);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mp_MAX30100_set_pulse_width_obj, mp_MAX30100_set_pulse_width);

STATIC mp_obj_t mp_MAX30100_set_sampling_rate(mp_obj_t rate) {

    uint8_t sampling_rate = mp_obj_get_int(rate);

    max30100_set_sampling_rate(&max30100, sampling_rate);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mp_MAX30100_set_sampling_rate_obj, mp_MAX30100_set_sampling_rate);


STATIC mp_obj_t mp_MAX30100_deinit(void) {
    _heart_bpm = 0;
    _spo2 = 0;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mp_MAX30100_deinit_obj, mp_MAX30100_deinit);


STATIC const mp_rom_map_elem_t max30100_globals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_init),           (mp_obj_t)&mp_MAX30100_init_obj },
    { MP_ROM_QSTR(MP_QSTR_get_heart_rate),  (mp_obj_t)&mp_MAX30100_get_HeartRate_obj },
    { MP_ROM_QSTR(MP_QSTR_get_spo2),       (mp_obj_t)&mp_MAX30100_get_SpO2_obj },
    { MP_ROM_QSTR(MP_QSTR_get_ir),         (mp_obj_t)&mp_MAX30100_get_ir_obj },
    { MP_ROM_QSTR(MP_QSTR_get_red),        (mp_obj_t)&mp_MAX30100_get_red_obj },

    { MP_ROM_QSTR(MP_QSTR_set_mode),       (mp_obj_t)&mp_MAX30100_set_mode_obj },
    { MP_ROM_QSTR(MP_QSTR_set_led_current),(mp_obj_t)&mp_MAX30100_set_led_current_obj },

    { MP_ROM_QSTR(MP_QSTR_update),         (mp_obj_t)&mp_MAX30100_update_obj },
    { MP_ROM_QSTR(MP_QSTR_set_pulse_width), (mp_obj_t)&mp_MAX30100_set_pulse_width_obj},
    { MP_ROM_QSTR(MP_QSTR_set_sampling_rate), (mp_obj_t)&mp_MAX30100_set_sampling_rate_obj},
    { MP_ROM_QSTR(MP_QSTR_deinit),         (mp_obj_t)&mp_MAX30100_deinit_obj}
};

STATIC MP_DEFINE_CONST_DICT(max30100_globals_dict, max30100_globals_dict_table);

const mp_obj_module_t mp_module_max30100 = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&max30100_globals_dict,
};
