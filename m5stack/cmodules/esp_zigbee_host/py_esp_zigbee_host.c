/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "py/objlist.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include "py/objtype.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "esp_check.h"
#include "string.h"
#include "nvs_flash.h"
#include "esp_log.h"

#include "ha/esp_zigbee_ha_standard.h"
#include "esp_zigbee_core.h"

static const char *TAG = "ESP_ZB_HOST";

/* Zigbee configuration */
#define MAX_CHILDREN                10    /* the max amount of connected devices */
#define INSTALLCODE_POLICY_ENABLE   false /* enable the install code policy for security */
#define HA_ONOFF_SWITCH_ENDPOINT    1     /* esp light switch device endpoint */
#define HA_ESP_LIGHT_ENDPOINT       10 /* esp light bulb device endpoint, used to process light controlling commands */
#define ESP_ZB_PRIMARY_CHANNEL_MASK (1l << 13) /* Zigbee primary channel mask use in the example */

typedef struct light_bulb_device_params_s {
    esp_zb_ieee_addr_t ieee_addr;
    uint8_t endpoint;
    uint16_t short_addr;
} light_bulb_device_params_t;

mp_obj_t g_bind_cb;

static void bdb_start_top_level_commissioning_cb(uint8_t mode_mask) {
    ESP_RETURN_ON_FALSE(esp_zb_bdb_start_top_level_commissioning(mode_mask) == ESP_OK, , TAG,
        "Failed to start Zigbee bdb commissioning");
}

// object: devinfo
typedef struct _py_devinfo_obj {
    mp_obj_base_t base;
    mp_obj_t addr;
    mp_obj_t endpoint;
} py_devinfo_obj_t;

mp_obj_t mp_devinfo_addr(mp_obj_t self_in) {
    return ((py_devinfo_obj_t *)self_in)->addr;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mp_devinfo_addr_obj, mp_devinfo_addr);

mp_obj_t mp_devinfo_endpoint(mp_obj_t self_in) {
    return ((py_devinfo_obj_t *)self_in)->endpoint;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mp_devinfo_endpoint_obj, mp_devinfo_endpoint);

static const mp_rom_map_elem_t mp_devinfo_locals_dict_table[] = {
    {MP_ROM_QSTR(MP_QSTR_addr), MP_ROM_PTR(&mp_devinfo_addr_obj)},
    {MP_ROM_QSTR(MP_QSTR_endpoint), MP_ROM_PTR(&mp_devinfo_endpoint_obj)},
};
static MP_DEFINE_CONST_DICT(mp_devinfo_locals_dict, mp_devinfo_locals_dict_table);

static mp_obj_t py_devinfo_make_new(mp_obj_t addr, mp_obj_t endpoint);

MP_DEFINE_CONST_OBJ_TYPE(py_devinfo_type, MP_QSTR_devinfo, MP_TYPE_FLAG_NONE, make_new, py_devinfo_make_new,
    locals_dict, &mp_devinfo_locals_dict);

static mp_obj_t py_devinfo_make_new(mp_obj_t addr, mp_obj_t endpoint) {
    py_devinfo_obj_t *self = m_new_obj(py_devinfo_obj_t);
    self->base.type = &py_devinfo_type;
    self->addr = addr;
    self->endpoint = endpoint;
    return MP_OBJ_FROM_PTR(self);
}

static void bind_cb(esp_zb_zdp_status_t zdo_status, void *user_ctx) {
    if (zdo_status == ESP_ZB_ZDP_STATUS_SUCCESS) {
        if (user_ctx) {
            light_bulb_device_params_t *light = (light_bulb_device_params_t *)user_ctx;
            uint16_t addr = light->short_addr;
            free(light);
            mp_sched_schedule(g_bind_cb, mp_obj_new_int(addr));
        }
    }
}

static void user_find_cb(esp_zb_zdp_status_t zdo_status, uint16_t addr, uint8_t endpoint, void *user_ctx) {
    if (zdo_status == ESP_ZB_ZDP_STATUS_SUCCESS) {
        esp_zb_zdo_bind_req_param_t bind_req;
        light_bulb_device_params_t *light = (light_bulb_device_params_t *)malloc(sizeof(light_bulb_device_params_t));
        light->endpoint = endpoint;
        light->short_addr = addr;
        esp_zb_ieee_address_by_short(light->short_addr, light->ieee_addr);
        esp_zb_get_long_address(bind_req.src_address);
        bind_req.src_endp = HA_ONOFF_SWITCH_ENDPOINT;
        bind_req.cluster_id = ESP_ZB_ZCL_CLUSTER_ID_ON_OFF;
        bind_req.dst_addr_mode = ESP_ZB_ZDO_BIND_DST_ADDR_MODE_64_BIT_EXTENDED;
        memcpy(bind_req.dst_address_u.addr_long, light->ieee_addr, sizeof(esp_zb_ieee_addr_t));
        bind_req.dst_endp = endpoint;
        bind_req.req_dst_addr = esp_zb_get_short_address(); /* TODO: Send bind request to self */
        esp_zb_zdo_device_bind_req(&bind_req, bind_cb, (void *)light);
    }
}

