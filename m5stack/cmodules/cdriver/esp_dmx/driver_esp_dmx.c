/*
 * Copyright (c) 2024 M5Stack Technology CO LTD
 */
#include "esp_dmx.h"

#include <math.h>
#include <string.h>

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objlist.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "mphalport.h"

#include "dmx/include/driver.h"
#include "driver/gpio.h"
#include "driver/periph_ctrl.h"
#include "driver/uart.h"
#include "esp_log.h"
#include "soc/io_mux_reg.h"
#include "soc/gpio_periph.h"
#include <rom/gpio.h>
#include <rom/ets_sys.h>

static uint8_t dmx_data[DMX_PACKET_SIZE] = {};  // Buffer to store DMX data
dmx_port_t dmxPort;
bool dmxIsConnected = false;

STATIC mp_obj_t mp_dmx_init(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_port_id, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 1}},
        {MP_QSTR_tx_pin, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 13}},  // 1us resolution
        {MP_QSTR_rx_pin, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 35}},
        {MP_QSTR_en_pin, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 12}},
        {MP_QSTR_sel_mode, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 1}},
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    dmxPort = args[0].u_int;
    mp_uint_t tx_pin = args[1].u_int;
    mp_uint_t rx_pin = args[2].u_int;
    mp_uint_t en_pin = args[3].u_int;
    mp_uint_t sel_mode = args[4].u_int;

    dmx_config_t dmxConfig = DMX_CONFIG_DEFAULT;

    if (sel_mode == 1) {
        const int personality_count = 0;
        dmx_driver_install(dmxPort, &dmxConfig, NULL, personality_count);
        dmx_set_pin(dmxPort, tx_pin, rx_pin, en_pin);
    } else if (sel_mode == 2) {
        dmx_personality_t personalities[] = {{1, "Default Personality"}};
        const int personality_count = 1;
        dmx_driver_install(dmxPort, &dmxConfig, personalities, personality_count);
        dmx_set_pin(dmxPort, tx_pin, rx_pin, en_pin);
    }

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(mp_dmx_init_obj, 5, mp_dmx_init);

STATIC mp_obj_t mp_dmx_write_data(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_channel, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 1}},
        {MP_QSTR_ch_data, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0}},  // 1us resolution
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    mp_uint_t channel = args[0].u_int;
    mp_uint_t ch_data = args[1].u_int;

    dmx_data[channel] = ch_data;
    // mp_printf(&mp_plat_print, "Channel %d set to%d\n", channel, ch_data);
    // mp_printf(&mp_plat_print, "bytes written DMX:%d", dmx_write(dmxPort, dmx_data, DMX_PACKET_SIZE));
    // mp_printf(&mp_plat_print, "bytes sent DMX:%d", dmx_send_num(dmxPort, DMX_PACKET_SIZE));
    // mp_printf(&mp_plat_print, "is done sending:%d", dmx_wait_sent(dmxPort, DMX_TIMEOUT_TICK));
    dmx_write(dmxPort, dmx_data, DMX_PACKET_SIZE);
    dmx_send_num(dmxPort, DMX_PACKET_SIZE);
    dmx_wait_sent(dmxPort, DMX_TIMEOUT_TICK);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(mp_dmx_write_data_obj, 2, mp_dmx_write_data);

STATIC mp_obj_t mp_dmx_read_data(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_channel, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 1}},
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    mp_uint_t channel = args[0].u_int;
    dmx_packet_t packet;
    bool is_connected = false;
    if (dmx_receive(dmxPort, &packet, DMX_TIMEOUT_TICK)) {
        if (dmx_receive(dmxPort, &packet, DMX_TIMEOUT_TICK)) {
            if (!is_connected) {
                // Log when we first connect
                // ESP_LOGI(TAG, "DMX is connected.");
                is_connected = true;
            }
            dmx_read(dmxPort, dmx_data, DMX_PACKET_SIZE);
        }
    }
    return mp_obj_new_int(dmx_data[channel]);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(mp_dmx_read_data_obj, 1, mp_dmx_read_data);

STATIC mp_obj_t mp_dmx_clear_buffer() {
    memset(dmx_data, 0, DMX_PACKET_SIZE);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mp_dmx_clear_buffer_obj, mp_dmx_clear_buffer);

STATIC mp_obj_t mp_dmx_delete_port() {
    dmx_driver_delete(dmxPort);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mp_dmx_delete_port_obj, mp_dmx_delete_port);

STATIC mp_obj_t mp_dmx_deinit() {
    dmx_driver_delete(dmxPort);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mp_dmx_deinit_obj, mp_dmx_deinit);

STATIC const mp_rom_map_elem_t esp_dmx_globals_dict_table[] = {
    {MP_ROM_QSTR(MP_QSTR_dmx_init), (mp_obj_t)&mp_dmx_init_obj},
    {MP_ROM_QSTR(MP_QSTR_dmx_write_data), (mp_obj_t)&mp_dmx_write_data_obj},
    {MP_ROM_QSTR(MP_QSTR_dmx_read_data), (mp_obj_t)&mp_dmx_read_data_obj},
    {MP_ROM_QSTR(MP_QSTR_dmx_clear_buffer), (mp_obj_t)&mp_dmx_clear_buffer_obj},
    {MP_ROM_QSTR(MP_QSTR_dmx_delete_port), (mp_obj_t)&mp_dmx_delete_port_obj},
    {MP_ROM_QSTR(MP_QSTR_dmx_deinit), (mp_obj_t)&mp_dmx_deinit_obj},
};

STATIC MP_DEFINE_CONST_DICT(esp_dmx_globals_dict, esp_dmx_globals_dict_table);

const mp_obj_module_t mp_module_esp_dmx = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&esp_dmx_globals_dict,
};
