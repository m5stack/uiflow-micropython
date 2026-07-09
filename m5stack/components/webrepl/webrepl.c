#include "webrepl.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_timer.h"
#include "esp_wifi.h"
#include "esp_websocket_client.h"
#include "nvs.h"
#include "cJSON.h"

#include "py/mperrno.h"
#include "py/mpstate.h"
#include "py/obj.h"
#include "py/ringbuf.h"
#include "py/runtime.h"
#include "py/stream.h"
#include "shared/runtime/interrupt_char.h"

#define WEBREPL_TAG "webrepl"
#define WEBREPL_URI_TEMPLATE "ws://%s/ws/realtime?role=device&mac=%s"
#define WEBREPL_NVS_NAMESPACE "uiflow"
#define WEBREPL_NVS_SERVER_KEY "server"
#define WEBREPL_ENABLED_SERVER "aiflow.m5stack.com"
#define WEBREPL_SERVER_MAX_LEN 96

#define WEBREPL_RX_BUF_SIZE 4096
#define WEBREPL_TX_BUF_SIZE 8192
#define WEBREPL_JSON_BUF_SIZE 8192
#define WEBREPL_SEND_CHUNK_SIZE 512
#define WEBREPL_HEARTBEAT_US (25LL * 1000LL * 1000LL)
#define WEBREPL_RESTART_DELAY_US (3LL * 1000LL * 1000LL)
#define WEBREPL_STATS_INTERVAL_US (5LL * 1000LL * 1000LL)
#define WEBREPL_LOOP_DELAY_MS 20

extern bool wifi_sta_connected;
extern bool lan_connected;
extern int mp_interrupt_char;
extern ringbuf_t stdin_ringbuf;
void mp_hal_wake_main_task(void);

TaskHandle_t webrepl_task_handle = NULL;

static esp_websocket_client_handle_t webrepl_client = NULL;
static volatile bool webrepl_connected = false;
static volatile bool webrepl_need_pong = false;
static volatile int64_t webrepl_last_activity_us = 0;
static int64_t webrepl_last_start_try_us = 0;

static uint8_t webrepl_rx_buf[WEBREPL_RX_BUF_SIZE];
static size_t webrepl_rx_head = 0;
static size_t webrepl_rx_tail = 0;
static size_t webrepl_rx_used = 0;

static uint8_t webrepl_tx_buf[WEBREPL_TX_BUF_SIZE];
static size_t webrepl_tx_head = 0;
static size_t webrepl_tx_tail = 0;
static size_t webrepl_tx_used = 0;
static size_t webrepl_tx_dropped = 0;

static char webrepl_json_buf[WEBREPL_JSON_BUF_SIZE];
static size_t webrepl_json_len = 0;
static char webrepl_uri[192] = {0};

static portMUX_TYPE webrepl_rx_mux = portMUX_INITIALIZER_UNLOCKED;
static portMUX_TYPE webrepl_tx_mux = portMUX_INITIALIZER_UNLOCKED;

static volatile size_t webrepl_rx_received_total = 0;
static volatile size_t webrepl_rx_dropped_total = 0;
static volatile size_t webrepl_rx_read_total = 0;
static volatile size_t webrepl_stdin_drained_total = 0;
static volatile size_t webrepl_ctrl_c_total = 0;
static volatile size_t webrepl_tx_queued_total = 0;
static volatile size_t webrepl_tx_sent_total = 0;
static volatile bool webrepl_dupterm_installed = false;

typedef struct _webrepl_stream_obj_t {
    mp_obj_base_t base;
} webrepl_stream_obj_t;

static mp_uint_t webrepl_stream_read(mp_obj_t self_in, void *buf, mp_uint_t size, int *errcode);
static mp_uint_t webrepl_stream_write(mp_obj_t self_in, const void *buf, mp_uint_t size, int *errcode);
static mp_uint_t webrepl_stream_ioctl(mp_obj_t self_in, mp_uint_t request, uintptr_t arg, int *errcode);

