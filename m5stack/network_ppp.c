/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2018 "Eric Poulsen" <eric@zyxod.com>
 *
 * Based on the ESP IDF example code which is Public Domain / CC0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objtype.h"
#include "py/stream.h"
#include "shared/netutils/netutils.h"
#include "modmachine.h"
#include "ppp_set_auth.h"

#include "netif/ppp/ppp.h"
#include "netif/ppp/pppos.h"
#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include "lwip/netdb.h"
#include "lwip/dns.h"
#include "netif/ppp/pppapi.h"

#include "esp_netif.h"
#include "esp_netif_ppp.h"
#include "esp_log.h"
#include "esp_event.h"

#include "modnetwork.h"
#include "extmod/modnetwork.h"


#if defined(CONFIG_ESP_NETIF_TCPIP_LWIP) && defined(CONFIG_LWIP_PPP_SUPPORT)

static const char *TAG = "PPP";

typedef struct esp_ppp_netif_glue_t {
    esp_netif_driver_base_t base;
    // todo: add ppp specific fields
    mp_obj_t stream;
} esp_ppp_netif_glue_t;

#define PPP_CLOSE_TIMEOUT_MS (4000)

typedef struct _ppp_if_obj_t {
    base_if_obj_t base;
    // mp_obj_base_t base;
    bool active;
    bool connected;
    volatile bool clean_close;
    mp_obj_t stream;
    volatile TaskHandle_t client_task_handle;
    esp_ppp_netif_glue_t *netif_glue;
    bool deinited;
} ppp_if_obj_t;

const mp_obj_type_t ppp_if_type;

void on_ppp_changed(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data) {
    ppp_if_obj_t *self = (ppp_if_obj_t *)arg;
    // esp_netif_t *netif = (esp_netif_t *)event_data;

    ESP_LOGI(TAG, "PPP state changed event %" PRId32, event_id);
    switch (event_id) {
        case NETIF_PPP_ERRORNONE:
            self->connected = true;
            break;

        case PPPERR_USER:
            self->clean_close = true;
            break;

        case PPPERR_CONNECT:
            self->connected = false;
            break;

        default:
            break;
    }
}

#if 0
static void on_modem_event(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data) {
    ESP_LOGD(TAG, "on_modem_event");
    ppp_if_obj_t *self = (ppp_if_obj_t *)arg;
    if (event_base == IP_EVENT) {
        ESP_LOGD(TAG, "IP event! %" PRId32, event_id);
        if (event_id == IP_EVENT_PPP_GOT_IP) {
            ESP_LOGI(TAG, "GOT ip event!!!");

            esp_netif_dns_info_t dns_info;
            ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;
            esp_netif_t *netif = event->esp_netif;

            ESP_LOGI(TAG, "Modem Connect to PPP Server");
            ESP_LOGI(TAG, "~~~~~~~~~~~~~~");
            ESP_LOGI(TAG, "IP          : " IPSTR, IP2STR(&event->ip_info.ip));
            ESP_LOGI(TAG, "Netmask     : " IPSTR, IP2STR(&event->ip_info.netmask));
            ESP_LOGI(TAG, "Gateway     : " IPSTR, IP2STR(&event->ip_info.gw));
            esp_netif_get_dns_info(netif, ESP_NETIF_DNS_MAIN, &dns_info);
            ESP_LOGI(TAG, "Name Server1: " IPSTR, IP2STR(&dns_info.ip.u_addr.ip4));
            esp_netif_get_dns_info(netif, ESP_NETIF_DNS_BACKUP, &dns_info);
            ESP_LOGI(TAG, "Name Server2: " IPSTR, IP2STR(&dns_info.ip.u_addr.ip4));
            ESP_LOGI(TAG, "~~~~~~~~~~~~~~");
            self->connected = true;
        } else if (event_id == IP_EVENT_PPP_LOST_IP) {
            ESP_LOGI(TAG, "Modem Disconnect from PPP Server");
            self->connected = false;
        } else if (event_id == IP_EVENT_GOT_IP6) {
            ESP_LOGI(TAG, "GOT IPv6 event!");
            ip_event_got_ip6_t *event = (ip_event_got_ip6_t *)event_data;
            ESP_LOGI(TAG, "Got IPv6 address " IPV6STR, IPV62STR(event->ip6_info.ip));
        }
    }
}
#endif

