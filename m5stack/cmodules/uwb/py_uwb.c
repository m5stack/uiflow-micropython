/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <stdbool.h>
#include <stdint.h>

#include "deca_device_api.h"
#include "deca_interface.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "py/obj.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "uwb_port.h"

#define UWB_MAX_PAYLOAD 125
#define UWB_FCS_LENGTH 2

extern const struct dwt_probe_s uwb_probe_interface;

typedef struct _uwb_obj_t {
    mp_obj_base_t base;
    bool active;
} uwb_obj_t;

static uwb_obj_t *active_instance;
extern const mp_obj_type_t uwb_type;

static uwb_obj_t *get_active(mp_obj_t self_in) {
    uwb_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (!self->active || active_instance != self) {
        mp_raise_OSError(MP_ENODEV);
    }
    return self;
}

static uint16_t preamble_code(mp_int_t value) {
    switch (value) {
        case 32:
            return DWT_PLEN_32;
        case 64:
            return DWT_PLEN_64;
        case 72:
            return DWT_PLEN_72;
        case 128:
            return DWT_PLEN_128;
        case 256:
            return DWT_PLEN_256;
        case 512:
            return DWT_PLEN_512;
        case 1024:
            return DWT_PLEN_1024;
        case 1536:
            return DWT_PLEN_1536;
        case 2048:
            return DWT_PLEN_2048;
        case 4096:
            return DWT_PLEN_4096;
        default:
            mp_raise_ValueError(MP_ERROR_TEXT("invalid preamble_length"));
    }
}

static dwt_pac_size_e pac_code(mp_int_t value) {
    switch (value) {
        case 4:
            return DWT_PAC4;
        case 8:
            return DWT_PAC8;
        case 16:
            return DWT_PAC16;
        case 32:
            return DWT_PAC32;
        default:
            mp_raise_ValueError(MP_ERROR_TEXT("invalid pac"));
    }
}

static dwt_sts_lengths_e sts_length_code(mp_int_t value) {
    switch (value) {
        case 32:
            return DWT_STS_LEN_32;
        case 64:
            return DWT_STS_LEN_64;
        case 128:
            return DWT_STS_LEN_128;
        case 256:
            return DWT_STS_LEN_256;
        case 512:
            return DWT_STS_LEN_512;
        case 1024:
            return DWT_STS_LEN_1024;
        case 2048:
            return DWT_STS_LEN_2048;
        default:
            mp_raise_ValueError(MP_ERROR_TEXT("invalid sts_length"));
    }
}