static const mp_stream_p_t webrepl_stream_p = {
    .read = webrepl_stream_read,
    .write = webrepl_stream_write,
    .ioctl = webrepl_stream_ioctl,
};

static MP_DEFINE_CONST_OBJ_TYPE(
    webrepl_stream_type,
    MP_QSTR_dupterm,
    MP_TYPE_FLAG_NONE,
    protocol, &webrepl_stream_p
    );

static const webrepl_stream_obj_t webrepl_stream_obj = {
    .base = { &webrepl_stream_type },
};

static void webrepl_rx_push(uint8_t ch);

static inline void webrepl_wake_main_task(void) {
    mp_hal_wake_main_task();
}

static bool webrepl_read_nvs_server_key(nvs_handle_t nvs_handle, const char *key, char *server, size_t server_len) {
    size_t len = server_len;
    server[0] = '\0';
    esp_err_t err = nvs_get_str(nvs_handle, key, server, &len);
    if (err == ESP_ERR_NVS_NOT_FOUND) {
        return false;
    }
    if (err != ESP_OK) {
        ESP_LOGW(WEBREPL_TAG, "read nvs %s failed: %s", key, esp_err_to_name(err));
        return false;
    }
    return server[0] != '\0';
}

static bool webrepl_read_server(char *server, size_t server_len) {
    nvs_handle_t nvs_handle;
    esp_err_t err = nvs_open(WEBREPL_NVS_NAMESPACE, NVS_READONLY, &nvs_handle);
    if (err != ESP_OK) {
        ESP_LOGW(WEBREPL_TAG, "open nvs %s failed: %s", WEBREPL_NVS_NAMESPACE, esp_err_to_name(err));
        return false;
    }

    bool ok = webrepl_read_nvs_server_key(nvs_handle, WEBREPL_NVS_SERVER_KEY, server, server_len);
    nvs_close(nvs_handle);
    if (!ok) {
        ESP_LOGW(WEBREPL_TAG, "nvs %s not configured", WEBREPL_NVS_SERVER_KEY);
    }
    return ok;
}

bool webrepl_should_start(void) {
    char server[WEBREPL_SERVER_MAX_LEN] = {0};
    return webrepl_read_server(server, sizeof(server)) && strcmp(server, WEBREPL_ENABLED_SERVER) == 0;
}