static esp_err_t esp_ppp_transmit(void *h, void *buffer, size_t len) {
    ESP_LOGD(TAG, "transmit");
    esp_ppp_netif_glue_t *netif_glue = (esp_ppp_netif_glue_t *)h;
    int err;
    mp_stream_rw(netif_glue->stream, buffer, len, &err, MP_STREAM_RW_WRITE);
    return ESP_OK;
}

static esp_err_t esp_ppp_post_attach(esp_netif_t *esp_netif, void *args) {
    ESP_LOGI(TAG, "post attach");
    esp_ppp_netif_glue_t *netif_glue = (esp_ppp_netif_glue_t *)args;
    netif_glue->base.netif = esp_netif;

    // set driver related config to esp-netif
    esp_netif_driver_ifconfig_t driver_ifconfig = {
        .handle = netif_glue,
        .transmit = esp_ppp_transmit,
    };
    ESP_ERROR_CHECK(esp_netif_set_driver_config(esp_netif, &driver_ifconfig));

    // check if PPP error events are enabled, if not, do enable the error occurred/state changed
    // to notify the modem layer when switching modes
    esp_netif_ppp_config_t ppp_config = { 0 };
    ppp_config.ppp_phase_event_enabled = true;    // assuming phase enabled, as earlier IDFs
    ppp_config.ppp_error_event_enabled = false;   // don't provide cfg getters so we enable both events
    #if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(4, 4, 0)
    esp_netif_ppp_get_params(esp_netif, &ppp_config);
    #endif // ESP-IDF >= v4.4
    if (!ppp_config.ppp_error_event_enabled) {
        ppp_config.ppp_error_event_enabled = true;
        esp_netif_ppp_set_params(esp_netif, &ppp_config);
    }

    return ESP_OK;
}

esp_ppp_netif_glue_t *esp_ppp_new_netif_glue(ppp_if_obj_t *self) {
    ESP_LOGI(TAG, "create netif glue");
    esp_ppp_netif_glue_t *netif_glue = m_malloc0(sizeof(esp_ppp_netif_glue_t));
    if (!netif_glue) {
        ESP_LOGE(TAG, "create netif glue failed");
        return NULL;
    }
    netif_glue->stream = self->stream;
    netif_glue->base.post_attach = esp_ppp_post_attach;
    ESP_ERROR_CHECK(esp_event_handler_register(NETIF_PPP_STATUS, ESP_EVENT_ANY_ID, &on_ppp_changed, self));
    // ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, ESP_EVENT_ANY_ID, on_modem_event, self));
    // ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_PPP_GOT_IP, esp_netif_action_connected, ppp_netif));
    // ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_PPP_LOST_IP, esp_netif_action_disconnected, ppp_netif));
    return netif_glue;
}


static mp_obj_t ppp_make_new(mp_obj_t stream) {
    mp_get_stream_raise(stream, MP_STREAM_OP_READ | MP_STREAM_OP_WRITE);

    ppp_if_obj_t *self = mp_obj_malloc_with_finaliser(ppp_if_obj_t, &ppp_if_type);
    self->stream = stream;
    self->active = false;
    self->connected = false;
    self->clean_close = false;
    self->client_task_handle = NULL;

    esp_netif_config_t cfg = ESP_NETIF_DEFAULT_PPP();
    self->base.netif = esp_netif_new(&cfg);
    self->netif_glue = esp_ppp_new_netif_glue(self);
    if (esp_netif_attach(self->base.netif, self->netif_glue) != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("esp_netif_attach failed"));
    }
    self->deinited = false;

    return MP_OBJ_FROM_PTR(self);
}
MP_DEFINE_CONST_FUN_OBJ_1(esp_network_ppp_make_new_obj, ppp_make_new);

