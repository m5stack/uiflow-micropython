// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "usbhost.h"
#include "hid_report.h"

typedef struct {
    mp_obj_base_t base;
    uint32_t generation;
} hid_host_obj_t;

static void check_error(esp_err_t err) {
    if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("USB HID Host: %s"), esp_err_to_name(err));
    }
}

static void check_active(mp_obj_t self_in) {
    hid_host_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (!uiflow_usbhost_active(self->generation)) {
        mp_raise_OSError(MP_ENODEV);
    }
}

static mp_obj_t hid_host_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 0, false);
    hid_host_obj_t *self = mp_obj_malloc(hid_host_obj_t, type);
    check_error(uiflow_usbhost_start());
    self->generation = uiflow_usbhost_generation();
    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t protocol_name(uint8_t protocol) {
    if (protocol == 1) {
        return MP_OBJ_NEW_QSTR(MP_QSTR_keyboard);
    }
    if (protocol == 2) {
        return MP_OBJ_NEW_QSTR(MP_QSTR_mouse);
    }
    return MP_OBJ_NEW_QSTR(MP_QSTR_unknown);
}

static void put(mp_obj_t dict, qstr key, mp_obj_t value) {
    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(key), value);
}

static mp_obj_t device_dict(const uiflow_hid_device_t *device) {
    mp_obj_t result = mp_obj_new_dict(0);
    put(result, MP_QSTR_address, MP_OBJ_NEW_SMALL_INT(device->address));
    put(result, MP_QSTR_interface, MP_OBJ_NEW_SMALL_INT(device->interface));
    put(result, MP_QSTR_protocol, protocol_name(device->protocol));
    put(result, MP_QSTR_vid, MP_OBJ_NEW_SMALL_INT(device->vid));
    put(result, MP_QSTR_pid, MP_OBJ_NEW_SMALL_INT(device->pid));
    return result;
}

static mp_obj_t hid_host_devices(mp_obj_t self_in) {
    check_active(self_in);
    check_error(uiflow_usbhost_service());
    uiflow_hid_device_t devices[UIFLOW_HID_MAX_INTERFACES];
    size_t count = uiflow_usbhost_devices(devices);
    mp_obj_t result = mp_obj_new_list(0, NULL);
    for (size_t i = 0; i < count; ++i) {
        mp_obj_list_append(result, device_dict(&devices[i]));
    }
    return result;
}
static MP_DEFINE_CONST_FUN_OBJ_1(hid_host_devices_obj, hid_host_devices);

static mp_obj_t event_dict(const uiflow_hid_event_t *event) {
    static const qstr event_names[] = {
        MP_QSTR_connected, MP_QSTR_disconnected, MP_QSTR_input, MP_QSTR_error, MP_QSTR_unsupported,
    };
    mp_obj_t result = device_dict(&event->device);
    put(result, MP_QSTR_event, MP_OBJ_NEW_QSTR(event_names[event->event]));
    if (event->event == UIFLOW_HID_ERROR) {
        put(result, MP_QSTR_error, mp_obj_new_int(event->error));
    }
    if (event->event == UIFLOW_HID_INPUT) {
        put(result, MP_QSTR_data, mp_obj_new_bytes(event->data, event->length));
        uiflow_hid_report_t decoded;
        if (!uiflow_hid_decode(event->device.protocol, event->data, event->length, &decoded)) {
            put(result, MP_QSTR_event, MP_OBJ_NEW_QSTR(MP_QSTR_error));
            put(result, MP_QSTR_error, mp_obj_new_int(ESP_ERR_INVALID_SIZE));
        } else if (event->device.protocol == 1) {
            mp_obj_t keys[6];
            size_t count = 0;
            if (!decoded.rollover) {
                for (size_t i = 0; i < MP_ARRAY_SIZE(decoded.keys); ++i) {
                    if (decoded.keys[i] != 0) {
                        keys[count++] = MP_OBJ_NEW_SMALL_INT(decoded.keys[i]);
                    }
                }
            }
            put(result, MP_QSTR_modifiers, MP_OBJ_NEW_SMALL_INT(decoded.modifiers));
            put(result, MP_QSTR_keys, mp_obj_new_tuple(count, keys));
            put(result, MP_QSTR_rollover, mp_obj_new_bool(decoded.rollover));
        } else {
            put(result, MP_QSTR_buttons, MP_OBJ_NEW_SMALL_INT(decoded.buttons));
            put(result, MP_QSTR_dx, MP_OBJ_NEW_SMALL_INT(decoded.x));
            put(result, MP_QSTR_dy, MP_OBJ_NEW_SMALL_INT(decoded.y));
        }
    }
    return result;
}

static mp_obj_t hid_host_read(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_timeout };
    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_timeout, MP_ARG_INT, {.u_int = 0}},
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    mp_int_t timeout = args[ARG_timeout].u_int;
    if (timeout < 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("timeout must be >= 0"));
    }
    mp_uint_t start = mp_hal_ticks_ms();
    for (;;) {
        check_active(pos_args[0]);
        check_error(uiflow_usbhost_service());
        uiflow_hid_event_t event;
        if (uiflow_usbhost_read(&event)) {
            return event_dict(&event);
        }
        if (mp_hal_ticks_ms() - start >= (mp_uint_t)timeout) {
            return mp_const_none;
        }
        mp_hal_delay_ms(1);
    }
}
static MP_DEFINE_CONST_FUN_OBJ_KW(hid_host_read_obj, 1, hid_host_read);

static mp_obj_t hid_host_dropped(mp_obj_t self_in) {
    check_active(self_in);
    return mp_obj_new_int_from_uint(uiflow_usbhost_dropped());
}
static MP_DEFINE_CONST_FUN_OBJ_1(hid_host_dropped_obj, hid_host_dropped);

static mp_obj_t hid_host_deinit(mp_obj_t self_in) {
    hid_host_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->generation == uiflow_usbhost_generation()) {
        check_error(uiflow_usbhost_stop());
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(hid_host_deinit_obj, hid_host_deinit);

static mp_obj_t module_deinit(void) {
    check_error(uiflow_usbhost_stop());
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_0(module_deinit_obj, module_deinit);

static const mp_rom_map_elem_t hid_host_locals_table[] = {
    {MP_ROM_QSTR(MP_QSTR_devices), MP_ROM_PTR(&hid_host_devices_obj)},
    {MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&hid_host_read_obj)},
    {MP_ROM_QSTR(MP_QSTR_dropped), MP_ROM_PTR(&hid_host_dropped_obj)},
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&hid_host_deinit_obj)},
};
static MP_DEFINE_CONST_DICT(hid_host_locals, hid_host_locals_table);

static MP_DEFINE_CONST_OBJ_TYPE(
    hid_host_type,
    MP_QSTR_HIDHost,
    MP_TYPE_FLAG_NONE,
    make_new, hid_host_make_new,
    locals_dict, &hid_host_locals
    );

static const mp_rom_map_elem_t module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_usbhost)},
    {MP_ROM_QSTR(MP_QSTR_HIDHost), MP_ROM_PTR(&hid_host_type)},
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&module_deinit_obj)},
};
static MP_DEFINE_CONST_DICT(module_globals, module_globals_table);

const mp_obj_module_t module_usbhost = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_usbhost, module_usbhost);
