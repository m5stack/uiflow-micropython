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


/** macro definitions */
#define TAG "M5Things"

#define DEBUG_printf(fmt, ...) // mp_printf(&mp_plat_print, fmt"\r\n", ##__VA_ARGS__)

/** type definitions */
typedef struct _msg_file_req_t
{
    unsigned char operator;
    const char *path;
    int sn;

    union {
        int total;
        int index;
        int len;
        const char *ctx;
    } data;
} msg_file_req_t;

/** local function prototypes */
static void mqtt_message_handle(void *event_data);

/** exported variables */
TaskHandle_t m5thing_task_handle;
esp_mqtt_client_handle_t m5things_mqtt_client = NULL;

volatile m5things_status_t m5things_cnct_status = M5THING_STATUS_STANDBY;
volatile m5things_info_t m5things_info;

/** local variables */

// order is request.
const char *topic_action_list[] = {"ping", "exec", "file"};
const char *file_operation[] = {"WRITE", "READ", "LIST", "REMOVE"};
const char *resulet_msg[] = {
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

static char *up_topic_list[3] = {
    mqtt_up_ping_topic,
    mqtt_up_exec_topic,
    mqtt_up_file_topic
};
static char *down_topic_list[3] = {
    mqtt_down_ping_topic,
    mqtt_down_exec_topic,
    mqtt_down_file_topic
};

SemaphoreHandle_t xSemaphore = NULL;
char *json_buf = NULL;

/******************************************************************************/
static lfs2_t *_fp = NULL;
static lfs2_file_t _file;
static struct lfs2_file_config _fcfg;

static bool lfs2_open_file(const char *path, int flags) {
    const char *full_path = {'\0'};

    mp_vfs_mount_t *_fm = mp_vfs_lookup_path(path, &full_path);
    if (_fm == MP_VFS_NONE || _fm == MP_VFS_ROOT) {
        // mp_printf(&mp_plat_print, "UiFlOW OTA Failed(OS Error:-99)");
        return false;
    }
    _fp = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(_fm->obj))->lfs;
    memset(&_file, 0x00, sizeof(_file));
    _fcfg.buffer = malloc(_fp->cfg->cache_size * sizeof(uint8_t));
    return (lfs2_file_opencfg(_fp, &_file, full_path, flags, &_fcfg) == LFS2_ERR_OK)
            ? true
            : false;
}

static inline int lfs2_write_file(const void *buffer, lfs2_size_t size) {
    return lfs2_file_write(_fp, &_file, buffer, size);
}

static inline int lfs2_seek_file(lfs2_soff_t off, int whence) {
    return lfs2_file_seek(_fp, &_file, off, whence);
}

static int lfs2_close_file(void) {
    int ret = LFS2_ERR_OK;
    if (_fp) {
        ret = lfs2_file_close(_fp, &_file);
    }
    if (_fcfg.buffer) {
        free(_fcfg.buffer);
    }
    return ret;
}

static void log_error_if_nonzero(const char *message, int error_code) {
    if (error_code != 0) {
        ESP_LOGE(TAG, "Last error %s: 0x%x", message, error_code);
    }
}