static bool webrepl_build_uri(void) {
    uint8_t mac[6] = {0};
    char mac_str[13] = {0};
    char server[WEBREPL_SERVER_MAX_LEN] = {0};
    esp_err_t err = esp_wifi_get_mac(WIFI_IF_STA, mac);
    if (err != ESP_OK) {
        ESP_LOGW(WEBREPL_TAG, "read mac failed: %s, fallback 000000000000", esp_err_to_name(err));
    }

    snprintf(mac_str, sizeof(mac_str), "%02x%02x%02x%02x%02x%02x",
        mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    if (!webrepl_read_server(server, sizeof(server))) {
        return false;
    }
    snprintf(webrepl_uri, sizeof(webrepl_uri), WEBREPL_URI_TEMPLATE, server, mac_str);
    return true;
}

static void webrepl_rx_clear_locked(void) {
    webrepl_rx_head = 0;
    webrepl_rx_tail = 0;
    webrepl_rx_used = 0;
}

static void webrepl_interrupt(void) {
    portENTER_CRITICAL(&webrepl_rx_mux);
    webrepl_rx_clear_locked();
    portEXIT_CRITICAL(&webrepl_rx_mux);

    webrepl_ctrl_c_total++;
    webrepl_rx_push(0x03);
    ESP_LOGD(WEBREPL_TAG, "ctrl-c queued");
    webrepl_wake_main_task();
}

static void webrepl_rx_push(uint8_t ch) {
    portENTER_CRITICAL(&webrepl_rx_mux);
    if (webrepl_rx_used < WEBREPL_RX_BUF_SIZE) {
        webrepl_rx_buf[webrepl_rx_head] = ch;
        webrepl_rx_head = (webrepl_rx_head + 1) % WEBREPL_RX_BUF_SIZE;
        webrepl_rx_used++;
    } else {
        webrepl_rx_dropped_total++;
    }
    portEXIT_CRITICAL(&webrepl_rx_mux);
}

static bool webrepl_rx_pop(uint8_t *ch) {
    bool ok = false;
    portENTER_CRITICAL(&webrepl_rx_mux);
    if (webrepl_rx_used > 0) {
        *ch = webrepl_rx_buf[webrepl_rx_tail];
        webrepl_rx_tail = (webrepl_rx_tail + 1) % WEBREPL_RX_BUF_SIZE;
        webrepl_rx_used--;
        ok = true;
    }
    portEXIT_CRITICAL(&webrepl_rx_mux);
    return ok;
}

static bool webrepl_rx_peek(uint8_t *ch) {
    bool ok = false;
    portENTER_CRITICAL(&webrepl_rx_mux);
    if (webrepl_rx_used > 0) {
        *ch = webrepl_rx_buf[webrepl_rx_tail];
        ok = true;
    }
    portEXIT_CRITICAL(&webrepl_rx_mux);
    return ok;
}

static void webrepl_queue_input(const char *data, size_t len) {
    webrepl_rx_received_total += len;
    for (size_t i = 0; i < len; i++) {
        uint8_t ch = (uint8_t)data[i];
        if (ch == 0x03) {
            webrepl_interrupt();
            continue;
        }
        if (ch == '\n') {
            ch = '\r';
        }
        webrepl_rx_push(ch);
    }
    webrepl_wake_main_task();
}

static void webrepl_drain_rx_to_stdin(void) {
    uint8_t ch;
    while (webrepl_rx_peek(&ch)) {
        if (ch == 0x03 && mp_interrupt_char == 0x03) {
            webrepl_rx_pop(&ch);
            mp_sched_keyboard_interrupt();
            webrepl_rx_read_total++;
            ESP_LOGD(WEBREPL_TAG, "ctrl-c interrupt scheduled");
            continue;
        }

        if (ringbuf_free(&stdin_ringbuf) <= 0) {
            break;
        }
        if (!webrepl_rx_pop(&ch)) {
            break;
        }
        ringbuf_put(&stdin_ringbuf, ch);
        webrepl_stdin_drained_total++;
        webrepl_rx_read_total++;
    }
}

static void webrepl_queue_output(const char *str, size_t len) {
    if (!webrepl_connected || str == NULL || len == 0) {
        return;
    }

    portENTER_CRITICAL(&webrepl_tx_mux);
    for (size_t i = 0; i < len; i++) {
        if (webrepl_tx_used >= WEBREPL_TX_BUF_SIZE) {
            webrepl_tx_dropped += len - i;
            break;
        }
        webrepl_tx_buf[webrepl_tx_head] = (uint8_t)str[i];
        webrepl_tx_head = (webrepl_tx_head + 1) % WEBREPL_TX_BUF_SIZE;
        webrepl_tx_used++;
        webrepl_tx_queued_total++;
    }
    portEXIT_CRITICAL(&webrepl_tx_mux);
}

static mp_uint_t webrepl_stream_read(mp_obj_t self_in, void *buf, mp_uint_t size, int *errcode) {
    (void)self_in;
    if (size == 0) {
        return 0;
    }

    *errcode = MP_EAGAIN;
    return MP_STREAM_ERROR;
}

static mp_uint_t webrepl_stream_write(mp_obj_t self_in, const void *buf, mp_uint_t size, int *errcode) {
    (void)self_in;
    (void)errcode;
    webrepl_queue_output((const char *)buf, size);
    return size;
}

static mp_uint_t webrepl_stream_ioctl(mp_obj_t self_in, mp_uint_t request, uintptr_t arg, int *errcode) {
    (void)self_in;
    (void)errcode;

    if (request == MP_STREAM_POLL) {
        mp_uint_t ret = 0;

        if (webrepl_connected && (arg & MP_STREAM_POLL_WR)) {
            ret |= MP_STREAM_POLL_WR;
        }
        return ret;
    }

    *errcode = MP_EINVAL;
    return MP_STREAM_ERROR;
}

static size_t webrepl_tx_pop_chunk(char *out, size_t max_len) {
    size_t n = 0;
    portENTER_CRITICAL(&webrepl_tx_mux);
    while (n < max_len && webrepl_tx_used > 0) {
        out[n++] = (char)webrepl_tx_buf[webrepl_tx_tail];
        webrepl_tx_tail = (webrepl_tx_tail + 1) % WEBREPL_TX_BUF_SIZE;
        webrepl_tx_used--;
    }
    portEXIT_CRITICAL(&webrepl_tx_mux);
    return n;
}

static void webrepl_tx_clear(void) {
    portENTER_CRITICAL(&webrepl_tx_mux);
    webrepl_tx_head = 0;
    webrepl_tx_tail = 0;
    webrepl_tx_used = 0;
    webrepl_tx_dropped = 0;
    portEXIT_CRITICAL(&webrepl_tx_mux);
}

static bool webrepl_text_equals(const char *data, int len, const char *text) {
    size_t text_len = strlen(text);
    return len == (int)text_len && memcmp(data, text, text_len) == 0;
}

static void webrepl_process_text_message(const char *data, int len) {
    if (data == NULL || len <= 0) {
        return;
    }

    webrepl_last_activity_us = esp_timer_get_time();

    if (webrepl_text_equals(data, len, "PONG")) {
        return;
    }
    if (webrepl_text_equals(data, len, "PING")) {
        webrepl_need_pong = true;
        return;
    }

    cJSON *root = cJSON_ParseWithLength(data, len);
    if (root == NULL) {
        ESP_LOGD(WEBREPL_TAG, "ignore non-json text len=%d", len);
        return;
    }

    cJSON *type = cJSON_GetObjectItem(root, "type");
    if (cJSON_IsString(type) && strcmp(type->valuestring, "clientMessage") == 0) {
        cJSON *payload = cJSON_GetObjectItem(root, "payload");
        if (cJSON_IsString(payload) && payload->valuestring != NULL) {
            webrepl_queue_input(payload->valuestring, strlen(payload->valuestring));
        } else if (cJSON_IsNumber(payload)) {
            char number_buf[32];
            int n = snprintf(number_buf, sizeof(number_buf), "%g", payload->valuedouble);
            if (n > 0) {
                webrepl_queue_input(number_buf, (size_t)n);
            }
        }
    }

    cJSON_Delete(root);
}

static void webrepl_append_event_data(const esp_websocket_event_data_t *event) {
    if (event->payload_offset == 0) {
        webrepl_json_len = 0;
    }

    if (event->data_len <= 0 || event->data_ptr == NULL) {
        return;
    }

    size_t free_len = WEBREPL_JSON_BUF_SIZE - 1 - webrepl_json_len;
    size_t copy_len = event->data_len < (int)free_len ? (size_t)event->data_len : free_len;
    if (copy_len < (size_t)event->data_len) {
        ESP_LOGW(WEBREPL_TAG, "drop oversized ws message: payload_len=%d", event->payload_len);
    }
    if (copy_len > 0) {
        memcpy(webrepl_json_buf + webrepl_json_len, event->data_ptr, copy_len);
        webrepl_json_len += copy_len;
        webrepl_json_buf[webrepl_json_len] = '\0';
    }
}

static bool webrepl_event_message_complete(const esp_websocket_event_data_t *event) {
    if (event->fin) {
        return true;
    }
    if (event->payload_len > 0 && event->payload_offset + event->data_len >= event->payload_len) {
        return true;
    }
    return false;
}

static void webrepl_ws_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    (void)handler_args;
    (void)base;
    esp_websocket_event_data_t *event = (esp_websocket_event_data_t *)event_data;

    switch (event_id) {
        case WEBSOCKET_EVENT_CONNECTED:
            webrepl_connected = true;
            webrepl_last_activity_us = esp_timer_get_time();
            ESP_LOGD(WEBREPL_TAG, "connected");
            break;

        case WEBSOCKET_EVENT_DISCONNECTED:
        case WEBSOCKET_EVENT_CLOSED:
        case WEBSOCKET_EVENT_ERROR:
            webrepl_connected = false;
            webrepl_tx_clear();
            ESP_LOGW(WEBREPL_TAG, "disconnected/error event: %ld", event_id);
            break;

        case WEBSOCKET_EVENT_DATA:
            webrepl_append_event_data(event);
            if (webrepl_event_message_complete(event)) {
                webrepl_process_text_message(webrepl_json_buf, (int)webrepl_json_len);
                webrepl_json_len = 0;
            }
            break;

        default:
            break;
    }
}