static mp_obj_t uwb_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw,
    const mp_obj_t *all_args) {
    enum { ARG_irq, ARG_wakeup, ARG_reset, ARG_mosi, ARG_miso, ARG_clock, ARG_cs };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_irq, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_wakeup, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_reset, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_mosi, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_miso, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_clock, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_cs, MP_ARG_REQUIRED | MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (active_instance != NULL) {
        mp_raise_OSError(MP_EBUSY);
    }
    uwb_obj_t *self = mp_obj_malloc_with_finaliser(uwb_obj_t, type);
    self->active = false;
    uwb_port_config_t config = {
        .irq = args[ARG_irq].u_int,
        .wakeup = args[ARG_wakeup].u_int,
        .reset = args[ARG_reset].u_int,
        .mosi = args[ARG_mosi].u_int,
        .miso = args[ARG_miso].u_int,
        .clock = args[ARG_clock].u_int,
        .cs = args[ARG_cs].u_int,
    };
    if (uwb_port_init(&config) != 0) {
        uwb_port_deinit();
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB SPI init failed"));
    }
    uwb_port_reset();
    if (dwt_probe((struct dwt_probe_s *)&uwb_probe_interface) == DWT_ERROR) {
        uwb_port_deinit();
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB probe failed"));
    }
    if (dwt_initialise(DWT_DW_INIT) != DWT_SUCCESS) {
        uwb_port_deinit();
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB initialise failed"));
    }
    self->active = true;
    active_instance = self;
    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t uwb_deinit(mp_obj_t self_in) {
    uwb_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->active && active_instance == self) {
        dwt_forcetrxoff();
        uwb_port_deinit();
        self->active = false;
        active_instance = NULL;
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_deinit_obj, uwb_deinit);

static mp_obj_t uwb_reset(mp_obj_t self_in) {
    get_active(self_in);
    dwt_forcetrxoff();
    uwb_port_reset();
    if (dwt_probe((struct dwt_probe_s *)&uwb_probe_interface) == DWT_ERROR ||
        dwt_initialise(DWT_DW_INIT) != DWT_SUCCESS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB reset failed"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_reset_obj, uwb_reset);

static mp_obj_t uwb_wakeup(mp_obj_t self_in) {
    get_active(self_in);
    uwb_port_wakeup();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_wakeup_obj, uwb_wakeup);

static mp_obj_t uwb_device_id(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int_from_uint(dwt_readdevid());
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_device_id_obj, uwb_device_id);

static mp_obj_t uwb_configure(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_channel, ARG_preamble_length, ARG_pac, ARG_tx_code, ARG_rx_code, ARG_sfd_type,
           ARG_data_rate, ARG_phr_mode, ARG_phr_rate, ARG_sfd_timeout, ARG_sts_mode,
           ARG_sts_length, ARG_pdoa_mode };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_channel, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 9}},
        {MP_QSTR_preamble_length, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 128}},
        {MP_QSTR_pac, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 8}},
        {MP_QSTR_tx_code, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 9}},
        {MP_QSTR_rx_code, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 9}},
        {MP_QSTR_sfd_type, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = DWT_SFD_DW_8}},
        {MP_QSTR_data_rate, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = DWT_BR_6M8}},
        {MP_QSTR_phr_mode, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = DWT_PHRMODE_STD}},
        {MP_QSTR_phr_rate, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = DWT_PHRRATE_STD}},
        {MP_QSTR_sfd_timeout, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 129}},
        {MP_QSTR_sts_mode, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = DWT_STS_MODE_OFF}},
        {MP_QSTR_sts_length, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 64}},
        {MP_QSTR_pdoa_mode, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = DWT_PDOA_M0}},
    };
    get_active(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    if (args[ARG_channel].u_int != 5 && args[ARG_channel].u_int != 9) {
        mp_raise_ValueError(MP_ERROR_TEXT("channel must be 5 or 9"));
    }
    dwt_config_t config = {
        .chan = args[ARG_channel].u_int,
        .txPreambLength = preamble_code(args[ARG_preamble_length].u_int),
        .rxPAC = pac_code(args[ARG_pac].u_int),
        .txCode = args[ARG_tx_code].u_int,
        .rxCode = args[ARG_rx_code].u_int,
        .sfdType = args[ARG_sfd_type].u_int,
        .dataRate = args[ARG_data_rate].u_int,
        .phrMode = args[ARG_phr_mode].u_int,
        .phrRate = args[ARG_phr_rate].u_int,
        .sfdTO = args[ARG_sfd_timeout].u_int,
        .stsMode = args[ARG_sts_mode].u_int,
        .stsLength = sts_length_code(args[ARG_sts_length].u_int),
        .pdoaMode = args[ARG_pdoa_mode].u_int,
    };
    if (dwt_configure(&config) != DWT_SUCCESS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB configure failed"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(uwb_configure_obj, 1, uwb_configure);

static mp_obj_t uwb_configure_tx_rf(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_pg_delay, ARG_tx_power, ARG_pg_count };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_pg_delay, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0x34}},
        {MP_QSTR_tx_power, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
        {MP_QSTR_pg_count, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0}},
    };
    get_active(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    dwt_txconfig_t config = {
        .PGdly = args[ARG_pg_delay].u_int,
        .power = (uint32_t)mp_obj_get_int_truncated(args[ARG_tx_power].u_obj),
        .PGcount = args[ARG_pg_count].u_int,
    };
    dwt_configuretxrf(&config);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(uwb_configure_tx_rf_obj, 1, uwb_configure_tx_rf);

static mp_obj_t uwb_set_antenna_delay(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_tx, ARG_rx };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_tx, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_rx, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0}},
    };
    get_active(pos_args[0]);
    mp_arg_val_t args[2];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, 2, allowed_args, args);
    dwt_settxantennadelay(args[ARG_tx].u_int);
    dwt_setrxantennadelay(args[ARG_rx].u_int);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(uwb_set_antenna_delay_obj, 1, uwb_set_antenna_delay);

