/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <string.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include "py/objarray.h"
#include "py/runtime.h"
#include "py/gc.h"
#include "py/binary.h"
#include "py/stream.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "driver/twai.h"

#define DEBUG 0
#if DEBUG
#define DEBUG_printf(...) mp_printf(&mp_plat_print, __VA_ARGS__)
#else
#define DEBUG_printf(...) (void)0
#endif

// Default timings; 125Kbps
#define CAN_DEFAULT_PRESCALER       (32)
#define CAN_DEFAULT_SJW             (3)
#define CAN_DEFAULT_BS1             (15)
#define CAN_DEFAULT_BS2             (4)

#define CAN_MAXIMUM_NBRP            (512)
#define CAN_MAXIMUM_NBS1            (256)
#define CAN_MAXIMUM_NBS2            (128)
// Minimum Nominal time segment for FDCAN is 2.
#define CAN_MINIMUM_TSEG            (2)

#define CAN_MAXIMUM_DBRP            (32)
#define CAN_MAXIMUM_DBS1            (32)
#define CAN_MAXIMUM_DBS2            (16)

#define CAN_MODE_NORMAL              TWAI_MODE_NORMAL
// #define CAN_MODE_LOOPBACK            TWAI_MODE_LOOPBACK // not supported
// #define CAN_MODE_SILENT              TWAI_MODE_SILENT // not supported
// #define CAN_MODE_SILENT_LOOPBACK     TWAI_MODE_SILENT_LOOPBACK // not supported
#define CAN_MODE_NO_ACKNOWLEDGE_MODE TWAI_MODE_NO_ACK
#define CAN_MODE_LISTEN_ONLY         TWAI_MODE_LISTEN_ONLY


#define CAN_MAX_FILTER              (28)
#define CAN_MAX_DATA_FRAME          (8)


#define CAN_STATE_STOPPED 0
#define CAN_STATE_ERROR_ACTIVE 1
#define CAN_STATE_ERROR_WARNING 2
#define CAN_STATE_ERROR_PASSIVE 3
#define CAN_STATE_BUS_OFF 4
#define CAN_STATE_RECOVERING 5
#define CAN_STATE_RUNNING 6


typedef struct _pyb_can_obj_t {
    mp_obj_base_t base;
    mp_uint_t can_id;
    bool is_enabled;

    twai_timing_config_t t_config;
    twai_general_config_t g_config;
    twai_filter_config_t f_config;
} pyb_can_obj_t;

const mp_obj_type_t pyb_can_type;


// static const twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(2, 1, TWAI_MODE_NORMAL);
// static const twai_timing_config_t t_config = TWAI_TIMING_CONFIG_1MBITS();
// static const twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

STATIC void pyb_can_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (!self->is_enabled) {
        mp_printf(print, "CAN(%u)", self->can_id);
    } else {
        qstr mode;
        switch (self->g_config.mode) {
            case TWAI_MODE_NORMAL:
                mode = MP_QSTR_NORMAL;
                break;
            default:
                mode = MP_QSTR_NORMAL;
                break;
        }
        mp_printf(print, "CAN(%u, CAN.%q, tx=%u, rx=%u, prescaler=%u, sjw=%u, bs1=%u, bs2=%u, triple_sampling=%u)",
            self->can_id,
            mode,
            self->g_config.tx_io,
            self->g_config.rx_io,
            self->t_config.brp,
            self->t_config.sjw,
            self->t_config.tseg_1,
            self->t_config.tseg_2,
            self->t_config.triple_sampling
            );
    }
}