static void webrepl_send_text(const char *data, int len) {
    if (!webrepl_connected || webrepl_client == NULL || data == NULL || len <= 0) {
        return;
    }
    int ret = esp_websocket_client_send_text(webrepl_client, data, len, pdMS_TO_TICKS(50));
    if (ret < 0) {
        ESP_LOGW(WEBREPL_TAG, "send failed: %d", ret);
        webrepl_connected = false;
    } else {
        webrepl_tx_sent_total += len;
    }
}

static void webrepl_drain_tx(void) {
    static char chunk[WEBREPL_SEND_CHUNK_SIZE];
    if (!webrepl_connected) {
        return;
    }
    size_t n = webrepl_tx_pop_chunk(chunk, sizeof(chunk));
    if (n > 0) {
        webrepl_send_text(chunk, (int)n);
    }
}

static void webrepl_send_heartbeat_if_due(void) {
    static int64_t last_ping_us = 0;
    int64_t now = esp_timer_get_time();
    if (!webrepl_connected) {
        last_ping_us = now;
        return;
    }
    if (last_ping_us == 0 || now - last_ping_us >= WEBREPL_HEARTBEAT_US) {
        webrepl_send_text("PING", 4);
        last_ping_us = now;
    }
    if (webrepl_need_pong) {
        webrepl_need_pong = false;
        webrepl_send_text("PONG", 4);
    }
}