static int8_t mqtt_file_write_helper(cJSON *_fs_path, cJSON *_pkg_ctx, uint8_t _pkg_idx, size_t _pkg_len) {
    int8_t ret = PKG_OK;
    size_t decode_len = 0;

    unsigned char *ctx_buf = (unsigned char *)base64_decode(
        _pkg_ctx->valuestring, strlen(_pkg_ctx->valuestring), &decode_len);

    if (ctx_buf == NULL && strlen(_pkg_ctx->valuestring)) {
        ESP_LOGE(TAG, "No memory(@base64_decode)");
        return PKG_ERR_NO_MEMORY_AVAILABLE;
    }

    if (_pkg_len != decode_len) {
        ESP_LOGE(TAG, "base64 decode failed");
        ret = PKG_ERR_LENGTH;
        goto end;
    }

    if (_pkg_idx == 0) {
        // open file, NEW + RW + ZERO File
        if (!lfs2_open_file(_fs_path->valuestring, LFS2_O_CREAT | LFS2_O_RDWR | LFS2_O_TRUNC)) {
            ESP_LOGE(TAG, "File create and open failed");
            ret = PKG_ERR_FILE_OPEN;
            goto close;
        }
    } else {
        // open file, RW + MOVE to END
        if (!lfs2_open_file(_fs_path->valuestring, LFS2_O_RDWR | LFS2_O_APPEND)) {
            ESP_LOGE(TAG, "File open failed");
            ret = PKG_ERR_FILE_OPEN;
            goto close;
        }
    }

    // write file
    size_t write_len = lfs2_write_file(ctx_buf, decode_len);
    if (write_len != decode_len) {
        ESP_LOGW(TAG, "File write error, write_len: %d != decode_len: %d", write_len, decode_len);
        ret = PKG_ERR_FILE_WRITE;
        goto close;
    }
close:
    // close file
    if (lfs2_close_file() != LFS2_ERR_OK) {
        ESP_LOGW(TAG, "file close failed");
        ret = PKG_ERR_FILE_CLOSE;
    }
end:
    free(ctx_buf);
    return ret;
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
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%d", base,
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
                ESP_LOGI(TAG, "Last errno string (%s)", strerror(event->error_handle->esp_transport_sock_errno));
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
    char resp_buf[64];
    sprintf(resp_buf, "{\"pkg_sn\":%lld,\"pkg_idx\":%d,\"err_code\":%d}", _pkg_sn, _pkg_idx, _result);
    return esp_mqtt_client_publish(m5things_mqtt_client, up_topic_list[_topic_idx],
        resp_buf, strlen(resp_buf), 0, 0);
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

    size_t len = sprintf(
        mqtt_report_buf,
        "{\"status\":\"online\",\"system\":{\"free_heap\":%u}, \"version\":\"%s\"}",
        esp_get_free_heap_size(),
        running_app_info.version
        );

    esp_mqtt_client_publish(
        m5things_mqtt_client,
        mqtt_up_ping_topic,
        mqtt_report_buf,
        len,
        0,
        0
        );
}

