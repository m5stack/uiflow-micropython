#ifndef __M5THINGS_H__
#define __M5THINGS_H__

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "mqtt_client.h"

#include "py/stackctrl.h"
#include "py/nlr.h"
#include "py/compile.h"
#include "py/runtime.h"
#include "py/persistentcode.h"
#include "py/repl.h"
#include "py/gc.h"
#include "py/mphal.h"
#include "py/ringbuf.h"
#include "shared/readline/readline.h"
#include "shared/runtime/pyexec.h"
#include "shared/runtime/interrupt_char.h"

#include "modnetwork.h"

#include "extmod/vfs.h"
#include "extmod/vfs_lfs.h"
#include "lib/littlefs/lfs2.h"

#define OTA_UPDATE_FILE_NAME "main_ota_temp.py"  // Fixed name!!!

#define M5THINGS_OTA_TOPIC_TEMPLATE \
    "$m5/uiflow/v1/%s/%02x%02x%02x%02x%02x%02x/%s"

#define FILE_RECORD_PATH "res/res.json"

#define BOOT_OPT_NOTHING  0  // Run main.py(after download code to device set to this)
#define BOOT_OPT_MENU_NET 1  // Show startup menu and network setup
#define BOOT_OPT_NETWORK  2  // Only Network setup

#define TOPIC_PING_IDX 0
#define TOPIC_EXEC_IDX 1
#define TOPIC_FILE_IDX 2

typedef enum {
    PKG_OK = 0,
    PKG_ERR_PARSE = -1,
    PKG_ERR_INDEX = -2,
    PKG_ERR_LENGTH = -3,
    PKG_ERR_EXECUTE = -4,
    PKG_ERR_FILE_OPEN = -5,
    PKG_ERR_FILE_READ = -6,
    PKG_ERR_FILE_WRITE = -7,
    PKG_ERR_FILE_CLOSE = -8,
    PKG_ERR_NO_FILE_OR_DIR = -9,
    PKG_ERR_FILE_REMOVE = -10,
    PKG_ERR_FILE_LIST = -11,
    PKG_ERR_NO_MEMORY_AVAILABLE = -12
}m5things_pkg_err_t;

typedef enum {
    M5THING_STATUS_SNTP_ERR = -2,
    M5THING_STATUS_CNCT_ERR = -1,
    M5THING_STATUS_STANDBY = 0,
    M5THING_STATUS_CONNECTING = 1,
    M5THING_STATUS_CONNECTED = 2,
    M5THING_STATUS_DISCONNECT = 3,
}m5things_status_t;

typedef struct {
    int category;
    char device_key[64];
    char device_token[64];
    char account[32];
    char mac[9];
    char user_name[64];
    char avatar[128];
} m5things_info_t;

typedef struct _mp_obj_vfs_lfs2_t {
    mp_obj_base_t base;
    mp_vfs_blockdev_t blockdev;
    bool enable_mtime;
    vstr_t cur_dir;
    struct lfs2_config config;
    lfs2_t lfs;
} mp_obj_vfs_lfs2_t;

extern ringbuf_t stdin_ringbuf;  // mp_task will take code form this buffer
extern TaskHandle_t m5thing_task_handle;
extern bool wifi_sta_connected;
extern int mp_interrupt_char;

extern esp_mqtt_client_handle_t m5things_mqtt_client;

extern int hmac_sha256(const uint8_t *, size_t, const uint8_t *, size_t data_len, uint8_t *);
extern char *base64_encode(const void *src, size_t len, size_t *out_len);
extern unsigned char *base64_decode(const char *src, size_t len, size_t *out_len);
extern char *base64_url_encode(const void *src, size_t len, size_t *out_len);
extern unsigned char *base64_url_decode(const char *src, size_t len, size_t *out_len);

void m5thing_task(void *pvParameter);

#endif