// init(mode, prescaler=100, *, sjw=1, bs1=6, bs2=8)
STATIC mp_obj_t pyb_can_init_helper(pyb_can_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_mode, ARG_tx, ARG_rx, ARG_prescaler, ARG_sjw, ARG_bs1, ARG_bs2, ARG_triple_sampling };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_mode,            MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = CAN_MODE_NORMAL} },
        { MP_QSTR_tx,              MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 2} },
        { MP_QSTR_rx,              MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 1} },
        { MP_QSTR_prescaler,       MP_ARG_INT,                   {.u_int = CAN_DEFAULT_PRESCALER} },
        { MP_QSTR_sjw,             MP_ARG_INT,                   {.u_int = CAN_DEFAULT_SJW} },
        { MP_QSTR_bs1,             MP_ARG_INT,                   {.u_int = CAN_DEFAULT_BS1} },
        { MP_QSTR_bs2,             MP_ARG_INT,                   {.u_int = CAN_DEFAULT_BS2} },
        { MP_QSTR_triple_sampling, MP_ARG_BOOL,                  {.u_bool = false} },
    };

    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    self->t_config.brp = args[ARG_prescaler].u_int;
    self->t_config.tseg_1 = args[ARG_bs1].u_int;
    self->t_config.tseg_2 = args[ARG_bs2].u_int;
    self->t_config.sjw = args[ARG_sjw].u_int;
    self->t_config.triple_sampling = args[ARG_triple_sampling].u_bool;

    self->g_config.tx_io = args[ARG_tx].u_int;
    self->g_config.rx_io = args[ARG_rx].u_int;
    self->g_config.mode = args[ARG_mode].u_int;

    DEBUG_printf(&mp_plat_print, "prescaler=%u, sjw=%u, bs1=%u, bs2=%u, triple_sampling=%u\n", self->t_config.brp, self->t_config.tseg_1, self->t_config.tseg_2, self->t_config.sjw, self->t_config.triple_sampling);
    DEBUG_printf(&mp_plat_print, "mode=%u, tx=%u, rx=%u\n", self->g_config.mode, self->g_config.tx_io, self->g_config.rx_io);

    check_esp_err(twai_driver_install(&self->g_config, &self->t_config, &self->f_config));
    check_esp_err(twai_start());

    self->is_enabled = true;
    return mp_const_none;
}

// CAN(bus, ...)
STATIC mp_obj_t pyb_can_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    // check arguments
    mp_arg_check_num(n_args, n_kw, 3, MP_OBJ_FUN_ARGS_MAX, true);

    // work out port
    mp_uint_t can_idx = mp_obj_get_int(args[0]);

    if (can_idx != 0) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("CAN(%d) doesn't exist"), can_idx);
    }

    pyb_can_obj_t *self;
    if (MP_STATE_PORT(pyb_can_obj_all)[can_idx] == NULL) {
        self = mp_obj_malloc(pyb_can_obj_t, &pyb_can_type);
        self->can_id = can_idx;
        self->is_enabled = false;
        {
            self->t_config.brp = CAN_DEFAULT_PRESCALER;
            self->t_config.tseg_1 = CAN_DEFAULT_BS1;
            self->t_config.tseg_2 = CAN_DEFAULT_BS2;
            self->t_config.sjw = CAN_DEFAULT_SJW;
            self->t_config.triple_sampling = false;
        };
        {
            self->g_config.mode = TWAI_MODE_NORMAL;
            self->g_config.tx_io = 21;
            self->g_config.rx_io = 22;
            self->g_config.clkout_io = TWAI_IO_UNUSED;
            self->g_config.bus_off_io = TWAI_IO_UNUSED;
            self->g_config.tx_queue_len = 5;
            self->g_config.rx_queue_len = 5;
            self->g_config.alerts_enabled = TWAI_ALERT_NONE;
            self->g_config.clkout_divider = 0;
            self->g_config.intr_flags = ESP_INTR_FLAG_LEVEL1;
        };
        {
            self->f_config.acceptance_code = 0;
            self->f_config.acceptance_mask = 0xFFFFFFFF;
            self->f_config.single_filter = true;
        }
        MP_STATE_PORT(pyb_can_obj_all)[can_idx] = self;
    } else {
        self = MP_STATE_PORT(pyb_can_obj_all)[can_idx];
    }

    if (self->is_enabled) {
        // The caller is requesting a reconfiguration of the hardware
        // this can only be done if the hardware is in init mode
        twai_stop();
        check_esp_err(twai_driver_uninstall());
        vTaskDelay(10 / portTICK_PERIOD_MS);
        self->is_enabled = false;
    }

    if (n_args > 1 || n_kw > 0) {
        // start the peripheral
        mp_map_t kw_args;
        mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
        pyb_can_init_helper(self, n_args - 1, args + 1, &kw_args);
    }

    return MP_OBJ_FROM_PTR(self);
}