static int8_t mqtt_ping_down_process(esp_mqtt_event_handle_t event, uint64_t *_pkg_sn) {
    int8_t ret = PKG_OK;
    *_pkg_sn = 0;

    if (event->data == NULL) {
        ESP_LOGW(TAG, "Message is null");
        ret = PKG_ERR_PARSE;
        return ret;
    }

    cJSON *root = cJSON_ParseWithLength(event->data, event->data_len);
    if (NULL == root || cJSON_IsNull(root)) {
        ESP_LOGW(TAG, "PING JSON parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }

    cJSON *category_obj = cJSON_GetObjectItemCaseSensitive(root, "category");
    cJSON *device_key_obj = cJSON_GetObjectItemCaseSensitive(root, "deviceKey");
    cJSON *email_obj = cJSON_GetObjectItemCaseSensitive(root, "email");
    cJSON *mac_obj = cJSON_GetObjectItemCaseSensitive(root, "mac");
    cJSON *user_name_obj = cJSON_GetObjectItemCaseSensitive(root, "userName");
    cJSON *avatar_obj = cJSON_GetObjectItemCaseSensitive(root, "avatar");

    memset((void *)&m5things_info, 0x00, sizeof(m5things_info));

    sscanf(category_obj->valuestring, "%d", &m5things_info.category);

    memcpy(
        (void *)m5things_info.device_key,
        device_key_obj->valuestring,
        strlen(device_key_obj->valuestring)
        );

    memcpy(
        (void *)m5things_info.account,
        email_obj->valuestring,
        strlen(email_obj->valuestring)
        );

    memcpy(
        (void *)m5things_info.mac,
        mac_obj->valuestring,
        strlen(mac_obj->valuestring)
        );

    memcpy(
        (void *)m5things_info.user_name,
        user_name_obj->valuestring,
        strlen(user_name_obj->valuestring)
        );

    memcpy(
        (void *)m5things_info.avatar,
        avatar_obj->valuestring,
        strlen(avatar_obj->valuestring)
        );

    cJSON_Delete(root);
end:
    return ret;
}

static int8_t mqtt_exec_process(esp_mqtt_event_handle_t event, uint64_t *_pkg_sn, uint8_t *_pkg_idx) {
    int8_t ret = PKG_OK;
    size_t decode_len = 0;

    cJSON *root = cJSON_ParseWithLength(event->data, event->data_len);
    if (cJSON_IsNull(root) || NULL == root) {
        ESP_LOGW(TAG, "EXEC JSON parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }

    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(root, "pkg_sn");
    cJSON *pkg_tot = cJSON_GetObjectItemCaseSensitive(root, "pkg_tot");
    cJSON *pkg_idx = cJSON_GetObjectItemCaseSensitive(root, "pkg_idx");
    cJSON *pkg_len = cJSON_GetObjectItemCaseSensitive(root, "pkg_len");
    cJSON *pkg_ctx = cJSON_GetObjectItemCaseSensitive(root, "pkg_ctx");

    if (cJSON_IsNull(root) || NULL == pkg_idx) {
        ESP_LOGW(TAG, "Unable to get 'pkg_idx' object");
        ret = PKG_ERR_INDEX;
        goto error_index;
    }

    *_pkg_sn = pkg_sn->valueint;
    *_pkg_idx = pkg_idx->valueint;

    unsigned char *ctx_buf = (unsigned char *)base64_decode(
        pkg_ctx->valuestring, strlen(pkg_ctx->valuestring), &decode_len);

    if (ctx_buf == NULL && strlen(pkg_ctx->valuestring)) {
        ESP_LOGE(TAG, "No memory(@base64_decode)");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        goto error_index;
    }

    if (pkg_len->valueint != decode_len) {
        ESP_LOGE(TAG, "base64 decode failed");
        ret = PKG_ERR_LENGTH;
        goto error_exec;
    }

    if (pkg_idx->valueint == 0) {
        while (ringbuf_get(&stdin_ringbuf) != -1) {
            ;
        }

        // enter paste mode
        mp_sched_keyboard_interrupt();
        ringbuf_put(&stdin_ringbuf, 0x03);  // CTRL + C
        ringbuf_put(&stdin_ringbuf, 0x05);  // CTRL + E
    }
    // esp_log_buffer_hex("ctx_buf", ctx_buf, decode_len);
    for (size_t idx = 0; idx < decode_len; ++idx) {
        uint8_t c = ctx_buf[idx];
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

    if (pkg_idx->valueint == (pkg_tot->valueint - 1)) {
        ringbuf_put(&stdin_ringbuf, 0x04);  // CTRL + D
    }

error_exec:
    free(ctx_buf);
error_index:
    cJSON_Delete(root);
end:
    return ret;
}


static int8_t file_write_helper(
    const char *path,
    const char *ctx,
    size_t ctx_len,
    size_t pkg_len,
    bool is_new_file
    ) {
    int8_t ret = PKG_OK;
    size_t decode_len = 0;

    uint8_t *ctx_buf = (uint8_t *)base64_decode(ctx, ctx_len, &decode_len);

    if (ctx_buf == NULL && ctx_len > 0) {
        ESP_LOGE(TAG, "No memory(@base64_decode)");
        return PKG_ERR_NO_MEMORY_AVAILABLE;
    }

    if (pkg_len != decode_len) {
        ESP_LOGW(TAG, "Base64 decode failed");
        ret = PKG_ERR_LENGTH;
        goto ERROR;
    }

    int flags = 0;
    if (is_new_file) {
        // NEW + RW + ZERO File
        flags = LFS2_O_CREAT | LFS2_O_RDWR | LFS2_O_TRUNC;
    } else {
        // open file, RW + MOVE to END
        flags = LFS2_O_RDWR | LFS2_O_APPEND;
    }

    // open file
    if (!lfs2_open_file(path, flags)) {
        ESP_LOGW(TAG, "File create and open failed");
        ret = PKG_ERR_FILE_OPEN;
        goto OUT;
    }

    // write file
    size_t write_len = lfs2_write_file(ctx_buf, decode_len);
    if (write_len != decode_len) {
        ESP_LOGW(TAG,
            "File write error, written: %d, total length: %d",
            write_len,
            decode_len
            );
        ret = PKG_ERR_FILE_WRITE;
        goto OUT;
    }

OUT:
    // close file
    if (lfs2_close_file() != LFS2_ERR_OK) {
        ESP_LOGW(TAG, "File close failed");
        ret = PKG_ERR_FILE_CLOSE;
    }

ERROR:
    free(ctx_buf);
    return ret;
}

static int mqtt_handle_file_write_response_helper(
    uint8_t topic_idx,
    uint64_t pkg_sn,
    uint32_t pkg_idx,
    int8_t result
    ) {
    char resp_buf[128];
    sprintf(
        resp_buf,
        "{\"file_op\": %d, \"pkg_sn\":%lld,\"pkg_idx\":%d,\"err_code\":%d}",
        0,
        pkg_sn,
        pkg_idx,
        result
        );
    return esp_mqtt_client_publish(
        m5things_mqtt_client,
        up_topic_list[topic_idx],
        resp_buf,
        strlen(resp_buf),
        0,
        0
        );
}

static int8_t mqtt_handle_file_write(cJSON *root) {
    int8_t ret = PKG_ERR_PARSE;
    static int last_idx = 0;

    // cJSON *file_op = cJSON_GetObjectItemCaseSensitive(root, "file_op");
    cJSON *fs_path = cJSON_GetObjectItemCaseSensitive(root, "fs_path");
    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(root, "pkg_sn");
    cJSON *pkg_tot = cJSON_GetObjectItemCaseSensitive(root, "pkg_tot");
    cJSON *pkg_idx = cJSON_GetObjectItemCaseSensitive(root, "pkg_idx");
    cJSON *pkg_len = cJSON_GetObjectItemCaseSensitive(root, "pkg_len");
    cJSON *pkg_ctx = cJSON_GetObjectItemCaseSensitive(root, "pkg_ctx");

    if (pkg_idx->valueint == 0) {
        last_idx = 0;
    } else if (pkg_idx->valueint != last_idx + 1) {
        // Packet data is not continuous
        ESP_LOGW(TAG, "Packet data is not continuous");
        ret = PKG_ERR_INDEX;
        goto ERROR;
    }

    ret = file_write_helper(
        fs_path->valuestring,
        pkg_ctx->valuestring,
        strlen(pkg_ctx->valuestring),
        pkg_len->valueint,
        pkg_idx->valueint == 0
        );
    mqtt_handle_file_write_response_helper(
        TOPIC_FILE_IDX,
        pkg_sn->valueint,
        pkg_idx->valueint,
        ret
        );
    vTaskDelay(500 / portTICK_PERIOD_MS);
    last_idx = pkg_idx->valueint;

    // when OTA done need restart device
    if (pkg_idx->valueint == (pkg_tot->valueint - 1)) {
        // path: /flash/main_ota_temp.py
        if ((strstr(fs_path->valuestring, OTA_UPDATE_FILE_NAME) != NULL)) {
            nvs_write_u8_helper(UIFLOW_NVS_NAMESPACE, "boot_option", BOOT_OPT_NETWORK);
            ESP_LOGW(TAG, "restart now :)");
            esp_restart();
        }
    }

ERROR:
    return ret;
}


static int mqtt_file_read_response_helper(cJSON *resp, const char *resp_buf) {
    int ret = -1;
    if (resp != NULL) {
        xSemaphoreTake(xSemaphore, portMAX_DELAY);
        memset(json_buf, 0x00, 4096 + 8);
        if (cJSON_PrintPreallocated(resp, json_buf, 4096 + 8, false)) {
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
    } else if (resp_buf != NULL) {
        ret = esp_mqtt_client_publish(
            m5things_mqtt_client,
            mqtt_up_file_topic,
            resp_buf,
            strlen(resp_buf),
            0,
            0
            );
    }
    return ret;
}

void read_task(void *pvParameter) {
    cJSON *req = (cJSON *)pvParameter;

    if (req == NULL) {
        ESP_LOGW(TAG, "Req json object does not exist");
        vTaskDelete(NULL);
        return;
    }

    // parse
    cJSON *file_op = cJSON_GetObjectItemCaseSensitive(req, "file_op");
    cJSON *fs_path = cJSON_GetObjectItemCaseSensitive(req, "fs_path");
    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(req, "pkg_sn");
    if (file_op == NULL || fs_path == NULL || pkg_sn == NULL) {
        cJSON_Delete(req);
        vTaskDelete(NULL);
        return;
    }

    // resp json
    cJSON *resp = cJSON_CreateObject();
    if (resp == NULL) {
        ESP_LOGW(TAG, "Failed to create resp json object");
        char resp_buf[256] = {0};
        sprintf(
            resp_buf,
            "{\"file_op\":1,\"%s\",\"pkg_sn\":%d,\"pkg_tot\":1,\"pkg_idx\":0,\"pkg_len\":0,\"pkg_ctx\":\"\",\"err_code\":-1}",
            fs_path->valuestring,
            pkg_sn->valueint
            );
        mqtt_file_read_response_helper(NULL, resp_buf);
        goto OUT_OF_RESP_OBJ;
    }

    cJSON_AddNumberToObject(resp, "file_op", 1);
    cJSON_AddStringToObject(resp, "fs_path", fs_path->valuestring);
    cJSON_AddNumberToObject(resp, "pkg_sn", pkg_sn->valueint);
    cJSON *total_obj = cJSON_AddNumberToObject(resp, "pkg_tot", 1);
    cJSON *index_obj = cJSON_AddNumberToObject(resp, "pkg_idx", 0);
    cJSON *len_obj = cJSON_AddNumberToObject(resp, "pkg_len", 0);
    cJSON *ctx_obj = cJSON_AddStringToObject(resp, "pkg_ctx", "");
    cJSON *err_obj = cJSON_AddNumberToObject(resp, "err_code", 0);

    // find vfs
    const char *path = fs_path->valuestring;
    const char *full_path = {'\0'};
    mp_vfs_mount_t *vfs = mp_vfs_lookup_path(path, &full_path);
    if (vfs == MP_VFS_NONE || vfs == MP_VFS_ROOT) {
        ESP_LOGW(TAG, "Unable to find mounted filesystem");
        err_obj->valueint = PKG_ERR_NO_FILE_OR_DIR;
        mqtt_file_read_response_helper(resp, NULL);
        goto OUT_OF_FS;
    }
    lfs2_t *lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(vfs->obj))->lfs;

    // get file stat
    struct lfs2_info info;
    if (lfs2_stat(lfs2, full_path, &info) != LFS2_ERR_OK) {
        ESP_LOGW(TAG, "No such file or directory");
        err_obj->valueint = PKG_ERR_NO_FILE_OR_DIR;
        mqtt_file_read_response_helper(resp, NULL);
        goto OUT_OF_FS;
    }
    if (info.type == LFS2_TYPE_DIR) {
        ESP_LOGW(TAG, "Directory read request not accepted");
        err_obj->valueint = PKG_ERR_FILE_READ;
        mqtt_file_read_response_helper(resp, NULL);
        goto OUT_OF_FS;
    }

    lfs2_ssize_t pkg_len = info.size > 2600 ? 2600 : info.size;
    int8_t *buffer = (int8_t *)malloc(pkg_len);

    // open file
    lfs2_file_t fp;
    int flags = LFS2_O_RDONLY;
    struct lfs2_file_config config;
    config.buffer = malloc(lfs2->cfg->cache_size * sizeof(uint8_t));
    if (lfs2_file_opencfg(lfs2, &fp, path, flags, &config) != LFS2_ERR_OK) {
        ESP_LOGW(TAG, "Fail to open the file");
        err_obj->valueint = PKG_ERR_FILE_READ;
        mqtt_file_read_response_helper(resp, NULL);
        goto OUT;
    }

    int total = 0;
    if (info.size % 2600) {
        total = (info.size / 2600) + 1;
    } else {
        total = (info.size / 2600);
    }
    cJSON_SetIntValue(total_obj, (info.size / 2600) + 1);

    int index = 0;
    while (1) {
        if (index == total - 1) {
            pkg_len = info.size % 2600;
        }

        // read file
        lfs2_ssize_t len = 0;
        while (len != pkg_len) {
            len = lfs2_file_read(lfs2, &fp, &buffer[len], pkg_len - len);
            if (len < 0) {
                ESP_LOGW(TAG, "Failed to read file");
                err_obj->valueint = PKG_ERR_FILE_READ;
                lfs2_file_close(lfs2, &fp);
                mqtt_file_read_response_helper(resp, NULL);
                goto OUT;
            }
        }

        // base64 encode
        size_t encode_len = 0;
        char *ctx_buf = base64_encode(buffer, pkg_len, &encode_len);

        // json load
        cJSON_SetIntValue(index_obj, index);
        cJSON_SetIntValue(len_obj, pkg_len);
        cJSON_SetValuestring(ctx_obj, ctx_buf);
        xSemaphoreTake(xSemaphore, portMAX_DELAY);
        memset(json_buf, 0x00, 4096 + 8);
        if (cJSON_PrintPreallocated(resp, json_buf, 4096 + 8, false)) {
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
            ESP_LOGI(TAG, "File read complete, total: %d bytes, packages: %d", info.size, total);
            break;
        }
    }

    lfs2_file_close(lfs2, &fp);
OUT:
    free(config.buffer);
    free(buffer);

OUT_OF_FS:
    cJSON_Delete(resp);

OUT_OF_RESP_OBJ:
    cJSON_Delete(req);
    vTaskDelete(NULL);
    return;
}

static int8_t mqtt_handle_file_read(cJSON *root) {
    int8_t ret = PKG_ERR_PARSE;

    cJSON *req = cJSON_Duplicate(root, true);
    if (req != NULL) {
        ret = xTaskCreatePinnedToCore(
            read_task,
            "read_task",
            6000,
            (void *)req,
            ESP_TASK_PRIO_MAX - 1,
            NULL,
            0
            ) == pdPASS ? PKG_OK : PKG_ERR_FILE_READ;
    }

    return ret;
}


static int mqtt_file_list_response_helper(cJSON *resp, const char *resp_buf) {
    int ret = -1;
    if (resp != NULL) {
        xSemaphoreTake(xSemaphore, portMAX_DELAY);
        memset(json_buf, 0x00, 4096 + 8);
        if (cJSON_PrintPreallocated(resp, json_buf, 4096 + 8, false)) {
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
    } else if (resp_buf != NULL) {
        ret = esp_mqtt_client_publish(m5things_mqtt_client, mqtt_up_file_topic, resp_buf, strlen(resp_buf), 0, 0);
    }
    return ret;
}


static int8_t mqtt_handle_file_list(cJSON *root) {
    int8_t ret = PKG_ERR_PARSE;

    cJSON *file_op = cJSON_GetObjectItemCaseSensitive(root, "file_op");
    cJSON *fs_path = cJSON_GetObjectItemCaseSensitive(root, "fs_path");
    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(root, "pkg_sn");
    // cJSON *pkg_tot = cJSON_GetObjectItemCaseSensitive(root, "pkg_tot");
    // cJSON *pkg_idx = cJSON_GetObjectItemCaseSensitive(root, "pkg_idx");
    // cJSON *pkg_len = cJSON_GetObjectItemCaseSensitive(root, "pkg_len");
    // cJSON *pkg_ctx = cJSON_GetObjectItemCaseSensitive(root, "pkg_ctx");

    if (file_op == NULL || fs_path == NULL || pkg_sn == NULL) {
        ESP_LOGW(TAG, "JSON is incomplete or missing");
        return ret;
    }

    cJSON *resp_root = cJSON_CreateObject();
    if (resp_root == NULL) {
        ESP_LOGW(TAG, "Failed to create resp json");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char resp_buf[256] = { 0 };
        sprintf(
            resp_buf,
            "{\"file_op\":2,\"fs_path\":\"%s\",\"file_list\":[],\"pkg_sn\":%d,\"err_code\":%d}",
            fs_path->valuestring,
            pkg_sn->valueint,
            ret
            );
        mqtt_file_list_response_helper(NULL, resp_buf);
        return ret;
    }
    cJSON *file_list = cJSON_CreateArray();
    if (file_list == NULL) {
        ESP_LOGW(TAG, "Failed to create json array");
        ret = PKG_ERR_NO_MEMORY_AVAILABLE;
        char resp_buf[256] = { 0 };
        sprintf(
            resp_buf,
            "{\"file_op\":2,\"fs_path\":\"%s\",\"file_list\":[],\"pkg_sn\":%d,\"err_code\":%d}",
            fs_path->valuestring,
            pkg_sn->valueint,
            ret
            );
        mqtt_file_list_response_helper(NULL, resp_buf);
        goto OUT_ROOT_OBJECT;
    }

    ret = file_list_helper(fs_path->valuestring, file_list);
    cJSON_AddNumberToObject(resp_root, "file_op", file_op->valueint);
    cJSON_AddStringToObject(resp_root, "fs_path", fs_path->valuestring);
    cJSON_AddItemToObject(resp_root, "file_list", file_list);
    cJSON_AddNumberToObject(resp_root, "pkg_sn", pkg_sn->valueint);
    cJSON_AddNumberToObject(resp_root, "err_code", ret);

    xSemaphoreTake(xSemaphore, portMAX_DELAY);
    memset(json_buf, 0x00, 4096 + 8);
    if (cJSON_PrintPreallocated(resp_root, json_buf, 4096 + 8, false)) {
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

OUT_ROOT_OBJECT:
    cJSON_Delete(resp_root);
    return ret;
}

static int8_t mqtt_handle_file_remove(cJSON *root) {
    int8_t ret = PKG_ERR_PARSE;

    cJSON *file_op = cJSON_GetObjectItemCaseSensitive(root, "file_op");
    cJSON *fs_path = cJSON_GetObjectItemCaseSensitive(root, "fs_path");
    cJSON *pkg_sn = cJSON_GetObjectItemCaseSensitive(root, "pkg_sn");
    // cJSON *pkg_tot = cJSON_GetObjectItemCaseSensitive(root, "pkg_tot");
    // cJSON *pkg_idx = cJSON_GetObjectItemCaseSensitive(root, "pkg_idx");
    // cJSON *pkg_len = cJSON_GetObjectItemCaseSensitive(root, "pkg_len");
    // cJSON *pkg_ctx = cJSON_GetObjectItemCaseSensitive(root, "pkg_ctx");

    if (file_op == NULL || fs_path == NULL || pkg_sn == NULL) {
        // There is no need to consider destroying the json object here.
        return ret;
    }

    cJSON *resp_root = cJSON_CreateObject();
    if (resp_root == NULL) {
        return ret;
    }

    ret = file_remove_helper(fs_path->valuestring);
    cJSON_AddNumberToObject(resp_root, "file_op", file_op->valueint);
    cJSON_AddStringToObject(resp_root, "fs_path", fs_path->valuestring);
    cJSON_AddNumberToObject(resp_root, "pkg_sn", pkg_sn->valueint);
    cJSON_AddNumberToObject(resp_root, "err_code", ret);

    xSemaphoreTake(xSemaphore, portMAX_DELAY);
    memset(json_buf, 0x00, 4096 + 8);
    if (cJSON_PrintPreallocated(resp_root, json_buf, 4096 + 8, false)) {
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

    cJSON_Delete(resp_root);
    return ret;
}

static int8_t mqtt_file_process(
    esp_mqtt_event_handle_t event,
    uint64_t *_pkg_sn,
    uint8_t *_pkg_idx
    ) {
    int8_t ret = PKG_OK;

    cJSON *root = cJSON_ParseWithLength(event->data, event->data_len);
    if (cJSON_IsNull(root) || NULL == root) {
        ESP_LOGW(TAG, "FILE JSON parsing failed");
        ret = PKG_ERR_PARSE;
        goto end;
    }

    cJSON *file_op = cJSON_GetObjectItemCaseSensitive(root, "file_op");
    if (cJSON_IsNull(file_op) || file_op == NULL) {
        ESP_LOGW(TAG, "Unable to get 'file_op' object");
        ret = PKG_ERR_PARSE;
        goto error_file_op;
    }

    ESP_LOGI(TAG,
        "File Operation: %s(%d)",
        file_operation[file_op->valueint],
        file_op->valueint
        );

    switch (file_op->valueint) {
        case 0:
            ret = mqtt_handle_file_write(root);
            break;

        case 1:
            ret = mqtt_handle_file_read(root);
            break;

        case 2:
            ret = mqtt_handle_file_list(root);
            break;

        case 3:
            ret = mqtt_handle_file_remove(root);
            break;

        default:
            ESP_LOGW(TAG, "Unsupported file operation");
            break;
    }

    ESP_LOGI(TAG, "Result: %s(%d)", resulet_msg[-ret], ret);

error_file_op:
    cJSON_Delete(root);
end:
    return ret;
}

static void mqtt_message_handle(void *event_data) {
    esp_mqtt_event_handle_t event = event_data;

    event->data[event->data_len] = '\0';
    ESP_LOGI(TAG, "Heap free: %d bytes", esp_get_free_heap_size());
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
    len = sprintf((char *)singn, "%s-%ld", client_id, (now - (now % 60)));
    hmac_sha256(encrypted_key, 16, singn, len, hash);

    return (char *)base64_encode(hash, 32, &len);
}

static esp_err_t mqtt_app_start(void) {
    uint8_t sta_mac[6] = {0};
    char client_id[17], username[12];
    char *password = NULL;
    size_t topic_len;

    esp_efuse_mac_get_default(sta_mac);

    for (size_t i = 0; i < 3; i++) {
        topic_len = sprintf(up_topic_list[i], M5THINGS_OTA_TOPIC_TEMPLATE, "up",
            MAC2STR(sta_mac), topic_action_list[i]);
        up_topic_list[i][topic_len] = '\0';

        topic_len = sprintf(down_topic_list[i], M5THINGS_OTA_TOPIC_TEMPLATE,
            "down", MAC2STR(sta_mac), topic_action_list[i]);
        down_topic_list[i][topic_len] = '\0';
    }

    ESP_LOGI(TAG, "PING:\r\n\t%s\r\n\t%s", mqtt_up_ping_topic,
        mqtt_down_ping_topic);
    ESP_LOGI(TAG, "EXEC:\r\n\t%s\r\n\t%s", mqtt_up_exec_topic,
        mqtt_down_exec_topic);
    ESP_LOGI(TAG, "FILE:\r\n\t%s\r\n\t%s", mqtt_up_file_topic,
        mqtt_down_file_topic);

    sprintf(client_id, "m5%02x%02x%02x%02x%02x%02xm5", MAC2STR(sta_mac));
    sprintf(username, "uiflow-%02x%02x", sta_mac[4], sta_mac[5]);
    password = calculate_password(client_id);

    // ESP_LOGI(TAG,
    //          "MQTT Info:\r\n\tclient_id: %s\r\n\tusername: %s\r\n\tpasswd: %s",
    //          client_id, username, password);

    esp_mqtt_client_config_t mqtt_cfg = {
        .buffer_size = 4096,
        .out_buffer_size = 4096,
        .client_id = client_id,
        .username = username,
        .password = password,
        .keepalive = 30
    };

    ESP_LOGI(TAG, "[APP] Free memory: %d bytes", esp_get_free_heap_size());

    char server_uri[64];
    char nvs_server_uri[32];
    size_t uri_len = sizeof(nvs_server_uri);
    if (nvs_read_str_helper(UIFLOW_NVS_NAMESPACE, "server", nvs_server_uri, &uri_len)) {
        sprintf(server_uri, "mqtt://%s:1883", nvs_server_uri);
        mqtt_cfg.uri = server_uri;
    } else {
        mqtt_cfg.uri = "mqtt://uiflow2.m5stack.com:1883";  // default
    }
    ESP_LOGI(TAG, "mqtt_cfg.uri: %s", mqtt_cfg.uri);

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

    time(&now);
    if (now > 1670484240) {  // magic day :)
        return true;
    }

    ESP_LOGI(TAG, "Initializing SNTP");
    sntp_setoperatingmode(SNTP_OPMODE_POLL);

    char sntp[64];
    size_t len = sizeof(sntp);
    if (nvs_read_str_helper(UIFLOW_NVS_NAMESPACE, "sntp0", sntp, &len) && len > 0 && strlen(sntp) > 0) {
        sntp_setservername(0, sntp);
    } else {
        sntp_setservername(0, "uiflow2.m5stack.com");  // default
    }

    sntp_set_time_sync_notification_cb(time_sync_notification_cb);
    sntp_init();

    int retry = 0;
    const int retry_count = 30;
    while ((sntp_get_sync_status() == SNTP_SYNC_STATUS_RESET) &&
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
    ESP_LOGI(TAG, "date/time is: %s, timestamp: %ld", strftime_buf, now);

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
            if ((esp_timer_get_time() - last_ping_time) > 30000000 /* microseconds */) {
                last_ping_time = esp_timer_get_time();
                mqtt_ping_report();
            }
        }

        ESP_LOGD(TAG, "heap:%u ringbuf free: %d", esp_get_free_heap_size(),
            ringbuf_free(&stdin_ringbuf));
    }

soft_reset_exit:
    ESP_LOGI(TAG, "Destroy mqtt client and reconnect");
    esp_mqtt_client_disconnect(m5things_mqtt_client);
    esp_mqtt_client_destroy(m5things_mqtt_client);
    vTaskDelay(15000 / portTICK_PERIOD_MS);
    goto soft_reset;
}
