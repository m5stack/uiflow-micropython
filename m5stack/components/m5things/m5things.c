/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#pragma GCC diagnostic ignored "-Wunused-function"
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <sys/time.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_wifi.h"
#include "esp_ota_ops.h"
#include "esp_sntp.h"
#include "esp_log.h"
#include "uart.h"
#include "aes/esp_aes.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "cJSON.h"
#include "m5things.h"
#include "uiflow_utility.h"
#include "boards.h"
#include "esp_timer.h"
#include "esp_mac.h"
#include "esp_psram.h"
#include "crypto.h"
#include "_vfs_stream.h"
#include "esp_netif_sntp.h"
#include "esp_sntp.h"

/** macro definitions */
#define TAG "M5Things"

#define DEBUG_printf(fmt, ...) // mp_printf(&mp_plat_print, fmt"\r\n", ##__VA_ARGS__)

typedef enum {
    E_M5THING_FILE_OP_WRITE = 0,
    E_M5THING_FILE_OP_READ,
    E_M5THING_FILE_OP_LIST,
    E_M5THING_FILE_OP_REMOVE,
    E_M5THING_FILE_OP_WRITE_V2,
    E_M5THING_FILE_OP_MULTI_WRITE,
    E_M5THING_FILE_OP_LIST_V2,
    E_M5THING_FILE_OP_MAX,
} m5thing_file_operator_t;

/** type definitions */
typedef struct _msg_ping_req_t
{
    int category;
    char device_key[64];
    char device_token[64];
    char account[32];
    char mac[9];
    char user_name[64];
    char avatar[128];
} msg_ping_req_t;

typedef struct _msg_exec_req_t
{
    int sn;
    int total;
    int index;
    int len;
    uint8_t *ctx_buf;
} msg_exec_req_t;

typedef struct _msg_file_req_t
{
    unsigned char operator;
    char path[128];
    int sn;
    int total;
    int index;
    int len;
    uint8_t *ctx_buf;
    cJSON *file_list;
    time_t time;
    size_t total_size;
} msg_file_req_t;

/** local function prototypes */
static void mqtt_message_handle(void *event_data);

/** exported variables */
TaskHandle_t m5thing_task_handle;
esp_mqtt_client_handle_t m5things_mqtt_client = NULL;

volatile m5things_status_t m5things_cnct_status = M5THING_STATUS_STANDBY;
volatile m5things_info_t m5things_info;
volatile char pair_code[16] = {0};
volatile char alias_name[32] = {0};

/** local variables */

// order is request.
const char *topic_action_list[] = {"ping", "exec", "file", "syscmd"};
const char *file_op_dsc[] = {"WRITE", "READ", "LIST", "REMOVE", "WRITE_V2", "MULTI_WRITE"};
const char *result_dsc[] = {
    "Success",
    "JSON parse error",
    "Packet data is not continuous",
    "Inconsistent data length",
    "Inconsistent data length",
    "File open error",
    "File read error",
    "File write error",
    "File close error",
    "No such file or directory",
    "File remove error",
    "File list error",
    "No memory",
};

// This topic is used for send status to cloud.
static char mqtt_up_ping_topic[64] = {0};
static char mqtt_down_ping_topic[64] = {0};
// This topic is used for execute code.
static char mqtt_up_exec_topic[64] = {0};
static char mqtt_down_exec_topic[64] = {0};
// This topic is used for send file to device from cloud.
static char mqtt_up_file_topic[64] = {0};
static char mqtt_down_file_topic[64] = {0};

static char mqtt_up_paircode_topic[64] = {0};
static char mqtt_down_paircode_topic[64] = {0};

static char *up_topic_list[4] = {
    mqtt_up_ping_topic,
    mqtt_up_exec_topic,
    mqtt_up_file_topic,
    mqtt_up_paircode_topic,
};
static char *down_topic_list[4] = {
    mqtt_down_ping_topic,
    mqtt_down_exec_topic,
    mqtt_down_file_topic,
    mqtt_down_paircode_topic,
};

static SemaphoreHandle_t xSemaphore = NULL;
static char *json_buf = NULL;

static void mqtt_ping_report();
static void mqtt_paircode_report();

/******************************************************************************/

static void log_error_if_nonzero(const char *message, int error_code) {
    if (error_code != 0) {
        ESP_LOGE(TAG, "Last error %s: 0x%x", message, error_code);
    }
}

static int8_t file_list_helper(const char *path, cJSON *file_list) {
    int8_t ret = PKG_OK;
    const char *full_path = {'\0'};
    lfs2_dir_t dir;

    if (path == NULL || file_list == NULL || !cJSON_IsArray(file_list)) {
        return PKG_ERR_PARSE;
    }

    mp_vfs_mount_t *vfs = mp_vfs_lookup_path(path, &full_path);
    if (vfs == MP_VFS_NONE || vfs == MP_VFS_ROOT) {
        ESP_LOGW(TAG, "vfs not found");
        return PKG_ERR_FILE_OPEN;
    }

    lfs2_t *fs = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(vfs->obj))->lfs;
    if (lfs2_dir_open(fs, &dir, path)) {
        ESP_LOGW(TAG, "No such file or directory");
        return PKG_ERR_FILE_OPEN;
    }

    for (;;) {
        struct lfs2_info info;
        int dir_ret = lfs2_dir_read(fs, &dir, &info);
        if (dir_ret == 0) {
            lfs2_dir_close(fs, &dir);
            ESP_LOGI(TAG, "Read to the end of directory");
            break;
        } else if (dir_ret < 0) {
            return PKG_ERR_FILE_OPEN;
        }
        if (!(
            info.name[0] == '.' && (
                info.name[1] == '\0' || (
                    info.name[1] == '.' && info.name[2] == '\0'
                    )
                )
            )) {
            cJSON_AddItemToArray(file_list, cJSON_CreateString(info.name));
        }
    }

    return ret;
}


static int8_t file_list_helper_v2(const char *path, cJSON *file_list) {
    int8_t ret = PKG_OK;
    const char *full_path = {'\0'};
    lfs2_dir_t dir;

    if (path == NULL || file_list == NULL || !cJSON_IsArray(file_list)) {
        return PKG_ERR_PARSE;
    }

    mp_vfs_mount_t *vfs = mp_vfs_lookup_path(path, &full_path);
    if (vfs == MP_VFS_NONE || vfs == MP_VFS_ROOT) {
        ESP_LOGW(TAG, "vfs not found");
        return PKG_ERR_FILE_OPEN;
    }

    lfs2_t *fs = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(vfs->obj))->lfs;
    if (lfs2_dir_open(fs, &dir, path)) {
        ESP_LOGW(TAG, "No such file or directory");
        return PKG_ERR_FILE_OPEN;
    }

    for (;;) {
        struct lfs2_info info;
        int dir_ret = lfs2_dir_read(fs, &dir, &info);
        if (dir_ret == 0) {
            lfs2_dir_close(fs, &dir);
            ESP_LOGI(TAG, "Read to the end of directory");
            break;
        } else if (dir_ret < 0) {
            return PKG_ERR_FILE_OPEN;
        }
        if (!(
            info.name[0] == '.' && (
                info.name[1] == '\0' || (
                    info.name[1] == '.' && info.name[2] == '\0'
                    )
                )
            )) {
            cJSON *file = cJSON_CreateObject();
            cJSON_AddStringToObject(file, "name", info.name);
            cJSON_AddNullToObject(file, "md5");
            cJSON_AddItemToArray(file_list, file);
        }
    }

    return ret;
}


static int8_t file_remove_helper(const char *path) {
    int8_t ret = PKG_OK;
    const char *full_path = {'\0'};

    if (path == NULL) {
        return PKG_ERR_PARSE;
    }

    mp_vfs_mount_t *vfs = mp_vfs_lookup_path(path, &full_path);
    if (vfs == MP_VFS_NONE || vfs == MP_VFS_ROOT) {
        return PKG_ERR_FILE_OPEN;
    }

    lfs2_t *fs = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(vfs->obj))->lfs;
    ret = lfs2_remove(fs, path) == LFS2_ERR_OK ? PKG_OK : PKG_ERR_FILE_REMOVE;

    return ret;
}