static void pppos_client_task(void *self_in) {
    ppp_if_obj_t *self = (ppp_if_obj_t *)self_in;
    uint8_t buf[256];

    int len = 0;
    while (ulTaskNotifyTake(pdTRUE, len <= 0) == 0) {
        int err;
        len = mp_stream_rw(self->stream, buf, sizeof(buf), &err, 0);
        if (len > 0) {
            esp_netif_receive(self->base.netif, (u8_t *)buf, len, NULL);
        }
    }

    self->client_task_handle = NULL;
    vTaskDelete(NULL);
    for (;;) {
    }
}

static mp_obj_t ppp_active(size_t n_args, const mp_obj_t *args) {
    ppp_if_obj_t *self = MP_OBJ_TO_PTR(args[0]);

    if (n_args > 1) {
        if (mp_obj_is_true(args[1])) {
            if (self->active) {
                return mp_const_true;
            }

            self->active = true;
        } else {
            if (!self->active) {
                return mp_const_false;
            }

            if (self->client_task_handle != NULL) { // is connecting or connected?
                // Wait for PPPERR_USER, with timeout
                esp_netif_action_stop(self->base.netif, 0, 0, 0);
                uint32_t t0 = mp_hal_ticks_ms();
                while (!self->clean_close && mp_hal_ticks_ms() - t0 < PPP_CLOSE_TIMEOUT_MS) {
                    mp_hal_delay_ms(10);
                }

                // Shutdown task
                xTaskNotifyGive(self->client_task_handle);
                t0 = mp_hal_ticks_ms();
                while (self->client_task_handle != NULL && mp_hal_ticks_ms() - t0 < PPP_CLOSE_TIMEOUT_MS) {
                    mp_hal_delay_ms(10);
                }
            }

            // Release PPP
            self->active = false;
            self->connected = false;
            self->clean_close = false;
        }
    }
    return mp_obj_new_bool(self->active);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(ppp_active_obj, 1, 2, ppp_active);

static mp_obj_t ppp_connect_py(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    enum { ARG_authmode, ARG_username, ARG_password };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_authmode, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = PPPAUTHTYPE_NONE} },
        { MP_QSTR_username, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_password, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
    };

    mp_arg_val_t parsed_args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, parsed_args);

    ppp_if_obj_t *self = MP_OBJ_TO_PTR(args[0]);

    if (!self->active) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("must be active"));
    }

    if (self->client_task_handle != NULL) {
        mp_raise_OSError(MP_EALREADY);
    }

    switch (parsed_args[ARG_authmode].u_int) {
        case PPPAUTHTYPE_NONE:
        case PPPAUTHTYPE_PAP:
        case PPPAUTHTYPE_CHAP:
            break;
        default:
            mp_raise_ValueError(MP_ERROR_TEXT("invalid auth"));
    }

    if (parsed_args[ARG_authmode].u_int != PPPAUTHTYPE_NONE) {
        const char *username_str = mp_obj_str_get_str(parsed_args[ARG_username].u_obj);
        const char *password_str = mp_obj_str_get_str(parsed_args[ARG_password].u_obj);
        esp_netif_ppp_set_auth(self->base.netif, parsed_args[ARG_authmode].u_int, username_str, password_str);
    }
    if (esp_netif_set_default_netif(self->base.netif) != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("set default failed"));
    }

    esp_netif_action_start(self->base.netif, 0, 0, 0);

    if (xTaskCreatePinnedToCore(pppos_client_task, "ppp", 2048, self, 1, (TaskHandle_t *)&self->client_task_handle, MP_TASK_COREID) != pdPASS) {
        mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("failed to create worker task"));
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_KW(ppp_connect_obj, 1, ppp_connect_py);