STATIC mp_obj_t pyb_can_init(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    return pyb_can_init_helper(MP_OBJ_TO_PTR(args[0]), n_args - 1, args + 1, kw_args);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(pyb_can_init_obj, 1, pyb_can_init);

// deinit()
STATIC mp_obj_t pyb_can_deinit(mp_obj_t self_in) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->is_enabled) {
        twai_stop();
        check_esp_err(twai_driver_uninstall());
        self->is_enabled = false;
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(pyb_can_deinit_obj, pyb_can_deinit);

// Force a software restart of the controller, to allow transmission after a bus error
STATIC mp_obj_t pyb_can_restart(mp_obj_t self_in) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->is_enabled) {
        twai_stop();
        check_esp_err(twai_start());
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(pyb_can_restart_obj, pyb_can_restart);

// Get the state of the controller
STATIC mp_obj_t pyb_can_state(mp_obj_t self_in) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(self_in);

    mp_int_t state = CAN_STATE_STOPPED;
    if (self->is_enabled) {
        twai_status_info_t status_info;
        check_esp_err(twai_get_status_info(&status_info));
        if (status_info.state == TWAI_STATE_STOPPED) {
            state = CAN_STATE_STOPPED;
        } else if (status_info.state == TWAI_STATE_RUNNING) {
            state = CAN_STATE_RUNNING;
        } else if (status_info.state == TWAI_STATE_BUS_OFF) {
            state = CAN_STATE_BUS_OFF;
        } else if (status_info.state == TWAI_STATE_RECOVERING) {
            state = CAN_STATE_RECOVERING;
        }
    }
    return MP_OBJ_NEW_SMALL_INT(state);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(pyb_can_state_obj, pyb_can_state);

// Get info about error states and TX/RX buffers
STATIC mp_obj_t pyb_can_info(size_t n_args, const mp_obj_t *args) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    mp_obj_list_t *list;
    if (n_args == 1) {
        list = MP_OBJ_TO_PTR(mp_obj_new_list(8, NULL));
    } else {
        if (!mp_obj_is_type(args[1], &mp_type_list)) {
            mp_raise_TypeError(NULL);
        }
        list = MP_OBJ_TO_PTR(args[1]);
        if (list->len < 8) {
            mp_raise_ValueError(NULL);
        }
    }

    if (self->is_enabled) {
        twai_status_info_t status_info;
        check_esp_err(twai_get_status_info(&status_info));
        list->items[0] = mp_obj_new_int(status_info.tx_error_counter); // TEC value
        list->items[1] = mp_obj_new_int(status_info.rx_error_counter); // REC value
        list->items[2] = mp_obj_new_int(0); // number of times the controller enterted the Error Warning state. ignored for now, compatible with pyb can
        list->items[3] = mp_obj_new_int(0); // number of times the controller enterted the Error Passive state. ignored for now, compatible with pyb can
        list->items[4] = mp_obj_new_int(0); // number of times the controller enterted the Bus Off state. ignored for now, compatible with pyb can
        list->items[5] = mp_obj_new_int(status_info.msgs_to_tx); // number of pending TX messages
        list->items[6] = mp_obj_new_int(status_info.msgs_to_rx); // number of pending RX messages on fifo 0
        list->items[7] = mp_obj_new_int(0); // number of pending RX messages on fifo 1. ignored for now, compatible with pyb can
    }

    return MP_OBJ_FROM_PTR(list);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(pyb_can_info_obj, 1, 2, pyb_can_info);

// any(fifo) - return `True` if any message waiting on the FIFO, else `False`
STATIC mp_obj_t pyb_can_any(mp_obj_t self_in, mp_obj_t fifo_in) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_int_t fifo = mp_obj_get_int(fifo_in); // ignored for now, compatible with pyb can
    if (self->is_enabled) {
        twai_status_info_t status_info;
        check_esp_err(twai_get_status_info(&status_info));
        if (status_info.msgs_to_rx) {
            return mp_const_true;
        } else {
            return mp_const_false;
        }
    }
    return mp_const_false;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(pyb_can_any_obj, pyb_can_any);

// send(send, addr, *, timeout=5000)
STATIC mp_obj_t pyb_can_send(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_data, ARG_id, ARG_timeout, ARG_rtr, ARG_extframe };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_data,     MP_ARG_REQUIRED | MP_ARG_OBJ,   {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_id,       MP_ARG_REQUIRED | MP_ARG_INT,   {.u_int = 0} },
        { MP_QSTR_timeout,  MP_ARG_KW_ONLY | MP_ARG_INT,   {.u_int = 0} },
        { MP_QSTR_rtr,      MP_ARG_KW_ONLY | MP_ARG_BOOL,  {.u_bool = false} },
        { MP_QSTR_extframe, MP_ARG_BOOL,                    {.u_bool = false} },
    };

    // parse args
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // get the buffer to send from
    mp_buffer_info_t bufinfo;
    uint8_t data[1];
    mp_get_buffer_raise(args[ARG_data].u_obj, &bufinfo, MP_BUFFER_READ);

    if (bufinfo.len > CAN_MAX_DATA_FRAME) {
        mp_raise_ValueError(MP_ERROR_TEXT("CAN data field too long"));
    }

    // send the data
    twai_message_t tx_msg = { 0 };
    tx_msg.identifier = args[ARG_id].u_int;
    tx_msg.data_length_code = bufinfo.len;
    memcpy(tx_msg.data, bufinfo.buf, bufinfo.len);
    tx_msg.rtr = args[ARG_rtr].u_bool;
    tx_msg.extd = args[ARG_extframe].u_bool;
    check_esp_err(twai_transmit(&tx_msg, args[ARG_timeout].u_int));
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(pyb_can_send_obj, 1, pyb_can_send);