/******************************************************************************/
static void mqtt_event_handler(void *handler_args, esp_event_base_t base,
    int32_t event_id, void *event_data) {
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%ld", base,
        event_id);
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t m5things_mqtt_client = event->client;
    int msg_id;
    switch ((esp_mqtt_event_id_t)event_id) {
        case MQTT_EVENT_ERROR:
            ESP_LOGI(TAG, "MQTT_EVENT_ERROR");
            if (event->error_handle->error_type == MQTT_ERROR_TYPE_TCP_TRANSPORT) {
                log_error_if_nonzero("reported from esp-tls",
                    event->error_handle->esp_tls_last_esp_err);
                log_error_if_nonzero("reported from tls stack",
                    event->error_handle->esp_tls_stack_err);
                log_error_if_nonzero(
                    "captured as transport's socket errno",
                    event->error_handle->esp_transport_sock_errno);
                ESP_LOGE(TAG, "Last errno string (%s)", strerror(event->error_handle->esp_transport_sock_errno));
            }
            m5things_cnct_status = M5THING_STATUS_CNCT_ERR;
            break;
        case MQTT_EVENT_CONNECTED: {
            for (size_t i = 0; i < 3; i++) {
                msg_id = esp_mqtt_client_subscribe(m5things_mqtt_client,
                    down_topic_list[i], 0);
                ESP_LOGI(TAG, "sent %s topic subscribe successful, msg_id=%d",
                    topic_action_list[i], msg_id);
            }
            msg_id = esp_mqtt_client_subscribe(m5things_mqtt_client,
                down_topic_list[3], 0);
            ESP_LOGI(TAG, "sent %s topic subscribe successful, msg_id=%d",
                topic_action_list[3], msg_id);
            mqtt_ping_report();
            mqtt_paircode_report();
            m5things_cnct_status = M5THING_STATUS_CONNECTED;
        } break;
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
            m5things_cnct_status = M5THING_STATUS_DISCONNECT;
            break;
        case MQTT_EVENT_SUBSCRIBED:
            ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_UNSUBSCRIBED:
            ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_PUBLISHED:
            ESP_LOGI(TAG, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_DATA:
            ESP_LOGI(TAG, "MQTT_EVENT_DATA");
            mqtt_message_handle(event);
            break;
        case MQTT_EVENT_BEFORE_CONNECT:
            ESP_LOGI(TAG, "MQTT_EVENT_BEFORE_CONNECT");
            break;
        case MQTT_EVENT_DELETED:
            ESP_LOGI(TAG, "MQTT_EVENT_DELETED");
            break;
        default:
            ESP_LOGI(TAG, "Other event id:%d", event->event_id);
            break;
    }
}


static int mqtt_response_helper(uint8_t _topic_idx, uint64_t _pkg_sn, uint32_t _pkg_idx, int8_t _result) {
    char rsp_buf[64];
    sprintf(rsp_buf, "{\"pkg_sn\":%lld,\"pkg_idx\":%ld,\"err_code\":%d}", _pkg_sn, _pkg_idx, _result);
    return esp_mqtt_client_publish(m5things_mqtt_client, up_topic_list[_topic_idx],
        rsp_buf, strlen(rsp_buf), 0, 0);
}

static int8_t mqtt_ping_process(esp_mqtt_event_handle_t event, uint64_t *_pkg_sn) {
    int8_t ret = PKG_OK;
    *_pkg_sn = 0;
    return ret;
}

static void mqtt_ping_report() {
    char mqtt_report_buf[128] = { 0 };
    const esp_partition_t *running = esp_ota_get_running_partition();
    esp_app_desc_t running_app_info;
    if (esp_ota_get_partition_description(running, &running_app_info) == ESP_OK) {
        ESP_LOGD(TAG, "Running firmware version: %s", running_app_info.version);
    }

    size_t len = 0;

    #if CONFIG_IDF_TARGET_ESP32 && CONFIG_ESP32_SPIRAM_SUPPORT && BOARD_ID == 1
    len = sprintf(
        mqtt_report_buf,
        "{\"status\":\"online\",\"system\":{\"free_heap\":%lu}, \"board_type\":%d, \"board\":\"%s\", \"version\":\"%s\"}",
        esp_get_free_heap_size(),
        BOARD_ID,
        "fire",
        running_app_info.version
        );
    #else
    len = sprintf(
        mqtt_report_buf,
        "{\"status\":\"online\",\"system\":{\"free_heap\":%lu}, \"board_type\":%d, \"board\":\"%s\", \"version\":\"%s\"}",
        esp_get_free_heap_size(),
        BOARD_ID,
        boards[BOARD_ID],
        running_app_info.version
        );
    #endif

    esp_mqtt_client_publish(
        m5things_mqtt_client,
        mqtt_up_ping_topic,
        mqtt_report_buf,
        len,
        0,
        0
        );
}

static void mqtt_paircode_report() {
    char mqtt_report_buf[64] = { 0 };
    size_t len = 0;

    len = sprintf(
        mqtt_report_buf,
        "{\"action\":\"%d\"}",
        0
        );

    esp_mqtt_client_publish(
        m5things_mqtt_client,
        mqtt_up_paircode_topic,
        mqtt_report_buf,
        len,
        0,
        0
        );
}