static mp_obj_t ppp_delete(mp_obj_t self_in) {
    ppp_if_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->deinited) {
        return mp_const_none;
    }
    mp_obj_t args[] = {self, mp_const_false};
    ppp_active(2, args);
    esp_netif_destroy(self->base.netif);
    m_free(self->netif_glue);
    self->deinited = true;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(ppp_delete_obj, ppp_delete);

static mp_obj_t ppp_status(mp_obj_t self_in) {
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ppp_status_obj, ppp_status);

static mp_obj_t ppp_isconnected(mp_obj_t self_in) {
    ppp_if_obj_t *self = MP_OBJ_TO_PTR(self_in);
    return mp_obj_new_bool(self->connected);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ppp_isconnected_obj, ppp_isconnected);

static mp_obj_t ppp_config(size_t n_args, const mp_obj_t *args, mp_map_t *kwargs) {
    if (n_args != 1 && kwargs->used != 0) {
        mp_raise_TypeError(MP_ERROR_TEXT("either pos or kw args are allowed"));
    }
    ppp_if_obj_t *self = MP_OBJ_TO_PTR(args[0]);

    if (kwargs->used != 0) {
        for (size_t i = 0; i < kwargs->alloc; i++) {
            if (mp_map_slot_is_filled(kwargs, i)) {
                switch (mp_obj_str_get_qstr(kwargs->table[i].key)) {
                    default:
                        break;
                }
            }
        }
        return mp_const_none;
    }

    if (n_args != 2) {
        mp_raise_TypeError(MP_ERROR_TEXT("can query only one param"));
    }

    mp_obj_t val = mp_const_none;

    switch (mp_obj_str_get_qstr(args[1])) {
        case MP_QSTR_ifname: {
            val = mp_obj_new_str_from_cstr("ppp");
            break;
        }
        default:
            mp_raise_ValueError(MP_ERROR_TEXT("unknown config param"));
    }

    return val;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(ppp_config_obj, 1, ppp_config);

static const mp_rom_map_elem_t ppp_if_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_active), MP_ROM_PTR(&ppp_active_obj) },
    { MP_ROM_QSTR(MP_QSTR_connect), MP_ROM_PTR(&ppp_connect_obj) },
    { MP_ROM_QSTR(MP_QSTR_isconnected), MP_ROM_PTR(&ppp_isconnected_obj) },
    { MP_ROM_QSTR(MP_QSTR_status), MP_ROM_PTR(&ppp_status_obj) },
    { MP_ROM_QSTR(MP_QSTR_config), MP_ROM_PTR(&ppp_config_obj) },
    { MP_ROM_QSTR(MP_QSTR_ifconfig), MP_ROM_PTR(&esp_network_ifconfig_obj) },
    { MP_ROM_QSTR(MP_QSTR_ipconfig), MP_ROM_PTR(&esp_nic_ipconfig_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_default), MP_ROM_PTR(&esp_nic_set_default_obj) },
    { MP_ROM_QSTR(MP_QSTR___del__), MP_ROM_PTR(&ppp_delete_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&ppp_delete_obj) },
    { MP_ROM_QSTR(MP_QSTR_AUTH_NONE), MP_ROM_INT(PPPAUTHTYPE_NONE) },
    { MP_ROM_QSTR(MP_QSTR_AUTH_PAP), MP_ROM_INT(PPPAUTHTYPE_PAP) },
    { MP_ROM_QSTR(MP_QSTR_AUTH_CHAP), MP_ROM_INT(PPPAUTHTYPE_CHAP) },
};
static MP_DEFINE_CONST_DICT(ppp_if_locals_dict, ppp_if_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    ppp_if_type,
    MP_QSTR_PPP,
    MP_TYPE_FLAG_NONE,
    locals_dict, &ppp_if_locals_dict
    );

#endif
