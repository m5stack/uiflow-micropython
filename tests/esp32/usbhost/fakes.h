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
EventBits_t xEventGroupClearBits(EventGroupHandle_t group, EventBits_t bits);
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

#define MALLOC_CAP_SPIRAM 1
#define MALLOC_CAP_8BIT 2
#define ESP_ERR_INVALID_ARG 0x102
#define CONFIG_UVC_INTERVAL_ARRAY_SIZE 8

typedef struct uvc_host_stream_s *uvc_host_stream_hdl_t;
enum uvc_host_driver_event { UVC_HOST_DRIVER_EVENT_DEVICE_CONNECTED };
enum uvc_host_stream_format {
    UVC_VS_FORMAT_DEFAULT, UVC_VS_FORMAT_MJPEG, UVC_VS_FORMAT_YUY2,
    UVC_VS_FORMAT_H264, UVC_VS_FORMAT_H265, UVC_VS_FORMAT_NV12,
};
enum uvc_host_dev_event {
    UVC_HOST_TRANSFER_ERROR, UVC_HOST_DEVICE_DISCONNECTED,
    UVC_HOST_FRAME_BUFFER_OVERFLOW, UVC_HOST_FRAME_BUFFER_UNDERFLOW,
};
typedef struct {
    enum uvc_host_driver_event type;
    struct { uint8_t dev_addr, uvc_stream_index; size_t frame_info_num; } device_connected;
} uvc_host_driver_event_data_t;
typedef struct {
    enum uvc_host_dev_event type;
    struct { esp_err_t error; } transfer_error;
    struct { uvc_host_stream_hdl_t stream_hdl; } device_disconnected;
} uvc_host_stream_event_data_t;
typedef struct { unsigned h_res, v_res; float fps; enum uvc_host_stream_format format; } uvc_host_stream_format_t;
typedef struct {
    const uvc_host_stream_format_t vs_format;
    size_t data_buffer_len, data_len;
    uint8_t *data;
} uvc_host_frame_t;
typedef struct {
    size_t driver_task_stack_size;
    unsigned driver_task_priority;
    int xCoreID;
    bool create_background_task;
    void (*event_cb)(const uvc_host_driver_event_data_t *, void *);
    void *user_ctx;
} uvc_host_driver_config_t;
typedef struct {
    void (*event_cb)(const uvc_host_stream_event_data_t *, void *);
    bool (*frame_cb)(const uvc_host_frame_t *, void *);
    void *user_ctx;
    struct { uint8_t dev_addr; uint16_t vid, pid; uint8_t uvc_stream_index; } usb;
    uvc_host_stream_format_t vs_format;
    struct {
        int number_of_frame_buffers;
        size_t frame_size;
        uint32_t frame_heap_caps;
        int number_of_urbs;
        size_t urb_size;
        uint8_t **user_frame_buffers;
    } advanced;
} uvc_host_stream_config_t;
typedef struct {
    enum uvc_host_stream_format format;
    unsigned h_res, v_res;
    uint32_t default_interval;
    uint8_t interval_type;
    uint32_t interval[CONFIG_UVC_INTERVAL_ARRAY_SIZE];
} uvc_host_frame_info_t;
int uvc_host_install(const uvc_host_driver_config_t *);
int uvc_host_uninstall(void);
int uvc_host_stream_open(const uvc_host_stream_config_t *, int, uvc_host_stream_hdl_t *);
int uvc_host_stream_start(uvc_host_stream_hdl_t);
int uvc_host_stream_stop(uvc_host_stream_hdl_t);
int uvc_host_stream_close(uvc_host_stream_hdl_t);
int uvc_host_stream_format_get(uvc_host_stream_hdl_t, uvc_host_stream_format_t *);
int uvc_host_frame_return(uvc_host_stream_hdl_t, uvc_host_frame_t *);
int uvc_host_get_frame_list(uint8_t, uint8_t, uvc_host_frame_info_t (*)[], size_t *);