static mp_obj_t uwb_set_lna_pa(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_lna, ARG_pa };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_lna, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = true}},
        {MP_QSTR_pa, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = true}},
    };
    get_active(pos_args[0]);
    mp_arg_val_t args[2];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, 2, allowed_args, args);
    dwt_setlnapamode((args[ARG_lna].u_bool ? DWT_LNA_ENABLE : 0) |
        (args[ARG_pa].u_bool ? DWT_PA_ENABLE : 0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(uwb_set_lna_pa_obj, 1, uwb_set_lna_pa);

#define DEFINE_UINT_SETTER(name, driver_function) \
    static mp_obj_t uwb_##name(mp_obj_t self_in, mp_obj_t value_in) { \
        get_active(self_in); \
        driver_function((uint32_t)mp_obj_get_int_truncated(value_in)); \
        return mp_const_none; \
    } \
    static MP_DEFINE_CONST_FUN_OBJ_2(uwb_##name##_obj, uwb_##name)

DEFINE_UINT_SETTER(set_rx_after_tx_delay, dwt_setrxaftertxdelay);
DEFINE_UINT_SETTER(set_rx_timeout, dwt_setrxtimeout);
DEFINE_UINT_SETTER(set_preamble_timeout, dwt_setpreambledetecttimeout);
DEFINE_UINT_SETTER(set_delayed_trx_time, dwt_setdelayedtrxtime);

static mp_obj_t uwb_write_tx_frame(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_data, ARG_ranging };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_data, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
        {MP_QSTR_ranging, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = true}},
    };
    get_active(pos_args[0]);
    mp_arg_val_t args[2];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, 2, allowed_args, args);
    mp_buffer_info_t buffer;
    mp_get_buffer_raise(args[ARG_data].u_obj, &buffer, MP_BUFFER_READ);
    if (buffer.len > UWB_MAX_PAYLOAD) {
        mp_raise_ValueError(MP_ERROR_TEXT("UWB payload exceeds 125 bytes"));
    }
    if (dwt_writetxdata(buffer.len, buffer.buf, 0) != DWT_SUCCESS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB TX buffer write failed"));
    }
    dwt_writetxfctrl(buffer.len + UWB_FCS_LENGTH, 0, args[ARG_ranging].u_bool);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(uwb_write_tx_frame_obj, 1, uwb_write_tx_frame);