void esp_zb_app_signal_handler(esp_zb_app_signal_t *signal_struct) {
    uint32_t *p_sg_p = signal_struct->p_app_signal;
    esp_err_t err_status = signal_struct->esp_err_status;
    esp_zb_app_signal_type_t sig_type = *p_sg_p;
    esp_zb_zdo_signal_device_annce_params_t *dev_annce_params = NULL;
    switch (sig_type) {
        case ESP_ZB_ZDO_SIGNAL_SKIP_STARTUP:
            ESP_LOGI(TAG, "Initialize Zigbee stack");
            esp_zb_bdb_start_top_level_commissioning(
                ESP_ZB_BDB_MODE_INITIALIZATION);  // 启动 Zigbee BDB 顶层的网络配置或设备行为模式。
            break;
        case ESP_ZB_BDB_SIGNAL_DEVICE_FIRST_START:
        case ESP_ZB_BDB_SIGNAL_DEVICE_REBOOT:
            if (err_status == ESP_OK) {
                ESP_LOGI(TAG, "Start network formation");
                esp_zb_bdb_start_top_level_commissioning(ESP_ZB_BDB_MODE_NETWORK_FORMATION);
            } else {
                ESP_LOGW(TAG, "%s failed with status: %s, retrying", esp_zb_zdo_signal_to_string(sig_type),
                    esp_err_to_name(err_status));
                esp_zb_scheduler_alarm((esp_zb_callback_t)bdb_start_top_level_commissioning_cb,
                    ESP_ZB_BDB_MODE_INITIALIZATION, 1000);
            }
            break;
        case ESP_ZB_BDB_SIGNAL_FORMATION:  // 设备尝试创建 Zigbee 网络，并完成网络形成的过程后，协议栈发出的信号。
            if (err_status == ESP_OK) {
                esp_zb_ieee_addr_t extended_pan_id;
                esp_zb_get_extended_pan_id(extended_pan_id);
                ESP_LOGI(TAG,
                    "Formed network successfully (Extended PAN ID: %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x, PAN "
                    "ID: 0x%04hx, Channel:%d, Short Address: 0x%04hx)",
                    extended_pan_id[7], extended_pan_id[6], extended_pan_id[5], extended_pan_id[4],
                    extended_pan_id[3], extended_pan_id[2], extended_pan_id[1], extended_pan_id[0],
                    esp_zb_get_pan_id(), esp_zb_get_current_channel(), esp_zb_get_short_address());
                esp_zb_bdb_start_top_level_commissioning(ESP_ZB_BDB_MODE_NETWORK_STEERING);
            } else {
                ESP_LOGI(TAG, "Restart network formation (status: %s)", esp_err_to_name(err_status));
                esp_zb_scheduler_alarm((esp_zb_callback_t)bdb_start_top_level_commissioning_cb,
                    ESP_ZB_BDB_MODE_NETWORK_FORMATION, 1000);
            }
            break;
        case ESP_ZB_BDB_SIGNAL_STEERING:
            if (err_status == ESP_OK) {
                ESP_LOGI(TAG, "Network steering started");
            }
            break;
        case ESP_ZB_ZDO_SIGNAL_DEVICE_ANNCE:  // 处理新设备加入网络的情况，并查找设备。
            dev_annce_params = (esp_zb_zdo_signal_device_annce_params_t *)esp_zb_app_signal_get_params(p_sg_p);
            ESP_LOGI(TAG, "New device commissioned or rejoined (short: 0x%04hx)", dev_annce_params->device_short_addr);
            esp_zb_zdo_match_desc_req_param_t cmd_req;
            cmd_req.dst_nwk_addr = dev_annce_params->device_short_addr;
            cmd_req.addr_of_interest = dev_annce_params->device_short_addr;
            esp_zb_zdo_find_on_off_light(&cmd_req, user_find_cb, NULL);
            break;
        case ESP_ZB_NWK_SIGNAL_PERMIT_JOIN_STATUS:
            if (err_status == ESP_OK) {
                if (*(uint8_t *)esp_zb_app_signal_get_params(p_sg_p)) {
                    ESP_LOGI(TAG, "Network(0x%04hx) is open for %d seconds", esp_zb_get_pan_id(),
                        *(uint8_t *)esp_zb_app_signal_get_params(p_sg_p));
                } else {
                    ESP_LOGW(TAG, "Network(0x%04hx) closed, devices joining not allowed.", esp_zb_get_pan_id());
                }
            }
            break;
        default:
            ESP_LOGI(TAG, "ZDO signal: %s (0x%x), status: %s", esp_zb_zdo_signal_to_string(sig_type), sig_type,
                esp_err_to_name(err_status));
            break;
    }
}