// recv(fifo, list=None, *, timeout=5000)
STATIC mp_obj_t pyb_can_recv(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_fifo, ARG_list, ARG_timeout };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_fifo,    MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_list,    MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_timeout, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 5000} },
    };

    // parse args
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // receive the data
    twai_message_t rx_msg;
    esp_err_t ret = twai_receive(&rx_msg, args[ARG_timeout].u_int);

    DEBUG_printf(&mp_plat_print, "Received message: %d\n", rx_msg.identifier);
    DEBUG_printf(&mp_plat_print, "Received message: %d\n", rx_msg.data_length_code);
    DEBUG_printf(&mp_plat_print, "Received message: %s\n", rx_msg.data);

    if (ret != ESP_OK || rx_msg.data_length_code > 8) {
        return mp_const_none;
    }

    // Create the tuple, or get the list, that will hold the return values
    // Also populate the fifth element, either a new bytes or reuse existing memoryview
    mp_obj_t ret_obj = args[ARG_list].u_obj;
    mp_obj_t *items;
    if (ret_obj == mp_const_none) {
        ret_obj = mp_obj_new_tuple(5, NULL);
        items = ((mp_obj_tuple_t *)MP_OBJ_TO_PTR(ret_obj))->items;
        items[4] = mp_obj_new_bytes(rx_msg.data, rx_msg.data_length_code);
    } else {
        // User should provide a list of length at least 5 to hold the values
        if (!mp_obj_is_type(ret_obj, &mp_type_list)) {
            mp_raise_TypeError(NULL);
        }
        mp_obj_list_t *list = MP_OBJ_TO_PTR(ret_obj);
        if (list->len < 5) {
            mp_raise_ValueError(NULL);
        }
        items = list->items;
        // Fifth element must be a memoryview which we assume points to a
        // byte-like array which is large enough, and then we resize it inplace
        if (!mp_obj_is_type(items[4], &mp_type_memoryview)) {
            mp_raise_TypeError(NULL);
        }
        mp_obj_array_t *mv = MP_OBJ_TO_PTR(items[4]);
        if (!(mv->typecode == (MP_OBJ_ARRAY_TYPECODE_FLAG_RW | BYTEARRAY_TYPECODE)
              || (mv->typecode | 0x20) == (MP_OBJ_ARRAY_TYPECODE_FLAG_RW | 'b'))) {
            mp_raise_ValueError(NULL);
        }
        mv->len = rx_msg.data_length_code;
        memcpy(mv->items, rx_msg.data, rx_msg.data_length_code);
    }

    // Populate the first 4 values of the tuple/list
    items[0] = mp_obj_new_int(rx_msg.identifier);
    items[1] = mp_obj_new_bool(rx_msg.extd);
    items[2] = rx_msg.rtr ? mp_const_true : mp_const_false;
    items[3] = mp_obj_new_int(0xFF);

    // Return the result
    return ret_obj;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(pyb_can_recv_obj, 1, pyb_can_recv);