static mp_obj_t uwb_start_tx(mp_obj_t self_in, mp_obj_t mode_in) {
    get_active(self_in);
    if (dwt_starttx(mp_obj_get_int(mode_in)) != DWT_SUCCESS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB delayed TX is too late"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(uwb_start_tx_obj, uwb_start_tx);

static mp_obj_t uwb_rx_enable(mp_obj_t self_in, mp_obj_t mode_in) {
    get_active(self_in);
    if (dwt_rxenable(mp_obj_get_int(mode_in)) != DWT_SUCCESS) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("UWB RX enable failed"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(uwb_rx_enable_obj, uwb_rx_enable);

static mp_obj_t uwb_wait_status(size_t n_args, const mp_obj_t *args) {
    get_active(args[0]);
    uint32_t mask = mp_obj_get_int_truncated(args[1]);
    mp_int_t timeout = n_args > 2 ? mp_obj_get_int(args[2]) : -1;
    mp_uint_t start = mp_hal_ticks_ms();
    for (;;) {
        uint32_t status = dwt_readsysstatuslo();
        if (status & mask) {
            return mp_obj_new_int_from_uint(status);
        }
        if (timeout >= 0 && (mp_uint_t)(mp_hal_ticks_ms() - start) >= (mp_uint_t)timeout) {
            mp_raise_OSError(MP_ETIMEDOUT);
        }
        MICROPY_EVENT_POLL_HOOK;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(uwb_wait_status_obj, 2, 3, uwb_wait_status);

static mp_obj_t uwb_read_status(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int_from_uint(dwt_readsysstatuslo());
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_read_status_obj, uwb_read_status);

static mp_obj_t uwb_clear_status(mp_obj_t self_in, mp_obj_t mask_in) {
    get_active(self_in);
    dwt_writesysstatuslo(mp_obj_get_int_truncated(mask_in));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(uwb_clear_status_obj, uwb_clear_status);

static mp_obj_t uwb_force_trx_off(mp_obj_t self_in) {
    get_active(self_in);
    dwt_forcetrxoff();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_force_trx_off_obj, uwb_force_trx_off);

static mp_obj_t uwb_frame_length(mp_obj_t self_in) {
    get_active(self_in);
    return MP_OBJ_NEW_SMALL_INT(dwt_getframelength(NULL));
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_frame_length_obj, uwb_frame_length);

static mp_obj_t uwb_read_rx_frame(mp_obj_t self_in) {
    get_active(self_in);
    uint16_t frame_length = dwt_getframelength(NULL);
    if (frame_length < UWB_FCS_LENGTH || frame_length > UWB_MAX_PAYLOAD + UWB_FCS_LENGTH) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("invalid UWB RX frame length"));
    }
    vstr_t frame;
    vstr_init_len(&frame, frame_length - UWB_FCS_LENGTH);
    dwt_readrxdata((uint8_t *)frame.buf, frame.len, 0);
    return mp_obj_new_bytes_from_vstr(&frame);
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_read_rx_frame_obj, uwb_read_rx_frame);

static uint64_t read_timestamp(void (*reader)(uint8_t *)) {
    uint8_t bytes[5];
    reader(bytes);
    uint64_t value = 0;
    for (int index = 4; index >= 0; --index) {
        value = (value << 8) | bytes[index];
    }
    return value;
}
static void read_rx_timestamp_adapter(uint8_t *timestamp) {
    dwt_readrxtimestamp(timestamp, DWT_IP_M);
}
static mp_obj_t uwb_tx_timestamp(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int_from_ull(read_timestamp(dwt_readtxtimestamp));
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_tx_timestamp_obj, uwb_tx_timestamp);
static mp_obj_t uwb_rx_timestamp(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int_from_ull(read_timestamp(read_rx_timestamp_adapter));
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_rx_timestamp_obj, uwb_rx_timestamp);
static mp_obj_t uwb_system_timestamp(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int_from_ull(read_timestamp(dwt_readsystime));
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_system_timestamp_obj, uwb_system_timestamp);

static mp_obj_t uwb_read_pdoa(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int(dwt_readpdoa());
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_read_pdoa_obj, uwb_read_pdoa);

static mp_obj_t uwb_read_tdoa_pdoa(size_t n_args, const mp_obj_t *args) {
    get_active(args[0]);
    mp_int_t index = n_args > 1 ? mp_obj_get_int(args[1]) : 0;
    if (index < 0 || index > 2) {
        mp_raise_ValueError(MP_ERROR_TEXT("index must be in range 0-2"));
    }
    dwt_pdoa_tdoa_res_t result = {0};
    dwt_read_tdoa_pdoa(&result, index);
    mp_obj_t values[] = {
        mp_obj_new_int(result.tdoa),
        mp_obj_new_int(result.pdoa),
    };
    return mp_obj_new_tuple(MP_ARRAY_SIZE(values), values);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(uwb_read_tdoa_pdoa_obj, 1, 2, uwb_read_tdoa_pdoa);

static mp_obj_t uwb_read_sts_quality(mp_obj_t self_in) {
    get_active(self_in);
    int16_t quality = 0;
    int32_t result = dwt_readstsquality(&quality, 0);
    mp_obj_t values[] = {
        mp_obj_new_bool(result >= 0),
        mp_obj_new_int(quality),
    };
    return mp_obj_new_tuple(MP_ARRAY_SIZE(values), values);
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_read_sts_quality_obj, uwb_read_sts_quality);

static mp_obj_t uwb_set_pdoa_offset(mp_obj_t self_in, mp_obj_t offset_in) {
    get_active(self_in);
    mp_int_t offset = mp_obj_get_int(offset_in);
    if (offset < 0 || offset > UINT16_MAX) {
        mp_raise_ValueError(MP_ERROR_TEXT("offset must be in range 0-65535"));
    }
    dwt_setpdoaoffset(offset);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(uwb_set_pdoa_offset_obj, uwb_set_pdoa_offset);

static mp_obj_t uwb_read_pdoa_offset(mp_obj_t self_in) {
    get_active(self_in);
    return mp_obj_new_int_from_uint(dwt_readpdoaoffset());
}
static MP_DEFINE_CONST_FUN_OBJ_1(uwb_read_pdoa_offset_obj, uwb_read_pdoa_offset);

static const mp_rom_map_elem_t uwb_locals_dict_table[] = {
    {MP_ROM_QSTR(MP_QSTR___del__), MP_ROM_PTR(&uwb_deinit_obj)},
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&uwb_deinit_obj)},
    {MP_ROM_QSTR(MP_QSTR_reset), MP_ROM_PTR(&uwb_reset_obj)},
    {MP_ROM_QSTR(MP_QSTR_wakeup), MP_ROM_PTR(&uwb_wakeup_obj)},
    {MP_ROM_QSTR(MP_QSTR_device_id), MP_ROM_PTR(&uwb_device_id_obj)},
    {MP_ROM_QSTR(MP_QSTR_configure), MP_ROM_PTR(&uwb_configure_obj)},
    {MP_ROM_QSTR(MP_QSTR_configure_tx_rf), MP_ROM_PTR(&uwb_configure_tx_rf_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_antenna_delay), MP_ROM_PTR(&uwb_set_antenna_delay_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_lna_pa), MP_ROM_PTR(&uwb_set_lna_pa_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_rx_after_tx_delay), MP_ROM_PTR(&uwb_set_rx_after_tx_delay_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_rx_timeout), MP_ROM_PTR(&uwb_set_rx_timeout_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_preamble_timeout), MP_ROM_PTR(&uwb_set_preamble_timeout_obj)},
    {MP_ROM_QSTR(MP_QSTR_write_tx_frame), MP_ROM_PTR(&uwb_write_tx_frame_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_delayed_trx_time), MP_ROM_PTR(&uwb_set_delayed_trx_time_obj)},
    {MP_ROM_QSTR(MP_QSTR_start_tx), MP_ROM_PTR(&uwb_start_tx_obj)},
    {MP_ROM_QSTR(MP_QSTR_rx_enable), MP_ROM_PTR(&uwb_rx_enable_obj)},
    {MP_ROM_QSTR(MP_QSTR_wait_status), MP_ROM_PTR(&uwb_wait_status_obj)},
    {MP_ROM_QSTR(MP_QSTR_read_status), MP_ROM_PTR(&uwb_read_status_obj)},
    {MP_ROM_QSTR(MP_QSTR_clear_status), MP_ROM_PTR(&uwb_clear_status_obj)},
    {MP_ROM_QSTR(MP_QSTR_force_trx_off), MP_ROM_PTR(&uwb_force_trx_off_obj)},
    {MP_ROM_QSTR(MP_QSTR_read_rx_frame), MP_ROM_PTR(&uwb_read_rx_frame_obj)},
    {MP_ROM_QSTR(MP_QSTR_frame_length), MP_ROM_PTR(&uwb_frame_length_obj)},
    {MP_ROM_QSTR(MP_QSTR_tx_timestamp), MP_ROM_PTR(&uwb_tx_timestamp_obj)},
    {MP_ROM_QSTR(MP_QSTR_rx_timestamp), MP_ROM_PTR(&uwb_rx_timestamp_obj)},
    {MP_ROM_QSTR(MP_QSTR_system_timestamp), MP_ROM_PTR(&uwb_system_timestamp_obj)},
    {MP_ROM_QSTR(MP_QSTR_read_pdoa), MP_ROM_PTR(&uwb_read_pdoa_obj)},
    {MP_ROM_QSTR(MP_QSTR_read_tdoa_pdoa), MP_ROM_PTR(&uwb_read_tdoa_pdoa_obj)},
    {MP_ROM_QSTR(MP_QSTR_read_sts_quality), MP_ROM_PTR(&uwb_read_sts_quality_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_pdoa_offset), MP_ROM_PTR(&uwb_set_pdoa_offset_obj)},
    {MP_ROM_QSTR(MP_QSTR_read_pdoa_offset), MP_ROM_PTR(&uwb_read_pdoa_offset_obj)},
};
static MP_DEFINE_CONST_DICT(uwb_locals_dict, uwb_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(uwb_type, MP_QSTR_UWB, MP_TYPE_FLAG_NONE,
    make_new, uwb_make_new,
    locals_dict, &uwb_locals_dict);

#define UWB_CONSTANT(name, value) {MP_ROM_QSTR(MP_QSTR_##name), MP_ROM_INT(value)}
static const mp_rom_map_elem_t uwb_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_uwb)},
    {MP_ROM_QSTR(MP_QSTR_UWB), MP_ROM_PTR(&uwb_type)},
    UWB_CONSTANT(SFD_DW_8, DWT_SFD_DW_8),
    UWB_CONSTANT(BR_6M8, DWT_BR_6M8),
    UWB_CONSTANT(PHR_STD, DWT_PHRMODE_STD),
    UWB_CONSTANT(PHR_RATE_STD, DWT_PHRRATE_STD),
    UWB_CONSTANT(STS_OFF, DWT_STS_MODE_OFF),
    UWB_CONSTANT(STS_MODE_1, DWT_STS_MODE_1),
    UWB_CONSTANT(STS_MODE_SDC, DWT_STS_MODE_SDC),
    UWB_CONSTANT(PDOA_M0, DWT_PDOA_M0),
    UWB_CONSTANT(PDOA_M1, DWT_PDOA_M1),
    UWB_CONSTANT(PDOA_M3, DWT_PDOA_M3),
    UWB_CONSTANT(VALID_TDOA_LIMIT, DWT_VALID_TDOA_LIMIT),
    UWB_CONSTANT(TX_IMMEDIATE, DWT_START_TX_IMMEDIATE),
    UWB_CONSTANT(TX_DELAYED, DWT_START_TX_DELAYED),
    UWB_CONSTANT(RESPONSE_EXPECTED, DWT_RESPONSE_EXPECTED),
    UWB_CONSTANT(RX_IMMEDIATE, DWT_START_RX_IMMEDIATE),
    UWB_CONSTANT(RX_DELAYED, DWT_START_RX_DELAYED),
    UWB_CONSTANT(IDLE_ON_DELAY_ERROR, DWT_IDLE_ON_DLY_ERR),
    UWB_CONSTANT(STATUS_TX_DONE, DWT_INT_TXFRS_BIT_MASK),
    UWB_CONSTANT(STATUS_RX_GOOD, DWT_INT_RXFCG_BIT_MASK),
    UWB_CONSTANT(STATUS_RX_TIMEOUT, SYS_STATUS_ALL_RX_TO),
    UWB_CONSTANT(STATUS_RX_ERROR, SYS_STATUS_ALL_RX_ERR),
    UWB_CONSTANT(STATUS_RX_ALL, DWT_INT_RXFCG_BIT_MASK | SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR),
};
static MP_DEFINE_CONST_DICT(uwb_module_globals, uwb_module_globals_table);
const mp_obj_module_t uwb_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&uwb_module_globals,
};
MP_REGISTER_MODULE(MP_QSTR_uwb, uwb_module);