static void esp_zb_task(void *pvParameters) {
    esp_zb_cfg_t zb_nwk_cfg = {
        .esp_zb_role = ESP_ZB_DEVICE_TYPE_COORDINATOR,
        .install_code_policy = INSTALLCODE_POLICY_ENABLE,
        .nwk_cfg.zczr_cfg =
        {
            .max_children = MAX_CHILDREN,
        },
    };
    esp_zb_init(&zb_nwk_cfg);

    esp_zb_on_off_switch_cfg_t switch_cfg = ESP_ZB_DEFAULT_ON_OFF_SWITCH_CONFIG();
    esp_zb_ep_list_t *esp_zb_on_off_switch_ep = esp_zb_on_off_switch_ep_create(HA_ONOFF_SWITCH_ENDPOINT, &switch_cfg);

    esp_zb_device_register(esp_zb_on_off_switch_ep);
    esp_zb_set_primary_network_channel_set(ESP_ZB_PRIMARY_CHANNEL_MASK);
    ESP_ERROR_CHECK(esp_zb_start(false));
    esp_zb_stack_main_loop();
}

// =================================================================================================
// class: SwitchEndpoint
typedef struct _switch_endpoint_obj_t {
    mp_obj_base_t base;
    int uart_id;
    int uart_tx;
    int uart_rx;
} switch_endpoint_obj_t;

extern const mp_obj_type_t mp_switch_endpoint_type;
static bool is_initialized;