STATIC mp_obj_t pyb_can_clearfilter(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_extframe };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_extframe, MP_ARG_BOOL, {.u_bool = false} },
    };

    // parse args
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_int_t f = mp_obj_get_int(pos_args[1]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 2, pos_args + 2, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // TODO: implement filter

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(pyb_can_clearfilter_obj, 2, pyb_can_clearfilter);

// setfilter(bank, mode, fifo, params, *, rtr)
#define EXTENDED_ID_TO_16BIT_FILTER(id) (((id & 0xC00000) >> 13) | ((id & 0x38000) >> 15)) | 8
STATIC mp_obj_t pyb_can_setfilter(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_bank, ARG_mode, ARG_fifo, ARG_params, ARG_rtr, ARG_extframe };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_bank,     MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} }, // ignored for now, compatible with pyb can
        { MP_QSTR_mode,     MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_fifo,     MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} }, // ignored for now, compatible with pyb can
        { MP_QSTR_params,   MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_rtr,      MP_ARG_KW_ONLY | MP_ARG_OBJ,  {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_extframe, MP_ARG_BOOL,                  {.u_bool = false} },
    };

    // parse args
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // TODO: implement filter

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(pyb_can_setfilter_obj, 1, pyb_can_setfilter);

STATIC const mp_rom_map_elem_t pyb_can_locals_dict_table[] = {
    // instance methods
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&pyb_can_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&pyb_can_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_restart), MP_ROM_PTR(&pyb_can_restart_obj) },
    { MP_ROM_QSTR(MP_QSTR_state), MP_ROM_PTR(&pyb_can_state_obj) },
    { MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&pyb_can_info_obj) },
    { MP_ROM_QSTR(MP_QSTR_any), MP_ROM_PTR(&pyb_can_any_obj) },
    { MP_ROM_QSTR(MP_QSTR_send), MP_ROM_PTR(&pyb_can_send_obj) },
    { MP_ROM_QSTR(MP_QSTR_recv), MP_ROM_PTR(&pyb_can_recv_obj) },
    { MP_ROM_QSTR(MP_QSTR_setfilter), MP_ROM_PTR(&pyb_can_setfilter_obj) },
    { MP_ROM_QSTR(MP_QSTR_clearfilter), MP_ROM_PTR(&pyb_can_clearfilter_obj) },

    // class constants
    // Note: we use the ST constants >> 4 so they fit in a small-int.  The
    // right-shift is undone when the constants are used in the init function.
    { MP_ROM_QSTR(MP_QSTR_NORMAL), MP_ROM_INT(CAN_MODE_NORMAL) },
    // { MP_ROM_QSTR(MP_QSTR_LOOPBACK), MP_ROM_INT(CAN_MODE_LOOPBACK) },
    // { MP_ROM_QSTR(MP_QSTR_SILENT), MP_ROM_INT(CAN_MODE_SILENT) },
    // { MP_ROM_QSTR(MP_QSTR_SILENT_LOOPBACK), MP_ROM_INT(CAN_MODE_SILENT_LOOPBACK) },
    { MP_ROM_QSTR(MP_QSTR_NO_ACKNOWLEDGE), MP_ROM_INT(CAN_MODE_NO_ACKNOWLEDGE_MODE) },
    { MP_ROM_QSTR(MP_QSTR_LISTEN_ONLY), MP_ROM_INT(CAN_MODE_LISTEN_ONLY) },

    { MP_ROM_QSTR(MP_QSTR_MASK16), MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_LIST16), MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_MASK32), MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_LIST32), MP_ROM_INT(3) },

    // { MP_ROM_QSTR(MP_QSTR_DUAL), MP_ROM_INT(0) },  // not supported
    // { MP_ROM_QSTR(MP_QSTR_RANGE), MP_ROM_INT(1) }, // not supported
    // { MP_ROM_QSTR(MP_QSTR_MASK), MP_ROM_INT(2) }, // not supported

    // values for CAN.state()
    { MP_ROM_QSTR(MP_QSTR_STOPPED), MP_ROM_INT(CAN_STATE_STOPPED) },
    { MP_ROM_QSTR(MP_QSTR_ERROR_ACTIVE), MP_ROM_INT(CAN_STATE_ERROR_ACTIVE) },
    { MP_ROM_QSTR(MP_QSTR_ERROR_WARNING), MP_ROM_INT(CAN_STATE_ERROR_WARNING) },
    { MP_ROM_QSTR(MP_QSTR_ERROR_PASSIVE), MP_ROM_INT(CAN_STATE_ERROR_PASSIVE) },
    { MP_ROM_QSTR(MP_QSTR_BUS_OFF), MP_ROM_INT(CAN_STATE_BUS_OFF) },
    { MP_ROM_QSTR(MP_QSTR_RECOVERING), MP_ROM_INT(CAN_STATE_RECOVERING) },
    { MP_ROM_QSTR(MP_QSTR_RUNNING), MP_ROM_INT(CAN_STATE_RUNNING) },
};
STATIC MP_DEFINE_CONST_DICT(pyb_can_locals_dict, pyb_can_locals_dict_table);

STATIC mp_uint_t can_ioctl(mp_obj_t self_in, mp_uint_t request, uintptr_t arg, int *errcode) {
    pyb_can_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_uint_t ret = 0;
    return ret;
}

STATIC const mp_stream_p_t can_stream_p = {
    // .read = can_read, // is read sensible for CAN?
    // .write = can_write, // is write sensible for CAN?
    .ioctl = can_ioctl,
    .is_text = false,
};

MP_DEFINE_CONST_OBJ_TYPE(
    pyb_can_type,
    MP_QSTR_CAN,
    MP_TYPE_FLAG_NONE,
    make_new, pyb_can_make_new,
    print, pyb_can_print,
    protocol, &can_stream_p,
    locals_dict, &pyb_can_locals_dict
    );

MP_REGISTER_ROOT_POINTER(struct _pyb_can_obj_t *pyb_can_obj_all[1]);

STATIC const mp_rom_map_elem_t m5can_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_m5can) },
    { MP_ROM_QSTR(MP_QSTR_CAN), MP_ROM_PTR(&pyb_can_type) },
};

STATIC MP_DEFINE_CONST_DICT(m5can_module_globals, m5can_module_globals_table);

const mp_obj_module_t m5can_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&m5can_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_m5can, m5can_module);