static int8_t mqtt_ping_parse_all(const char *data, size_t len, msg_ping_req_t *msg) {
    int8_t ret = PKG_OK;

    if (data == NULL || len == 0) {
        ESP_LOGW(TAG, "Message is null");
        ret = PKG_ERR_PARSE;
        return ret;
    }

    cJSON *root = cJSON_ParseWithLength(data, len);
    if (root == NULL || cJSON_IsNull(root)) {
        ESP_LOGW(TAG, "PING JSON parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }

    memset(msg, 0x00, sizeof(msg_ping_req_t));
    cJSON *category_obj = cJSON_GetObjectItemCaseSensitive(root, "category");
    if (category_obj == NULL || cJSON_IsNull(category_obj)) {
        ESP_LOGW(TAG, "'category' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        sscanf(category_obj->valuestring, "%d", &m5things_info.category);
    }

    cJSON *device_key_obj = cJSON_GetObjectItemCaseSensitive(root, "deviceKey");
    if (device_key_obj == NULL || cJSON_IsNull(device_key_obj)) {
        ESP_LOGW(TAG, "'deviceKey' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        memset(m5things_info.device_key, 0x00, sizeof(m5things_info.device_key));
        memcpy(
            (void *)m5things_info.device_key,
            device_key_obj->valuestring,
            strlen(device_key_obj->valuestring)
            );
    }

    cJSON *device_token_obj = cJSON_GetObjectItemCaseSensitive(root, "deviceToken");
    if (device_token_obj == NULL || cJSON_IsNull(device_token_obj)) {
        ESP_LOGW(TAG, "'deviceKey' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        memset(m5things_info.device_key, 0x00, sizeof(m5things_info.device_key));
        memcpy(
            (void *)m5things_info.device_token,
            device_token_obj->valuestring,
            strlen(device_token_obj->valuestring)
            );
    }

    cJSON *email_obj = cJSON_GetObjectItemCaseSensitive(root, "email");
    if (email_obj == NULL || cJSON_IsNull(email_obj)) {
        ESP_LOGW(TAG, "'email' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        memset(m5things_info.device_key, 0x00, sizeof(m5things_info.device_key));
        memcpy(
            (void *)m5things_info.account,
            email_obj->valuestring,
            strlen(email_obj->valuestring)
            );
    }

    cJSON *mac_obj = cJSON_GetObjectItemCaseSensitive(root, "mac");
    if (mac_obj == NULL || cJSON_IsNull(mac_obj)) {
        ESP_LOGW(TAG, "'mac' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        memset(m5things_info.device_key, 0x00, sizeof(m5things_info.device_key));
        memcpy(
            (void *)m5things_info.mac,
            mac_obj->valuestring,
            strlen(mac_obj->valuestring)
            );
    }

    cJSON *user_name_obj = cJSON_GetObjectItemCaseSensitive(root, "userName");
    if (user_name_obj == NULL || cJSON_IsNull(user_name_obj)) {
        ESP_LOGW(TAG, "'userName' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        memset(m5things_info.device_key, 0x00, sizeof(m5things_info.device_key));
        memcpy(
            (void *)m5things_info.user_name,
            user_name_obj->valuestring,
            strlen(user_name_obj->valuestring)
            );
    }

    cJSON *avatar_obj = cJSON_GetObjectItemCaseSensitive(root, "avatar");
    if (avatar_obj == NULL || cJSON_IsNull(avatar_obj)) {
        ESP_LOGW(TAG, "'avatar' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        memset(m5things_info.device_key, 0x00, sizeof(m5things_info.device_key));
        memcpy(
            (void *)m5things_info.avatar,
            avatar_obj->valuestring,
            strlen(avatar_obj->valuestring)
            );
    }

    cJSON_Delete(root);
end:
    return ret;
}


static int8_t mqtt_ping_down_process(esp_mqtt_event_handle_t event, uint64_t *_pkg_sn) {
    msg_ping_req_t msg;
    return mqtt_ping_parse_all(event->data, event->data_len, &msg);
}

static int8_t mqtt_exec_parse_all(const char *data, size_t len, msg_exec_req_t *msg) {
    int8_t ret = PKG_OK;

    if (data == NULL || len == 0) {
        ESP_LOGW(TAG, "Message is null");
        ret = PKG_ERR_PARSE;
        return ret;
    }

    cJSON *root = cJSON_ParseWithLength(data, len);
    if (root == NULL || cJSON_IsNull(root)) {
        ESP_LOGW(TAG, "PING JSON parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }

    memset(msg, 0x00, sizeof(msg_exec_req_t));

    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(root, "pkg_sn");
    if (pkg_sn == NULL || cJSON_IsNull(pkg_sn)) {
        ESP_LOGW(TAG, "'pkg_sn' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        msg->sn = cJSON_GetNumberValue(pkg_sn);
    }

    cJSON *pkg_tot = cJSON_GetObjectItemCaseSensitive(root, "pkg_tot");
    if (pkg_tot == NULL || cJSON_IsNull(pkg_tot)) {
        ESP_LOGW(TAG, "'pkg_tot' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        msg->total = cJSON_GetNumberValue(pkg_tot);
    }

    cJSON *pkg_idx = cJSON_GetObjectItemCaseSensitive(root, "pkg_idx");
    if (pkg_idx == NULL || cJSON_IsNull(pkg_idx)) {
        ESP_LOGW(TAG, "'pkg_idx' parsing failed");
        ret = PKG_ERR_INDEX;
    } else {
        msg->index = cJSON_GetNumberValue(pkg_idx);
    }

    cJSON *pkg_len = cJSON_GetObjectItemCaseSensitive(root, "pkg_len");
    if (pkg_len == NULL || cJSON_IsNull(pkg_len)) {
        ESP_LOGW(TAG, "'pkg_len' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        msg->len = cJSON_GetNumberValue(pkg_len);
    }

    cJSON *pkg_ctx = cJSON_GetObjectItemCaseSensitive(root, "pkg_ctx");
    if (pkg_ctx == NULL || cJSON_IsNull(pkg_ctx)) {
        ESP_LOGW(TAG, "'pkg_ctx' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        size_t decode_len = 0;
        msg->ctx_buf = (unsigned char *)m5_base64_decode(
            pkg_ctx->valuestring, strlen(pkg_ctx->valuestring), &decode_len);

        if (msg->ctx_buf == NULL && strlen(pkg_ctx->valuestring)) {
            ESP_LOGE(TAG, "No memory(@m5_base64_decode)");
            ret = PKG_ERR_NO_MEMORY_AVAILABLE;
            goto error_base64_decode;
        }
        if (msg->len != decode_len) {
            ESP_LOGE(TAG, "base64 decode failed");
            ret = PKG_ERR_LENGTH;
            if (msg->ctx_buf) {
                free(msg->ctx_buf);
            }
        }
    }

error_base64_decode:
    cJSON_Delete(root);
end:
    return ret;
}


static int8_t mqtt_exec_process(esp_mqtt_event_handle_t event, uint64_t *_pkg_sn, uint8_t *_pkg_idx) {
    int8_t ret = PKG_OK;
    msg_exec_req_t msg;

    ret = mqtt_exec_parse_all(event->data, event->data_len, &msg);
    if (ret != PKG_OK) {
        return ret;
    }

    *_pkg_sn = msg.sn;
    *_pkg_idx = msg.index;

    if (msg.index == 0) {
        // while (ringbuf_get(&stdin_ringbuf) != -1) {
        //     ;
        // }

        // enter paste mode
        if (0x03 == mp_interrupt_char) {
            mp_sched_keyboard_interrupt();
        }
        ringbuf_put(&stdin_ringbuf, 0x03);  // CTRL + C
        ringbuf_put(&stdin_ringbuf, 0x05);  // CTRL + E
        const char *sync_code = {"from m5sync import sync\nsync.run()\n"};
        for (size_t i = 0; i < strlen(sync_code); i++) {
            uint8_t c = sync_code[i];
            if (c == 0x0A) {
                c = 0x0D;
            }
            ringbuf_put(&stdin_ringbuf, c);
        }
    }

    // esp_log_buffer_hex("ctx_buf", ctx_buf, decode_len);
    for (size_t idx = 0; idx < msg.len; ++idx) {
        uint8_t c = msg.ctx_buf[idx];
        if (c == 0x0A) {
            c = 0x0D;
        }

        uint64_t timeout = esp_timer_get_time();
        while (ringbuf_free(&stdin_ringbuf) <= 0) {
            vTaskDelay(40 / portTICK_PERIOD_MS);
            ESP_LOGI(TAG, "ringbuf free: %d bytes", ringbuf_free(&stdin_ringbuf));
            if ((esp_timer_get_time() - timeout) > 30000000) {
                ESP_LOGE(TAG, "wait ringbuf free timeout");
                ret = PKG_ERR_EXECUTE;
                goto error_exec;
            }
        }
        ringbuf_put(&stdin_ringbuf, c);  // User Code
    }

    if (msg.index == (msg.total - 1)) {
        ringbuf_put(&stdin_ringbuf, 0x04);  // CTRL + D
    }

error_exec:
    free(msg.ctx_buf);
    return ret;
}


static int8_t file_write_helper(
    const char *path,
    const char *ctx,
    size_t ctx_len,
    bool is_new_file
    ) {
    int8_t ret = PKG_OK;
    int flags = 0;

    if (is_new_file) {
        // NEW + RW + ZERO File
        flags = VFS_CREATE | VFS_WRITE;
    } else {
        // open file, RW + MOVE to END
        flags = VFS_WRITE | VFS_APPEND;
    }

    // open file
    void *stream = vfs_stream_open(path, flags);
    if (!stream) {
        ESP_LOGW(TAG, "File create and open failed");
        ret = PKG_ERR_FILE_OPEN;
        goto out;
    }

    // write file
    size_t write_len = vfs_stream_write(stream, ctx, ctx_len);
    if (write_len != ctx_len) {
        ESP_LOGW(TAG, "File write error, written: %d, total length: %d", write_len, ctx_len);
        ret = PKG_ERR_FILE_WRITE;
        goto out;
    }

out:
    // close file
    vfs_stream_close(stream);
    return ret;
}

static int mqtt_handle_file_write_response_helper(
    uint8_t topic_idx,
    uint64_t pkg_sn,
    uint32_t pkg_idx,
    int8_t result
    ) {
    char rsp_buf[128];
    sprintf(
        rsp_buf,
        "{\"file_op\": %d, \"pkg_sn\":%lld,\"pkg_idx\":%ld,\"err_code\":%d}",
        4,
        pkg_sn,
        pkg_idx,
        result
        );
    ESP_LOGW(TAG, "topic: '%s', msg: '%s'", up_topic_list[topic_idx], rsp_buf);
    return esp_mqtt_client_publish(
        m5things_mqtt_client,
        up_topic_list[topic_idx],
        rsp_buf,
        strlen(rsp_buf),
        0,
        0
        );
}


static int mqtt_handle_multi_file_write_response_helper(
    uint8_t topic_idx,
    uint64_t pkg_sn,
    uint32_t pkg_idx,
    int8_t result
    ) {
    char rsp_buf[128];
    sprintf(
        rsp_buf,
        "{\"file_op\": %d, \"pkg_sn\":%lld,\"pkg_idx\":%ld,\"err_code\":%d}",
        5,
        pkg_sn,
        pkg_idx,
        result
        );
    ESP_LOGW(TAG, "topic: '%s', msg: '%s'", up_topic_list[topic_idx], rsp_buf);
    return esp_mqtt_client_publish(
        m5things_mqtt_client,
        up_topic_list[topic_idx],
        rsp_buf,
        strlen(rsp_buf),
        0,
        0
        );
}

static int8_t mqtt_handle_file_write(msg_file_req_t *msg) {
    int8_t ret = PKG_ERR_PARSE;
    static int last_idx = 0;

    if (msg->index == 0) {
        last_idx = 0;
    } else if (msg->index != last_idx + 1) {
        // Packet data is not continuous
        ESP_LOGW(TAG, "Packet data is not continuous");
        ret = PKG_ERR_INDEX;
        goto error;
    }

    ret = file_write_helper(msg->path, (const char *)msg->ctx_buf, msg->len, msg->index == 0);
    mqtt_handle_file_write_response_helper(TOPIC_FILE_IDX, msg->sn, msg->index, ret);
    vTaskDelay(500 / portTICK_PERIOD_MS);
    last_idx = msg->index;

    // when OTA done need restart device
    if (msg->index == (msg->total - 1)) {
        // path: /flash/main_ota_temp.py
        if ((strstr(msg->path, OTA_UPDATE_FILE_NAME) != NULL)) {
            nvs_write_u8_helper(UIFLOW_NVS_NAMESPACE, "boot_option", BOOT_OPT_NETWORK);
            ESP_LOGW(TAG, "restart now :)");
            esp_restart();
        }
    }

error:
    return ret;
}


cJSON *generate_res_record(void) {
    cJSON *root = cJSON_CreateObject();
    if (root == NULL) {
        ESP_LOGE(TAG, "root object create failed");
        return NULL;
    }

    cJSON *file_list = cJSON_CreateArray();
    if (file_list == NULL) {
        ESP_LOGE(TAG, "file_list object create failed");
        cJSON_Delete(root);
        return NULL;
    }

    cJSON_AddNumberToObject(root, "time", 0);
    cJSON_AddBoolToObject(root, "cache", false);
    cJSON_AddNumberToObject(root, "totalSize", 0);
    cJSON_AddItemToObject(root, "fileList", file_list);
    return root;
}

static size_t vfs_stream_size(const char *path) {
    void *stream = vfs_stream_open(path, VFS_READ);
    if (!stream) {
        return 0;
    }
    size_t size = vfs_stream_seek(stream, 0, SEEK_END);
    vfs_stream_close(stream);
    return size;
}

cJSON *get_res_record(void) {
    cJSON *json = NULL;
    size_t file_size = vfs_stream_size(FILE_RECORD_PATH);
    ESP_LOGI(TAG, "'%s' file size: %d", FILE_RECORD_PATH, file_size);
    if (file_size == 0) {
        ESP_LOGW(TAG, "'%s' file does not exist, create it", FILE_RECORD_PATH);
        json = generate_res_record();
    } else {
        void *stream = vfs_stream_open(FILE_RECORD_PATH, VFS_READ);
        if (stream == NULL) {
            ESP_LOGE(TAG, "Fail to open the file");
            return NULL;
        }
        int8_t *buffer = (int8_t *)malloc(file_size + 1);
        if (buffer == NULL) {
            ESP_LOGE(TAG, "No memory available");
            vfs_stream_close(stream);
            return NULL;
        }
        if (vfs_stream_read(stream, buffer, file_size) != file_size) {
            free(buffer);
            vfs_stream_close(stream);
            return NULL;
        }
        buffer[file_size] = '\0';
        vfs_stream_close(stream);

        json = cJSON_ParseWithLength((const char *)buffer, file_size);
        free(buffer);
    }

    // check json object
    if (!json) {
        const char *error_ptr = cJSON_GetErrorPtr();
        if (error_ptr != NULL) {
            fprintf(stderr, "Error before: %s\n", error_ptr);
        }
    }
    return json;
}


int8_t update_res_record(cJSON *json) {
    int8_t ret = PKG_OK;
    void *stream = vfs_stream_open(FILE_RECORD_PATH, VFS_WRITE | VFS_CREATE);
    if (stream == NULL) {
        ESP_LOGE(TAG, "Fail to open the file");
        ret = PKG_ERR_FILE_OPEN;
        goto out;
    }

    // serialize json object
    char *buf = cJSON_PrintUnformatted(json);
    xSemaphoreTake(xSemaphore, portMAX_DELAY);
    if (buf == NULL) {
        ESP_LOGE(TAG, "json object serialization failed");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
    } else {
        vfs_stream_write(stream, buf, strlen(buf));
        free(buf);
    }
    xSemaphoreGive(xSemaphore);

    vfs_stream_close(stream);
out:
    return ret;
}


static int8_t mqtt_handle_file_write_v2_helper(msg_file_req_t *msg_file_req) {
    int8_t ret = PKG_OK;

    cJSON *json = get_res_record();
    if (json == NULL) {
        ESP_LOGE(TAG, "get res.json failed");
        ret = PKG_ERR_PARSE;
        goto out;
    }

    // process file write request
    cJSON *time = cJSON_GetObjectItemCaseSensitive(json, "time");
    if (time) {
        cJSON_SetNumberValue(time, msg_file_req->time);
    }
    cJSON *totalSize = cJSON_GetObjectItemCaseSensitive(json, "totalSize");
    int total_size = totalSize->valueint;

    cJSON *res_file_list = cJSON_GetObjectItemCaseSensitive(json, "fileList");
    int old_file_num = cJSON_GetArraySize(res_file_list);
    bool exist = false;

    cJSON *new_file = cJSON_GetArrayItem(msg_file_req->file_list, 0);
    if (new_file) {
        cJSON_AddStringToObject(new_file, "devicePath", msg_file_req->path);
        cJSON_AddStringToObject(new_file, "domain", "user");
        total_size += cJSON_GetObjectItemCaseSensitive(new_file, "size")->valueint;

        for (int i = 0; i < old_file_num; i++) {
            cJSON *file = cJSON_GetArrayItem(res_file_list, i);
            cJSON *path = cJSON_GetObjectItemCaseSensitive(file, "devicePath");
            if (strcmp(path->valuestring, msg_file_req->path) == 0) {
                // NOTE: 添加 "devicePath" 保存文件路径
                total_size -= cJSON_GetObjectItemCaseSensitive(file, "size")->valueint;
                cJSON_ReplaceItemInArray(res_file_list, i, cJSON_Duplicate(new_file, true));
                exist = true;
            }
        }
        if (exist == false) {
            // NOTE: 添加 "devicePath" 保存文件路径
            cJSON_AddItemToArray(res_file_list, cJSON_Duplicate(new_file, true));
        }
    } else {
        ESP_LOGW(TAG, "'fileList' object is empty");
        ret = PKG_ERR_PARSE;
        goto out;
    }
    cJSON_SetNumberValue(totalSize, total_size);

    // save res.json
    ret = update_res_record(json);
    cJSON_Delete(json);

out:
    return ret;
}


static int8_t mqtt_handle_file_write_v2(msg_file_req_t *msg) {
    int8_t ret = PKG_ERR_PARSE;
    static int last_idx = 0;

    if (msg->index == 0) {
        last_idx = 0;
    } else if (msg->index != last_idx + 1) {
        // Packet data is not continuous
        ESP_LOGW(TAG, "Packet data is not continuous");
        ret = PKG_ERR_INDEX;
        goto error;
    }

    ret = mqtt_handle_file_write_v2_helper(msg);
    mqtt_handle_file_write_response_helper(TOPIC_FILE_IDX, msg->sn, msg->index, ret);

    if ((strstr(msg->path, OTA_UPDATE_FILE_NAME) != NULL)) {
        nvs_write_u8_helper(UIFLOW_NVS_NAMESPACE, "boot_option", BOOT_OPT_NETWORK);
        ESP_LOGW(TAG, "restart now :)");
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        esp_restart();
    }

error:
    return ret;
}


static int8_t mqtt_handle_multi_file_write_helper(msg_file_req_t *msg_file_req) {
    int8_t ret = PKG_OK;

    // get file record
    cJSON *json = get_res_record();
    if (json == NULL) {
        ESP_LOGE(TAG, "get res.json failed");
        ret = PKG_ERR_PARSE;
        goto out;
    }

    cJSON *time = cJSON_GetObjectItemCaseSensitive(json, "time");
    if (time) {
        cJSON_SetNumberValue(time, msg_file_req->time);
    }
    cJSON *totalSize = cJSON_GetObjectItemCaseSensitive(json, "totalSize");
    int total_size = totalSize->valueint;

    // 对于 multi_file_write 请求，先删除旧的项目域文件
    cJSON *old_file_list = cJSON_GetObjectItemCaseSensitive(json, "fileList");
    int old_file_num = cJSON_GetArraySize(old_file_list);
    // 倒序遍历，避免删除元素后索引变化的问题
    for (int i = old_file_num - 1; i >= 0; i--) {
        cJSON *file = cJSON_GetArrayItem(old_file_list, i);
        cJSON *domain_obj = cJSON_GetObjectItemCaseSensitive(file, "domain");
        if (domain_obj) {
            if (strncmp(domain_obj->valuestring, "project", strlen("project")) == 0) {
                total_size -= cJSON_GetObjectItemCaseSensitive(file, "size")->valueint;
                // 找到匹配的项目域文件，从数组中删除
                cJSON *deleted_item = cJSON_DetachItemFromArray(old_file_list, i);
                if (deleted_item) {
                    cJSON_Delete(deleted_item);
                }
            }
        }
    }
    old_file_num = cJSON_GetArraySize(old_file_list);

    cJSON *new_file_list = msg_file_req->file_list;
    int new_file_num = cJSON_GetArraySize(new_file_list);

    ESP_LOGW(TAG, "old_file_num: %d, new_file_num: %d", old_file_num, new_file_num);

    for (int j = 0; j < new_file_num; j++) {
        cJSON *new_file = cJSON_GetArrayItem(new_file_list, j);
        if (new_file == NULL) {
            continue;
        }
        cJSON *new_file_dir = cJSON_GetObjectItemCaseSensitive(new_file, "devicePath");
        cJSON *new_file_name = cJSON_GetObjectItemCaseSensitive(new_file, "name");
        if (new_file_dir == NULL || new_file_name == NULL) {
            continue;
        }

        char new_file_path[256] = {'\0'};
        sprintf(new_file_path, "%s%s", new_file_dir->valuestring, new_file_name->valuestring);

        bool exist = false;
        for (int i = 0; i < old_file_num; i++) {
            cJSON *file = cJSON_GetArrayItem(old_file_list, i);
            cJSON *old_path = cJSON_GetObjectItemCaseSensitive(file, "devicePath");
            if (strcmp(new_file_path, old_path->valuestring) == 0) {
                total_size -= cJSON_GetObjectItemCaseSensitive(file, "size")->valueint;
                total_size += cJSON_GetObjectItemCaseSensitive(new_file, "size")->valueint;
                cJSON_ReplaceItemInObject(new_file, "devicePath", cJSON_CreateString(new_file_path));
                cJSON_ReplaceItemInArray(old_file_list, i, cJSON_Duplicate(new_file, true));
                exist = true;
            }
        }
        if (exist == false) {
            total_size += cJSON_GetObjectItemCaseSensitive(new_file, "size")->valueint;
            cJSON_ReplaceItemInObject(new_file, "devicePath", cJSON_CreateString(new_file_path));
            // 对于不存在的项目域文件，添加 domain 字段
            cJSON_AddStringToObject(new_file, "domain", "project");
            cJSON_AddItemToArray(old_file_list, cJSON_Duplicate(new_file, true));
        }
    }
    cJSON_SetNumberValue(totalSize, total_size);

    // save res.json
    ret = update_res_record(json);
    cJSON_Delete(json);

out:
    return ret;
}


static int8_t mqtt_handle_multi_file_write_v2(msg_file_req_t *msg) {
    int8_t ret = PKG_ERR_PARSE;
    static int last_idx = 0;

    if (msg->index == 0) {
        last_idx = 0;
    } else if (msg->index != last_idx + 1) {
        // Packet data is not continuous
        ESP_LOGW(TAG, "Packet data is not continuous");
        ret = PKG_ERR_INDEX;
        goto error;
    }

    ret = mqtt_handle_multi_file_write_helper(msg);
    mqtt_handle_multi_file_write_response_helper(TOPIC_FILE_IDX, msg->sn, msg->index, ret);
error:
    return ret;
}


static int mqtt_file_read_response_helper(cJSON *rsp, const char *rsp_buf) {
    int ret = -1;
    if (rsp != NULL) {
        xSemaphoreTake(xSemaphore, portMAX_DELAY);
        memset(json_buf, 0x00, 4096 + 8);
        if (cJSON_PrintPreallocated(rsp, json_buf, 4096 + 8, false)) {
            esp_mqtt_client_publish(
                m5things_mqtt_client,
                mqtt_up_file_topic,
                json_buf,
                strlen(json_buf),
                0,
                0
                );
        } else {
            ESP_LOGW(TAG, "json object serialization failed");
        }
        xSemaphoreGive(xSemaphore);
    } else if (rsp_buf != NULL) {
        ret = esp_mqtt_client_publish(
            m5things_mqtt_client,
            mqtt_up_file_topic,
            rsp_buf,
            strlen(rsp_buf),
            0,
            0
            );
    }
    return ret;
}


static void read_task(void *pvParameter) {
    msg_file_req_t *msg = (msg_file_req_t *)pvParameter;
    int8_t ret = PKG_OK;

    // rsp json
    cJSON *rsp_obj = cJSON_CreateObject();
    if (rsp_obj == NULL) {
        ESP_LOGW(TAG, "Failed to create rsp json object");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char rsp_buf[256] = {0};
        sprintf(
            rsp_buf,
            "{\"file_op\":1,\"%s\",\"pkg_sn\":%d,\"pkg_tot\":1,\"pkg_idx\":0,\"pkg_len\":0,\"pkg_ctx\":\"\",\"err_code\":%d}",
            msg->path,
            msg->sn,
            ret
            );
        mqtt_file_read_response_helper(NULL, rsp_buf);
        goto out;
    }

    cJSON_AddNumberToObject(rsp_obj, "file_op", msg->operator);
    cJSON_AddStringToObject(rsp_obj, "fs_path", msg->path);
    cJSON_AddNumberToObject(rsp_obj, "pkg_sn", msg->sn);
    cJSON *total_obj = cJSON_AddNumberToObject(rsp_obj, "pkg_tot", 1);
    cJSON *index_obj = cJSON_AddNumberToObject(rsp_obj, "pkg_idx", 0);
    cJSON *len_obj = cJSON_AddNumberToObject(rsp_obj, "pkg_len", 0);
    cJSON *ctx_obj = cJSON_AddStringToObject(rsp_obj, "pkg_ctx", "");
    cJSON *err_obj = cJSON_AddNumberToObject(rsp_obj, "err_code", 0);

    // find vfs
    size_t file_size = vfs_stream_size(msg->path);
    if (file_size == 0) {
        ESP_LOGW(TAG, "File '%s' does not exist", msg->path);
        err_obj->valueint = PKG_ERR_FILE_OPEN;
        mqtt_file_read_response_helper(rsp_obj, NULL);
        goto file_err;
    }

    void *stream = vfs_stream_open(msg->path, VFS_READ);
    if (!stream) {
        ESP_LOGW(TAG, "Failed to open VFS stream");
        err_obj->valueint = PKG_ERR_FILE_READ;
        mqtt_file_read_response_helper(rsp_obj, NULL);
        goto file_err;
    }

    lfs2_ssize_t pkg_len = file_size > 2600 ? 2600 : file_size;
    int8_t *buffer = (int8_t *)malloc(pkg_len);
    if (buffer == NULL) {
        ESP_LOGW(TAG, "No memory available for buffer");
        err_obj->valueint = PKG_ERR_NO_MEMORY_AVAILABLE;
        mqtt_file_read_response_helper(rsp_obj, NULL);
        vfs_stream_close(stream);
        goto file_err;
    }

    int total = 0;
    if (file_size % 2600) {
        total = (file_size / 2600) + 1;
    } else {
        total = (file_size / 2600);
    }
    cJSON_SetIntValue(total_obj, (file_size / 2600) + 1);

    int index = 0;
    while (1) {
        if (index == total - 1) {
            pkg_len = file_size % 2600;
        }

        // read file
        size_t read = 0;
        size_t len = 0;
        while (len != pkg_len) {
            len = vfs_stream_read(stream, &buffer[read], pkg_len - read);
            if (len < 0) {
                ESP_LOGW(TAG, "Failed to read file");
                err_obj->valueint = PKG_ERR_FILE_READ;
                vfs_stream_close(stream);
                mqtt_file_read_response_helper(rsp_obj, NULL);
                goto file_err;
            }
            read += len;
        }

        // base64 encode
        size_t encode_len = 0;
        char *ctx_buf = m5_base64_encode(buffer, pkg_len, &encode_len);

        // json load
        cJSON_SetIntValue(index_obj, index);
        cJSON_SetIntValue(len_obj, pkg_len);
        cJSON_SetValuestring(ctx_obj, ctx_buf);
        xSemaphoreTake(xSemaphore, portMAX_DELAY);
        memset(json_buf, 0x00, 4096 + 8);
        if (cJSON_PrintPreallocated(rsp_obj, json_buf, 4096 + 8, false)) {
            esp_mqtt_client_publish(
                m5things_mqtt_client,
                mqtt_up_file_topic,
                json_buf,
                strlen(json_buf),
                0,
                0
                );
        } else {
            ESP_LOGW(TAG, "json object serialization failed");
        }
        xSemaphoreGive(xSemaphore);

        // release resources
        free(ctx_buf);
        vTaskDelay(200 / portTICK_PERIOD_MS);
        index += 1;
        if (index == total) {
            ESP_LOGI(TAG, "File read complete, total: %d bytes, packages: %d", file_size, total);
            break;
        }
    }

    vfs_stream_close(stream);
    free(buffer);
file_err:
    cJSON_Delete(rsp_obj);

out:
    free(msg);
    vTaskDelete(NULL);
    return;
}


static int8_t mqtt_handle_file_read(msg_file_req_t *msg) {
    int8_t ret = PKG_ERR_PARSE;

    msg_file_req_t *arg = (msg_file_req_t *)malloc(sizeof(msg_file_req_t));
    if (arg != NULL && msg != NULL) {
        memcpy(arg, msg, sizeof(msg_file_req_t));
        ret = xTaskCreatePinnedToCore(
            read_task,
            "read_task",
            6000,
            (void *)arg,
            ESP_TASK_PRIO_MAX - 1,
            NULL,
            0
            ) == pdPASS ? PKG_OK : PKG_ERR_FILE_READ;
    }

    return ret;
}


static int mqtt_file_list_response_helper(cJSON *rsp, const char *rsp_buf) {
    int ret = -1;
    if (rsp != NULL) {
        xSemaphoreTake(xSemaphore, portMAX_DELAY);
        memset(json_buf, 0x00, 4096 + 8);
        if (cJSON_PrintPreallocated(rsp, json_buf, 4096 + 8, false)) {
            esp_mqtt_client_publish(
                m5things_mqtt_client,
                mqtt_up_file_topic,
                json_buf,
                strlen(json_buf),
                0,
                0
                );
        } else {
            ESP_LOGW(TAG, "json object serialization failed");
        }
        xSemaphoreGive(xSemaphore);
    } else if (rsp_buf != NULL) {
        ret = esp_mqtt_client_publish(m5things_mqtt_client, mqtt_up_file_topic, rsp_buf, strlen(rsp_buf), 0, 0);
    }
    return ret;
}


static int8_t mqtt_handle_file_list(msg_file_req_t *msg) {
    int8_t ret = PKG_ERR_PARSE;

    cJSON *rsp = cJSON_CreateObject();
    if (rsp == NULL) {
        ESP_LOGW(TAG, "Failed to create rsp json");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char rsp_buf[256] = { 0 };
        sprintf(
            rsp_buf,
            "{\"file_op\":2,\"fs_path\":\"%s\",\"file_list\":[],\"pkg_sn\":%d,\"err_code\":%d}",
            msg->path,
            msg->sn,
            ret
            );
        mqtt_file_list_response_helper(NULL, rsp_buf);
        return ret;
    }

    cJSON *file_list = cJSON_CreateArray();
    if (file_list == NULL) {
        ESP_LOGW(TAG, "Failed to create json array");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char rsp_buf[256] = { 0 };
        sprintf(
            rsp_buf,
            "{\"file_op\":2,\"fs_path\":\"%s\",\"file_list\":[],\"pkg_sn\":%d,\"err_code\":%d}",
            msg->path,
            msg->sn,
            ret
            );
        mqtt_file_list_response_helper(NULL, rsp_buf);
        goto no_memory;
    }

    ret = file_list_helper(msg->path, file_list);
    cJSON_AddNumberToObject(rsp, "file_op", msg->operator);
    cJSON_AddStringToObject(rsp, "fs_path", msg->path);
    cJSON_AddItemToObject(rsp, "file_list", file_list);
    cJSON_AddNumberToObject(rsp, "pkg_sn", msg->sn);
    cJSON_AddNumberToObject(rsp, "err_code", ret);

    xSemaphoreTake(xSemaphore, portMAX_DELAY);
    memset(json_buf, 0x00, 4096 + 8);
    if (cJSON_PrintPreallocated(rsp, json_buf, 4096 + 8, false)) {
        esp_mqtt_client_publish(
            m5things_mqtt_client,
            mqtt_up_file_topic,
            json_buf,
            strlen(json_buf),
            0,
            0
            );
    } else {
        ESP_LOGW(TAG, "json object serialization failed");
    }
    xSemaphoreGive(xSemaphore);

no_memory:
    cJSON_Delete(rsp);
    return ret;
}


static int8_t mqtt_handle_file_list_v2(msg_file_req_t *msg) {
    int8_t ret = PKG_OK;

    cJSON *rsp = cJSON_CreateObject();
    if (rsp == NULL) {
        ESP_LOGW(TAG, "Failed to create rsp json");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char rsp_buf[256] = { 0 };
        sprintf(
            rsp_buf,
            "{\"file_op\":2,\"fs_path\":\"%s\",\"file_list\":[],\"pkg_sn\":%d,\"err_code\":%d}",
            msg->path,
            msg->sn,
            ret
            );
        mqtt_file_list_response_helper(NULL, rsp_buf);
        return ret;
    }

    cJSON *file_list = cJSON_CreateArray();
    if (file_list == NULL) {
        ESP_LOGW(TAG, "Failed to create json array");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char rsp_buf[256] = { 0 };
        sprintf(
            rsp_buf,
            "{\"file_op\":2,\"fs_path\":\"%s\",\"file_list\":[],\"pkg_sn\":%d,\"err_code\":%d}",
            msg->path,
            msg->sn,
            ret
            );
        mqtt_file_list_response_helper(NULL, rsp_buf);
        goto out;
    }

    cJSON_AddNumberToObject(rsp, "file_op", msg->operator);
    cJSON_AddStringToObject(rsp, "fs_path", msg->path);
    cJSON_AddItemToObject(rsp, "file_list", file_list);
    cJSON_AddNumberToObject(rsp, "pkg_sn", msg->sn);
    cJSON_AddNumberToObject(rsp, "err_code", ret);
    ret = file_list_helper_v2(msg->path, file_list);

    // find vfs
    cJSON *json = get_res_record();
    if (json == NULL) {
        ESP_LOGE(TAG, "get res.json failed");
        ret = PKG_ERR_PARSE;
        goto out;
    }

    if (json) {
        cJSON *resFileList = cJSON_GetObjectItemCaseSensitive(json, "fileList");
        if (resFileList) {
            int file_num = cJSON_GetArraySize(resFileList);
            for (int i = 0; i < file_num; i++) {
                cJSON *file = cJSON_GetArrayItem(resFileList, i);
                cJSON *path = cJSON_GetObjectItemCaseSensitive(file, "devicePath");
                cJSON *md5 = cJSON_GetObjectItemCaseSensitive(file, "md5");
                const char *last_slash = strrchr(path->valuestring, '/');
                char base_path[128] = { 0 };
                char filename[128] = { 0 };
                if (last_slash != NULL) {
                    memcpy(filename, last_slash + 1, strlen(last_slash + 1));
                    memcpy(base_path, path->valuestring, strlen(path->valuestring) - strlen(last_slash) + 1);
                } else {
                    continue;
                }
                ESP_LOGW(TAG, "msg path: %s, base_path: %s, filename: %s", msg->path, base_path, filename);
                if (strcmp(base_path, msg->path) != 0) {
                    continue;
                }
                bool exist = false;
                for (int j = 0; j < cJSON_GetArraySize(file_list); j++) {
                    cJSON *file = cJSON_GetArrayItem(file_list, j);
                    cJSON *name = cJSON_GetObjectItemCaseSensitive(file, "name");
                    ESP_LOGW(TAG, "name: %s", name->valuestring);
                    ESP_LOGW(TAG, "md5: %s", md5->valuestring);
                    if (strcmp(name->valuestring, filename) == 0) {
                        cJSON_ReplaceItemInObject(file, "md5", cJSON_Duplicate(md5, true));
                        exist = true;
                    }
                }
                if (exist == false) {
                    cJSON *new_file = cJSON_CreateObject();
                    cJSON_AddStringToObject(new_file, "name", filename);
                    cJSON_AddStringToObject(new_file, "md5", md5->valuestring);
                    cJSON_AddItemToArray(file_list, new_file);
                }
            }
        }
        cJSON_Delete(json);
    }

    xSemaphoreTake(xSemaphore, portMAX_DELAY);
    memset(json_buf, 0x00, 4096 + 8);
    if (cJSON_PrintPreallocated(rsp, json_buf, 4096 + 8, false)) {
        ESP_LOGW(TAG, "json_buf: %s", json_buf);
        esp_mqtt_client_publish(
            m5things_mqtt_client,
            mqtt_up_file_topic,
            json_buf,
            strlen(json_buf),
            0,
            0
            );
    } else {
        ESP_LOGW(TAG, "json object serialization failed");
    }
    xSemaphoreGive(xSemaphore);

out:
    cJSON_Delete(rsp);
    return ret;
}


static int8_t file_remove_helper_v2(const char *path) {
    int8_t ret = PKG_OK;

    // get file record
    cJSON *json = get_res_record();
    if (json == NULL) {
        ESP_LOGE(TAG, "get res.json failed");
        ret = PKG_ERR_PARSE;
        goto out;
    }

    cJSON *old_file_list = cJSON_GetObjectItemCaseSensitive(json, "fileList");
    cJSON *totalSize = cJSON_GetObjectItemCaseSensitive(json, "totalSize");
    int total_size = totalSize->valueint;
    int old_file_num = cJSON_GetArraySize(old_file_list);
    int i = 0;
    for (i = 0; i < old_file_num; i++) {
        cJSON *file = cJSON_GetArrayItem(old_file_list, i);
        cJSON *devicePath = cJSON_GetObjectItemCaseSensitive(file, "devicePath");
        if (strcmp(devicePath->valuestring, path) == 0) {
            total_size -= cJSON_GetObjectItemCaseSensitive(file, "size")->valueint;
            break;
        }
    }
    cJSON_DeleteItemFromArray(old_file_list, i);
    cJSON_SetNumberValue(totalSize, total_size);

    // save res.json
    update_res_record(json);

    cJSON_Delete(json);

out:
    return ret;
}


static int8_t mqtt_handle_file_remove(msg_file_req_t *msg) {
    int8_t ret = PKG_OK;
    ret = file_remove_helper(msg->path);
    ret = file_remove_helper_v2(msg->path);

    char rsp_buf[256] = { 0 };
    sprintf(
        rsp_buf,
        "{\"file_op\":%d,\"fs_path\":\"%s\",\"pkg_sn\":%d,\"err_code\":%d}",
        msg->operator,
        msg->path,
        msg->sn,
        ret
        );

    esp_mqtt_client_publish(
        m5things_mqtt_client,
        mqtt_up_file_topic,
        rsp_buf,
        strlen(rsp_buf),
        0,
        0
        );
    return ret;
}

static int8_t mqtt_file_parse_all(const char *data, size_t len, msg_file_req_t *msg) {
    int8_t ret = PKG_OK;

    if (data == NULL || len == 0) {
        ESP_LOGW(TAG, "Message is null");
        ret = PKG_ERR_PARSE;
        return ret;
    }

    cJSON *root = cJSON_ParseWithLength(data, len);
    if (root == NULL || cJSON_IsNull(root)) {
        ESP_LOGW(TAG, "FILE JSON parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }

    memset(msg, 0x00, sizeof(msg_file_req_t));
    cJSON *file_op = cJSON_GetObjectItemCaseSensitive(root, "file_op");
    if (file_op == NULL || cJSON_IsNull(file_op)) {
        ESP_LOGW(TAG, "'file_op' parsing failed");
        ret = PKG_ERR_PARSE;
        goto error_file_op;
    } else {
        msg->operator = cJSON_GetNumberValue(file_op);
    }

    cJSON *fs_path = cJSON_GetObjectItemCaseSensitive(root, "fs_path");
    if (fs_path == NULL || cJSON_IsNull(fs_path)) {
        ESP_LOGW(TAG, "'fs_path' parsing failed");
        ret = PKG_ERR_PARSE;
        goto error_file_op;
    } else {
        memcpy(msg->path, fs_path->valuestring, strlen(fs_path->valuestring));
    }

    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(root, "pkg_sn");
    if (pkg_sn == NULL || cJSON_IsNull(pkg_sn)) {
        ESP_LOGW(TAG, "'pkg_sn' parsing failed");
        ret = PKG_ERR_PARSE;
    } else {
        msg->sn = cJSON_GetNumberValue(pkg_sn);
    }

    switch (msg->operator)
    {
        case 0: {
            cJSON *pkg_tot = cJSON_GetObjectItemCaseSensitive(root, "pkg_tot");
            if (pkg_tot == NULL || cJSON_IsNull(pkg_tot)) {
                ESP_LOGW(TAG, "'pkg_tot' parsing failed");
                ret = PKG_ERR_PARSE;
            } else {
                msg->total = cJSON_GetNumberValue(pkg_tot);
            }
            cJSON *pkg_idx = cJSON_GetObjectItemCaseSensitive(root, "pkg_idx");
            if (pkg_idx == NULL || cJSON_IsNull(pkg_idx)) {
                ESP_LOGW(TAG, "'pkg_idx' parsing failed");
                ret = PKG_ERR_PARSE;
            } else {
                msg->index = cJSON_GetNumberValue(pkg_idx);
            }
            cJSON *pkg_len = cJSON_GetObjectItemCaseSensitive(root, "pkg_len");
            if (pkg_len == NULL || cJSON_IsNull(pkg_len)) {
                ESP_LOGW(TAG, "'pkg_len' parsing failed");
                ret = PKG_ERR_PARSE;
            } else {
                msg->len = cJSON_GetNumberValue(pkg_len);
            }
            cJSON *pkg_ctx = cJSON_GetObjectItemCaseSensitive(root, "pkg_ctx");
            if (pkg_ctx == NULL || cJSON_IsNull(pkg_ctx)) {
                ESP_LOGW(TAG, "'pkg_ctx' parsing failed");
                ret = PKG_ERR_PARSE;
            } else {
                size_t decode_len = 0;
                msg->ctx_buf = (uint8_t *)m5_base64_decode(pkg_ctx->valuestring, strlen(pkg_ctx->valuestring), &decode_len);
                if (msg->ctx_buf == NULL && strlen(pkg_ctx->valuestring)) {
                    ESP_LOGE(TAG, "No memory(@m5_base64_decode)");
                    ret = PKG_ERR_NO_MEMORY_AVAILABLE;
                    goto error_base64_decode;
                }
                if (msg->len != decode_len) {
                    ESP_LOGE(TAG, "base64 decode failed");
                    ret = PKG_ERR_LENGTH;
                    if (msg->ctx_buf) {
                        free(msg->ctx_buf);
                    }
                    goto error_base64_decode;
                }
            }
        }
        break;

        case 1:
            // pass
            break;

        case 2:
            // pass
            break;

        case 3:
            // pass
            break;

        case 4:
        case 5: {
            cJSON *fileList = cJSON_GetObjectItemCaseSensitive(root, "fileList");
            if (fileList == NULL || cJSON_IsNull(fileList)) {
                ESP_LOGW(TAG, "'fileList' parsing failed");
                ret = PKG_ERR_PARSE;
            } else {
                msg->file_list = cJSON_Duplicate(fileList, true);
            }
            cJSON *time = cJSON_GetObjectItemCaseSensitive(root, "createTime");
            if (time) {
                msg->time = cJSON_GetNumberValue(time);
            }
            cJSON *total_size = cJSON_GetObjectItemCaseSensitive(root, "totalSize");
            if (total_size) {
                msg->total_size = cJSON_GetNumberValue(total_size);
            }
        }
        break;

        case 6:
            // pass
            break;

        default:
            break;
    }

error_base64_decode:
error_file_op:
    cJSON_Delete(root);
end:
    return ret;
}

static int8_t mqtt_file_process(
    esp_mqtt_event_handle_t event,
    uint64_t *_pkg_sn,
    uint8_t *_pkg_idx
    ) {
    int8_t ret = PKG_OK;
    msg_file_req_t msg;

    ret = mqtt_file_parse_all(event->data, event->data_len, &msg);
    if (ret != PKG_OK) {
        return ret;
    }

    ESP_LOGI(TAG, "File Operation: %s(%d)", file_op_dsc[msg.operator], msg.operator);

    switch (msg.operator) {
        case E_M5THING_FILE_OP_WRITE:
            ret = mqtt_handle_file_write(&msg);
            break;

        case E_M5THING_FILE_OP_READ:
            ret = mqtt_handle_file_read(&msg);
            break;

        case E_M5THING_FILE_OP_LIST:
            ret = mqtt_handle_file_list(&msg);
            break;

        case E_M5THING_FILE_OP_REMOVE:
            ret = mqtt_handle_file_remove(&msg);
            break;

        case E_M5THING_FILE_OP_WRITE_V2:
            ret = mqtt_handle_file_write_v2(&msg);
            break;

        case E_M5THING_FILE_OP_MULTI_WRITE:
            ret = mqtt_handle_multi_file_write_v2(&msg);
            break;

        case E_M5THING_FILE_OP_LIST_V2:
            ret = mqtt_handle_file_list_v2(&msg);
            break;

        default:
            ESP_LOGW(TAG, "Unsupported file operation");
            break;
    }

    ESP_LOGI(TAG, "Result: %s(%d)", result_dsc[-ret], ret);
    if (msg.ctx_buf != NULL) {
        free(msg.ctx_buf);
    }
    if (msg.file_list != NULL) {
        cJSON_Delete(msg.file_list);
    }
    return ret;
}

int8_t mqtt_paircode_process(
    esp_mqtt_event_handle_t event,
    uint64_t *_pkg_sn
    ) {
    int8_t ret = PKG_OK;

    cJSON *root = cJSON_ParseWithLength(event->data, event->data_len);
    if (root == NULL || cJSON_IsNull(root)) {
        ESP_LOGW(TAG, "FILE JSON parsing failed");
        ret = PKG_ERR_PARSE;
        return ret;
    }

    cJSON *data = cJSON_GetObjectItemCaseSensitive(root, "data");
    cJSON *code = cJSON_GetObjectItemCaseSensitive(data, "code");
    if (data == NULL || cJSON_IsNull(data) || code == NULL || cJSON_IsNull(code)) {
        ESP_LOGW(TAG, "'data' or 'code' parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }
    ESP_LOGI(TAG, "New Paircode data: %s", code->valuestring);
    ESP_LOGI(TAG, "Old Paircode data: %s", pair_code);

    if (strcmp(code->valuestring, pair_code) != 0) {
        memset(pair_code, 0x00, sizeof(pair_code));
        memcpy(pair_code, code->valuestring, strlen(code->valuestring));
    }

    cJSON *name = cJSON_GetObjectItemCaseSensitive(data, "name");
    if (name != NULL && !cJSON_IsNull(name)) {
        ESP_LOGI(TAG, "New Device Name data: %s", name->valuestring);
        ESP_LOGI(TAG, "Old Device Name data: %s", alias_name);

        if (strcmp(name->valuestring, alias_name) != 0) {
            memset(alias_name, 0x00, sizeof(alias_name));
            memcpy(alias_name, name->valuestring, strlen(name->valuestring));
        }
    }

    ESP_LOGI(TAG, "Result: %s(%d)", result_dsc[-ret], ret);
end:
    cJSON_Delete(root);
    return ret;
}

static void mqtt_message_handle(void *event_data) {
    esp_mqtt_event_handle_t event = event_data;

    event->data[event->data_len] = '\0';
    ESP_LOGI(TAG, "Heap free: %ld bytes", esp_get_free_heap_size());
    ESP_LOGI(TAG, "\r\nTopic: '%.*s'\r\nMessage: '%.*s'\r\nOffset: %d",
        event->topic_len, event->topic, event->data_len, event->data,
        event->current_data_offset);

    // esp_log_buffer_hex("data", event->data, event->data_len);

    uint64_t resp_pkg_sn = 0;
    uint8_t resp_pkg_idx = 0;
    int8_t result = 0;
    if ((strncmp(mqtt_down_ping_topic, event->topic, event->topic_len) == 0)) {
        ESP_LOGI(TAG, "Downlink msg's topic is match down ping topic");
        result = mqtt_ping_down_process(event, &resp_pkg_sn);
        mqtt_response_helper(TOPIC_PING_IDX, resp_pkg_sn, 0, result);
    } else if ((strncmp(mqtt_down_exec_topic, event->topic, event->topic_len) == 0)) {
        ESP_LOGI(TAG, "Downlink msg's topic is match down exec topic");
        result = mqtt_exec_process(event, &resp_pkg_sn, &resp_pkg_idx);
        mqtt_response_helper(TOPIC_EXEC_IDX, resp_pkg_sn, resp_pkg_idx, result);
    } else if ((strncmp(mqtt_down_file_topic, event->topic, event->topic_len) == 0)) {
        ESP_LOGI(TAG, "Downlink msg's topic is match down file topic");
        result = mqtt_file_process(event, &resp_pkg_sn, &resp_pkg_idx);
        // mqtt_response_helper(TOPIC_FILE_IDX, resp_pkg_sn, resp_pkg_idx, result);
    } else if ((strncmp(mqtt_down_paircode_topic, event->topic, event->topic_len) == 0)) {
        ESP_LOGI(TAG, "Downlink msg's topic is match down paircode topic");
        result = mqtt_paircode_process(event, &resp_pkg_sn);
        // mqtt_response_helper(TOPIC_PAIRCODE_IDX, resp_pkg_sn, 0, result);
    } else {
        ESP_LOGW(TAG, "Downlink msg's topic is not match any topic");
    }
}

static char *calculate_password(char *client_id) {
    uint8_t encrypt_key[32] = {
        0x38, 0x39, 0x44, 0x4c, 0x66, 0x30, 0x31, 0x58,
        0x45, 0x46, 0x52, 0x41, 0x4f, 0x6c, 0x76, 0x35,
        0x48, 0x48, 0x52, 0x34, 0x59, 0x66, 0x73, 0x49,
        0x49, 0x4f, 0x31, 0x76, 0x45, 0x43, 0x55, 0x44
    };
    uint8_t iv[16] = {
        0x39, 0x53, 0x48, 0x48, 0x63, 0x5a, 0x49, 0x6a,
        0x79, 0x4b, 0x79, 0x6c, 0x37, 0x61, 0x45, 0x64
    };

    uint8_t encrypted_key[16] = {0};
    uint8_t singn[32] = {0};
    uint8_t hash[32] = {0};
    size_t len;
    time_t now = 0;

    esp_aes_context ctx;
    esp_aes_init(&ctx);
    esp_aes_setkey(&ctx, encrypt_key, 256);
    esp_aes_crypt_cbc(&ctx, ESP_AES_ENCRYPT, 16, iv, (uint8_t *)client_id,
        (uint8_t *)encrypted_key);
    esp_aes_free(&ctx);

    time(&now);
    len = sprintf((char *)singn, "%s-%lld", client_id, (now - (now % 60)));
    m5_hmac_sha256(encrypted_key, 16, singn, len, hash);

    return (char *)m5_base64_encode(hash, 32, &len);
}

static esp_err_t mqtt_app_start(void) {
    uint8_t sta_mac[6] = {0};
    char client_id[17], username[12];
    static char *password = NULL;
    size_t topic_len;

    #if !CONFIG_IDF_TARGET_ESP32P4
    esp_read_mac(sta_mac, ESP_MAC_WIFI_STA);
    #else
    esp_efuse_mac_get_default(sta_mac);
    #endif

    for (size_t i = 0; i < 3; i++) {
        topic_len = sprintf(up_topic_list[i], M5THINGS_OTA_TOPIC_TEMPLATE, "up",
            MAC2STR(sta_mac), topic_action_list[i]);
        up_topic_list[i][topic_len] = '\0';

        topic_len = sprintf(down_topic_list[i], M5THINGS_OTA_TOPIC_TEMPLATE,
            "down", MAC2STR(sta_mac), topic_action_list[i]);
        down_topic_list[i][topic_len] = '\0';
    }
    topic_len = sprintf(up_topic_list[3], "$m5/uiflow/v2/%s/%02x%02x%02x%02x%02x%02x/%s", "up",
        MAC2STR(sta_mac), topic_action_list[3]);
    up_topic_list[3][topic_len] = '\0';

    topic_len = sprintf(down_topic_list[3], "$m5/uiflow/v2/%s/%02x%02x%02x%02x%02x%02x/%s", "down",
        MAC2STR(sta_mac), topic_action_list[3]);
    down_topic_list[3][topic_len] = '\0';

    ESP_LOGI(TAG, "PING:\r\n\t%s\r\n\t%s", mqtt_up_ping_topic,
        mqtt_down_ping_topic);
    ESP_LOGI(TAG, "EXEC:\r\n\t%s\r\n\t%s", mqtt_up_exec_topic,
        mqtt_down_exec_topic);
    ESP_LOGI(TAG, "FILE:\r\n\t%s\r\n\t%s", mqtt_up_file_topic,
        mqtt_down_file_topic);
    ESP_LOGI(TAG, "PAIRCODE:\r\n\t%s\r\n\t%s", mqtt_up_paircode_topic,
        mqtt_down_paircode_topic);

    sprintf(client_id, "m5%02x%02x%02x%02x%02x%02xm5", MAC2STR(sta_mac));
    sprintf(username, "uiflow-%02x%02x", sta_mac[4], sta_mac[5]);
    if (password) {
        free(password);
        password = NULL;
    }
    password = calculate_password(client_id);

    ESP_LOGI(TAG,
        "MQTT Info:\r\n\tclient_id: %s\r\n\tusername: %s\r\n\tpasswd: %s",
        client_id, username, password);

    esp_mqtt_client_config_t mqtt_cfg = {
        .buffer.size = 4096,
        .buffer.out_size = 4096,
        .credentials.client_id = client_id,
        .credentials.username = username,
        .credentials.authentication.password = password,
        .session.keepalive = 30
    };

    ESP_LOGI(TAG, "[APP] Free memory: %ld bytes", esp_get_free_heap_size());

    char server_uri[64];
    char nvs_server_uri[32];
    size_t uri_len = sizeof(nvs_server_uri);
    if (nvs_read_str_helper(UIFLOW_NVS_NAMESPACE, "server", nvs_server_uri, &uri_len)) {
        sprintf(server_uri, "mqtt://%s:1883", nvs_server_uri);
        mqtt_cfg.broker.address.uri = server_uri;
    } else {
        mqtt_cfg.broker.address.uri = "mqtt://uiflow2.m5stack.com:1883";  // default
    }
    ESP_LOGI(TAG, "mqtt_cfg.broker.address.uri: %s", mqtt_cfg.broker.address.uri);

    m5things_mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(m5things_mqtt_client, ESP_EVENT_ANY_ID,
        mqtt_event_handler, NULL);
    return esp_mqtt_client_start(m5things_mqtt_client);
}

void time_sync_notification_cb(struct timeval *tv) {
    ESP_LOGI(TAG, "Notification of a time synchronization event");
}

static bool sync_time_by_sntp(void) {
    time_t now = 0;

    // time(&now);
    // if (now > 1670484240) {  // magic day :)
    //     return true;
    // }

    ESP_LOGI(TAG, "Initializing SNTP");
    // sntp_setoperatingmode(SNTP_OPMODE_POLL);

    char sntp[64];
    size_t len = sizeof(sntp);
    if (nvs_read_str_helper(UIFLOW_NVS_NAMESPACE, "sntp0", sntp, &len) && len > 0 && strlen(sntp) > 0) {
        // sntp_setservername(0, sntp);
        // memcpy(sntp, sntp, strlen(sntp) + 1);
    } else {
        // sntp_setservername(0, "ntp.aliyun.com");  // default
        memcpy(sntp, "ntp.aliyun.com", strlen("ntp.aliyun.com") + 1);
    }

    esp_sntp_config_t config = ESP_NETIF_SNTP_DEFAULT_CONFIG(sntp);
    config.sync_cb = time_sync_notification_cb;
    #ifdef CONFIG_SNTP_TIME_SYNC_METHOD_SMOOTH
    config.smooth_sync = true;
    #endif
    esp_netif_sntp_init(&config);
    // sntp_set_time_sync_notification_cb(time_sync_notification_cb);
    // sntp_init();

    int retry = 0;
    const int retry_count = 30;
    while ((esp_netif_sntp_sync_wait(2000 / portTICK_PERIOD_MS) == ESP_ERR_TIMEOUT) &&
           (++retry < retry_count)) {
        ESP_LOGI(TAG, "Waiting for system time to be set... (%d/%d)", retry,
            retry_count);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }

    char strftime_buf[64];
    struct tm timeinfo;
    time(&now);
    localtime_r(&now, &timeinfo);
    strftime(strftime_buf, sizeof(strftime_buf), "%c", &timeinfo);
    ESP_LOGI(TAG, "date/time is: %s, timestamp: %lld", strftime_buf, now);

    esp_netif_sntp_deinit();

    return retry < retry_count ? true : false;
}

void m5thing_task(void *pvParameter) {

creat_mutex:
    xSemaphore = xSemaphoreCreateMutex();
    if (xSemaphore == NULL) {
        ESP_LOGE(TAG, "xSemaphoreCreateMutex failed!");
        goto creat_mutex;
    }

json_buffer_preallocated:
    #if CONFIG_SPIRAM_SUPPORT
    json_buf = (char *)heap_caps_malloc(4096 + 8, MALLOC_CAP_8BIT);
    #else
    json_buf = (char *)malloc(4096 + 8);
    #endif
    if (json_buf == NULL) {
        ESP_LOGE(TAG, "waiting connect to Wi-Fi");
        goto json_buffer_preallocated;
    }

soft_reset:
    ESP_LOGI(TAG, "waiting connect to Wi-Fi");
    while (!wifi_sta_connected) {
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
    ESP_LOGI(TAG, "Wi-Fi is connected, connect to server");
    vTaskDelay(500 / portTICK_PERIOD_MS);

    if (!sync_time_by_sntp()) {
        m5things_cnct_status = M5THING_STATUS_SNTP_ERR;
        ESP_LOGI(TAG, "synchronize time failed");
        goto soft_reset;
    }

    m5things_cnct_status = M5THING_STATUS_CONNECTING;
    if (mqtt_app_start() != ESP_OK) {
        ESP_LOGI(TAG, "connect to server error");
        goto soft_reset_exit;
    }
    m5things_cnct_status = M5THING_STATUS_CONNECTED;

    ESP_LOGI(TAG,
        "connect to server success, waiting downlink data or command");

    uint64_t last_ping_time = esp_timer_get_time();
    for (;;) {
        vTaskDelay(1000 / portTICK_PERIOD_MS);

        if (m5things_cnct_status != M5THING_STATUS_CONNECTED) {
            ESP_LOGI(TAG, "disconnected from the server for some reason");
            break;
        } else {
            // report device status
            if ((esp_timer_get_time() - last_ping_time) > M5THINGS_MQTT_PING_REPORT_INTERVAL_US) {
                last_ping_time = esp_timer_get_time();
                mqtt_ping_report();
            }
        }

        ESP_LOGD(TAG, "heap:%lu ringbuf free: %d", esp_get_free_heap_size(),
            ringbuf_free(&stdin_ringbuf));
    }

soft_reset_exit:
    ESP_LOGI(TAG, "Destroy mqtt client and reconnect");
    esp_mqtt_client_disconnect(m5things_mqtt_client);
    esp_mqtt_client_destroy(m5things_mqtt_client);
    vTaskDelay(M5THINGS_MQTT_RECONNECT_WAIT_MS / portTICK_PERIOD_MS);
    m5things_cnct_status = M5THING_STATUS_STANDBY;
    goto soft_reset;
}