static mp_obj_t switch_endpoint_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    switch_endpoint_obj_t *self = mp_obj_malloc_with_finaliser(switch_endpoint_obj_t, &mp_switch_endpoint_type);

    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_id, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
        {MP_QSTR_tx, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
        {MP_QSTR_rx, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
    };
    mp_arg_val_t args_vals[MP_ARRAY_SIZE(allowed_args)];
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    mp_arg_parse_all(n_args, args + 1, &kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args_vals);

    if (args_vals[0].u_obj != MP_OBJ_NULL) {
        self->uart_id = mp_obj_get_int(args_vals[0].u_obj);
    }
    if (args_vals[1].u_obj != MP_OBJ_NULL) {
        self->uart_tx = mp_obj_get_int(args_vals[1].u_obj);
    }
    if (args_vals[2].u_obj != MP_OBJ_NULL) {
        self->uart_rx = mp_obj_get_int(args_vals[2].u_obj);
    }

    host_bus_init(self->uart_id, self->uart_tx, self->uart_rx);
    if (!is_initialized) {
        esp_zb_platform_config_t config = {
            .radio_config =
            {
                .radio_mode = RADIO_MODE_UART_NCP,
            },
            .host_config =
            {
                .host_mode = HOST_CONNECTION_MODE_UART,
            },
        };
        ESP_ERROR_CHECK(esp_zb_platform_config(&config));
        xTaskCreate(esp_zb_task, "zigbee_main", 4096, NULL, 5, NULL);
        if (self->uart_id == 2) {  // FIXME: (That's testing for you)
            vTaskDelay(pdMS_TO_TICKS(200));
            host_bus_deinit();
            vTaskDelay(pdMS_TO_TICKS(20));
            host_bus_init(self->uart_id, self->uart_tx, self->uart_rx);
            ESP_ERROR_CHECK(esp_zb_platform_config(&config));
            xTaskCreate(esp_zb_task, "zigbee_main", 4096, NULL, 5, NULL);
        }
        is_initialized = true;
    }

    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t switch_endpoint_set_bind_cb(mp_obj_t self_in, mp_obj_t cb) {
    if (cb == mp_const_none || mp_obj_is_callable(cb)) {
        g_bind_cb = cb;
    } else {
        mp_raise_ValueError(MP_ERROR_TEXT("callback must be callable or None"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(switch_endpoint_set_bind_cb_obj, switch_endpoint_set_bind_cb);

static mp_obj_t switch_endpoint_on(size_t n_args, const mp_obj_t *args) {
    switch_endpoint_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    esp_zb_zcl_on_off_cmd_t cmd_req;

    cmd_req.zcl_basic_cmd.src_endpoint = HA_ONOFF_SWITCH_ENDPOINT;
    cmd_req.on_off_cmd_id = ESP_ZB_ZCL_CMD_ON_OFF_ON_ID;
    if (n_args > 1) {
        cmd_req.address_mode = ESP_ZB_APS_ADDR_MODE_16_ENDP_PRESENT;
        cmd_req.zcl_basic_cmd.dst_addr_u.addr_short = mp_obj_get_int(args[1]);
        cmd_req.zcl_basic_cmd.dst_endpoint = 10;
    } else {
        cmd_req.address_mode = ESP_ZB_APS_ADDR_MODE_DST_ADDR_ENDP_NOT_PRESENT;
    }

    esp_zb_zcl_on_off_cmd_req(&cmd_req);

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(switch_endpoint_on_obj, 1, 2, switch_endpoint_on);

static mp_obj_t switch_endpoint_off(size_t n_args, const mp_obj_t *args) {
    switch_endpoint_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    esp_zb_zcl_on_off_cmd_t cmd_req;

    cmd_req.zcl_basic_cmd.src_endpoint = HA_ONOFF_SWITCH_ENDPOINT;
    cmd_req.on_off_cmd_id = ESP_ZB_ZCL_CMD_ON_OFF_OFF_ID;
    if (n_args > 1) {
        cmd_req.address_mode = ESP_ZB_APS_ADDR_MODE_16_ENDP_PRESENT;
        cmd_req.zcl_basic_cmd.dst_addr_u.addr_short = mp_obj_get_int(args[1]);
        cmd_req.zcl_basic_cmd.dst_endpoint = 10;
    } else {
        cmd_req.address_mode = ESP_ZB_APS_ADDR_MODE_DST_ADDR_ENDP_NOT_PRESENT;
    }

    esp_zb_zcl_on_off_cmd_req(&cmd_req);

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(switch_endpoint_off_obj, 1, 2, switch_endpoint_off);

static mp_obj_t switch_endpoint_toggle(size_t n_args, const mp_obj_t *args) {
    switch_endpoint_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    esp_zb_zcl_on_off_cmd_t cmd_req;

    cmd_req.zcl_basic_cmd.src_endpoint = HA_ONOFF_SWITCH_ENDPOINT;
    cmd_req.on_off_cmd_id = ESP_ZB_ZCL_CMD_ON_OFF_TOGGLE_ID;
    if (n_args > 1) {
        cmd_req.address_mode = ESP_ZB_APS_ADDR_MODE_16_ENDP_PRESENT;
        cmd_req.zcl_basic_cmd.dst_addr_u.addr_short = mp_obj_get_int(args[1]);
        cmd_req.zcl_basic_cmd.dst_endpoint = 10;
    } else {
        cmd_req.address_mode = ESP_ZB_APS_ADDR_MODE_DST_ADDR_ENDP_NOT_PRESENT;
    }

    esp_zb_zcl_on_off_cmd_req(&cmd_req);

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(switch_endpoint_toggle_obj, 1, 2, switch_endpoint_toggle);

static const mp_rom_map_elem_t switch_endpoint_locals_dict_table[] = {
    // Methods
    {MP_ROM_QSTR(MP_QSTR_set_bind_callback), MP_ROM_PTR(&switch_endpoint_set_bind_cb_obj)},
    {MP_ROM_QSTR(MP_QSTR_on), MP_ROM_PTR(&switch_endpoint_on_obj)},
    {MP_ROM_QSTR(MP_QSTR_off), MP_ROM_PTR(&switch_endpoint_off_obj)},
    {MP_ROM_QSTR(MP_QSTR_toggle), MP_ROM_PTR(&switch_endpoint_toggle_obj)},
};
MP_DEFINE_CONST_DICT(switch_endpoint_locals_dict, switch_endpoint_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(mp_switch_endpoint_type, MP_QSTR_SwitchEndpoint, MP_TYPE_FLAG_NONE, make_new,
    switch_endpoint_make_new, locals_dict, &switch_endpoint_locals_dict);

// =================================================================================================
// module: esp_zigbee_host
static const mp_rom_map_elem_t esp_zigbee_host_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_esp_zigbee_host)},
    {MP_ROM_QSTR(MP_QSTR_SwitchEndpoint), MP_ROM_PTR(&mp_switch_endpoint_type)},
};
static MP_DEFINE_CONST_DICT(esp_zigbee_host_globals, esp_zigbee_host_globals_table);

const mp_obj_module_t module_esp_zigbee_host = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&esp_zigbee_host_globals,
};

MP_REGISTER_MODULE(MP_QSTR_esp_zigbee_host, module_esp_zigbee_host);