static void webrepl_wait_network(void) {
    ESP_LOGD(WEBREPL_TAG, "waiting for network");
    while (!(wifi_sta_connected || lan_connected)) {
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

static esp_err_t webrepl_start_client(void) {
    if (webrepl_client != NULL) {
        return ESP_OK;
    }

    webrepl_last_start_try_us = esp_timer_get_time();
    esp_websocket_client_config_t cfg = {
        .uri = webrepl_uri,
        .task_name = "webrepl_ws",
        .task_stack = 6144,
        .task_prio = tskIDLE_PRIORITY + 5,
        .buffer_size = 4096,
        .reconnect_timeout_ms = 3000,
        .network_timeout_ms = 10000,
        .ping_interval_sec = 30,
        .disable_auto_reconnect = false,
        .keep_alive_enable = true,
    };

    webrepl_client = esp_websocket_client_init(&cfg);
    if (webrepl_client == NULL) {
        return ESP_FAIL;
    }
    esp_websocket_register_events(webrepl_client, WEBSOCKET_EVENT_ANY, webrepl_ws_event_handler, NULL);
    esp_err_t err = esp_websocket_client_start(webrepl_client);
    if (err != ESP_OK) {
        ESP_LOGE(WEBREPL_TAG, "websocket start failed: %s", esp_err_to_name(err));
        esp_websocket_client_destroy(webrepl_client);
        webrepl_client = NULL;
    }
    return err;
}

static void webrepl_try_start_client_if_due(void) {
    if (!(wifi_sta_connected || lan_connected) || webrepl_client != NULL) {
        return;
    }
    int64_t now = esp_timer_get_time();
    if (webrepl_last_start_try_us != 0 && now - webrepl_last_start_try_us < WEBREPL_RESTART_DELAY_US) {
        return;
    }
    if (webrepl_start_client() == ESP_OK) {
        ESP_LOGD(WEBREPL_TAG, "websocket client started");
    }
}

static void webrepl_log_stats_if_due(void) {
    static int64_t last_log_us = 0;
    static size_t last_rx_received = 0;
    static size_t last_rx_dropped = 0;
    static size_t last_rx_read = 0;
    static size_t last_stdin_drained = 0;
    static size_t last_ctrl_c = 0;
    static size_t last_tx_queued = 0;
    static size_t last_tx_sent = 0;
    static size_t last_tx_dropped = 0;

    int64_t now = esp_timer_get_time();
    if (last_log_us != 0 && now - last_log_us < WEBREPL_STATS_INTERVAL_US) {
        return;
    }

    size_t rx_received = webrepl_rx_received_total;
    size_t rx_dropped = webrepl_rx_dropped_total;
    size_t rx_read = webrepl_rx_read_total;
    size_t stdin_drained = webrepl_stdin_drained_total;
    size_t ctrl_c = webrepl_ctrl_c_total;
    size_t tx_queued = webrepl_tx_queued_total;
    size_t tx_sent = webrepl_tx_sent_total;
    size_t tx_dropped = webrepl_tx_dropped;

    bool changed = rx_received != last_rx_received
        || rx_dropped != last_rx_dropped
        || rx_read != last_rx_read
        || stdin_drained != last_stdin_drained
        || ctrl_c != last_ctrl_c
        || tx_queued != last_tx_queued
        || tx_sent != last_tx_sent
        || tx_dropped != last_tx_dropped;
    if (!changed) {
        last_log_us = now;
        return;
    }

    ESP_LOGD(WEBREPL_TAG,
        "stats connected=%d dupterm=%d in=%u read=%u stdin=%u rx_drop=%u ctrl_c=%u out=%u sent=%u tx_drop=%u",
        webrepl_connected,
        webrepl_dupterm_installed,
        (unsigned)rx_received,
        (unsigned)rx_read,
        (unsigned)stdin_drained,
        (unsigned)rx_dropped,
        (unsigned)ctrl_c,
        (unsigned)tx_queued,
        (unsigned)tx_sent,
        (unsigned)tx_dropped);

    last_log_us = now;
    last_rx_received = rx_received;
    last_rx_dropped = rx_dropped;
    last_rx_read = rx_read;
    last_stdin_drained = stdin_drained;
    last_ctrl_c = ctrl_c;
    last_tx_queued = tx_queued;
    last_tx_sent = tx_sent;
    last_tx_dropped = tx_dropped;
}

static void webrepl_install_dupterm_if_needed(void) {
    #if MICROPY_PY_OS_DUPTERM
    mp_obj_t stream = MP_OBJ_FROM_PTR(&webrepl_stream_obj);
    mp_obj_t current = MP_STATE_VM(dupterm_objs[0]);
    if (current == stream) {
        webrepl_dupterm_installed = true;
        return;
    }
    if (current != MP_OBJ_NULL) {
        return;
    }

    MP_STATE_VM(dupterm_objs[0]) = stream;
    webrepl_dupterm_installed = true;
    ESP_LOGD(WEBREPL_TAG, "dupterm stream installed");
    #endif
}

void webrepl_task(void *pvParameter) {
    (void)pvParameter;
    webrepl_wait_network();
    if (!webrepl_build_uri()) {
        ESP_LOGE(WEBREPL_TAG, "task stop: server is not configured");
        webrepl_task_handle = NULL;
        vTaskDelete(NULL);
        return;
    }
    ESP_LOGD(WEBREPL_TAG, "task start: %s", webrepl_uri);

    if (webrepl_start_client() != ESP_OK) {
        ESP_LOGE(WEBREPL_TAG, "failed to start websocket client");
    }

    for (;;) {
        if (!(wifi_sta_connected || lan_connected)) {
            webrepl_connected = false;
        }
        webrepl_install_dupterm_if_needed();
        webrepl_try_start_client_if_due();
        webrepl_drain_rx_to_stdin();
        webrepl_drain_tx();
        webrepl_send_heartbeat_if_due();
        webrepl_log_stats_if_due();
        vTaskDelay(pdMS_TO_TICKS(WEBREPL_LOOP_DELAY_MS));
    }
}
