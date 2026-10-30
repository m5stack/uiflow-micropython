// Native-test substitutes for FreeRTOS and ESP-IDF. No USB hardware is emulated.
#pragma once
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <pthread.h>

typedef int esp_err_t;
#define ESP_OK 0
#define ESP_FAIL -1
#define ESP_ERR_NO_MEM 0x101
#define ESP_ERR_INVALID_STATE 0x103
#define ESP_ERR_NOT_FOUND 0x105
#define ESP_ERR_TIMEOUT 0x107
#define ESP_ERR_INVALID_SIZE 0x104
#define ESP_INTR_FLAG_LEVEL1 1
#define ESP_LOGE(...) ((void)0)
const char *esp_err_to_name(int err);
typedef uint32_t TickType_t;
typedef uint32_t EventBits_t;
typedef int BaseType_t;
#define pdTRUE 1
#define pdFALSE 0
#define pdPASS 1
#define pdMS_TO_TICKS(ms) (ms)
#define tskNO_AFFINITY -1
typedef pthread_mutex_t portMUX_TYPE;
#define portMUX_INITIALIZER_UNLOCKED PTHREAD_MUTEX_INITIALIZER
#define portENTER_CRITICAL(p) pthread_mutex_lock(p)
#define portEXIT_CRITICAL(p) pthread_mutex_unlock(p)
typedef struct fake_queue *QueueHandle_t;
typedef struct fake_group *EventGroupHandle_t;
QueueHandle_t xQueueCreate(size_t count, size_t size);
int xQueueSend(QueueHandle_t queue, const void *item, TickType_t timeout);
int xQueueReceive(QueueHandle_t queue, void *item, TickType_t timeout);
void vQueueDelete(QueueHandle_t queue);
EventGroupHandle_t xEventGroupCreate(void);
EventBits_t xEventGroupSetBits(EventGroupHandle_t group, EventBits_t bits);
EventBits_t xEventGroupWaitBits(EventGroupHandle_t group, EventBits_t bits, int clear, int all, TickType_t timeout);
void vEventGroupDelete(EventGroupHandle_t group);
int xTaskCreate(void (*fn)(void *), const char *name, int stack, void *arg, int priority, void *handle);
void vTaskDelete(void *task);
void vTaskDelay(TickType_t delay);
TickType_t xTaskGetTickCount(void);

#define USB_HOST_LIB_EVENT_FLAGS_NO_CLIENTS 1
#define USB_HOST_LIB_EVENT_FLAGS_ALL_FREE 2
typedef struct {
    int intr_flags;
    bool root_port_unpowered;
    unsigned peripheral_map;
} usb_host_config_t;
int usb_host_install(const usb_host_config_t *config);
int usb_host_uninstall(void);
int usb_host_lib_set_root_port_power(bool enabled);
int usb_host_lib_handle_events(TickType_t ticks, uint32_t *flags);
int usb_host_lib_unblock(void);
int usb_host_device_free_all(void);

typedef struct fake_hid *hid_host_device_handle_t;
typedef int hid_host_driver_event_t;
typedef int hid_host_interface_event_t;
#define HID_HOST_DRIVER_EVENT_CONNECTED 0
#define HID_HOST_INTERFACE_EVENT_INPUT_REPORT 0
#define HID_HOST_INTERFACE_EVENT_TRANSFER_ERROR 1
#define HID_HOST_INTERFACE_EVENT_DISCONNECTED 2
#define HID_SUBCLASS_BOOT_INTERFACE 1
#define HID_PROTOCOL_KEYBOARD 1
#define HID_PROTOCOL_MOUSE 2
#define HID_REPORT_PROTOCOL_BOOT 0
typedef struct { uint8_t addr, iface_num, sub_class, proto; } hid_host_dev_params_t;
typedef struct { uint16_t VID, PID; } hid_host_dev_info_t;
typedef struct {
    void (*callback)(hid_host_device_handle_t, hid_host_interface_event_t, void *);
    void *callback_arg;
} hid_host_device_config_t;
typedef struct {
    bool create_background_task;
    int task_priority, stack_size, core_id;
    void (*callback)(hid_host_device_handle_t, hid_host_driver_event_t, void *);
} hid_host_driver_config_t;
int hid_host_install(const hid_host_driver_config_t *config);
int hid_host_uninstall(void);
int hid_host_device_get_params(hid_host_device_handle_t dev, hid_host_dev_params_t *params);
int hid_host_device_open(hid_host_device_handle_t dev, const hid_host_device_config_t *config);
int hid_host_device_close(hid_host_device_handle_t dev);
int hid_host_get_device_info(hid_host_device_handle_t dev, hid_host_dev_info_t *info);
int hid_host_device_start(hid_host_device_handle_t dev);
int hid_class_request_set_protocol(hid_host_device_handle_t dev, int protocol);
int hid_class_request_set_idle(hid_host_device_handle_t dev, int duration, int id);
int hid_host_device_get_raw_input_report_data(hid_host_device_handle_t dev, uint8_t *data, size_t capacity, size_t *length);
