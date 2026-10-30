// Exercise the production backend with POSIX task/queue substitutes and fault injection.
// These tests do not validate ESP-IDF, USB enumeration, PHYs, VBUS, or actual peripherals.
#define _POSIX_C_SOURCE 200809L
#include <stdatomic.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "fakes.h"
#include "usbhost.h"
#include "hid_report.h"

struct fake_queue { pthread_mutex_t lock; size_t capacity, size, head, count; uint8_t *data; };
struct fake_group { pthread_mutex_t lock; pthread_cond_t cond; unsigned bits; };
struct fake_hid {
    bool alive, opened, waiting;
    hid_host_dev_params_t params;
    hid_host_device_config_t config;
    uint8_t data[8];
    size_t length;
};
static struct fake_hid fake_devices[32];
static atomic_bool host_ok, hid_ok;
static bool rail;
static int resources, allocation_calls, fail_allocation;
static bool fail_library, fail_hid, fail_task, fail_enable, fail_disable, fail_protocol, fail_close, unplug_on_open;
static pthread_t daemon_thread;
static bool thread_created;
static void (*task_entry)(void *);

static void *allocate(size_t size) {
    if (++allocation_calls == fail_allocation) { return NULL; }
    void *p = calloc(1, size);
    assert(p);
    ++resources;
    return p;
}
QueueHandle_t xQueueCreate(size_t count, size_t size) {
    struct fake_queue *q = allocate(sizeof(*q));
    if (!q) { return NULL; }
    pthread_mutex_init(&q->lock, NULL);
    q->capacity = count;
    q->size = size;
    q->data = calloc(count, size);
    assert(q->data);
    return q;
}
int xQueueSend(QueueHandle_t q, const void *item, TickType_t timeout) {
    pthread_mutex_lock(&q->lock);
    bool ok = q->count < q->capacity;
    if (ok) { memcpy(q->data + ((q->head + q->count++) % q->capacity) * q->size, item, q->size); }
    pthread_mutex_unlock(&q->lock);
    return ok;
}
int xQueueReceive(QueueHandle_t q, void *item, TickType_t timeout) {
    pthread_mutex_lock(&q->lock);
    bool ok = q->count != 0;
    if (ok) {
        memcpy(item, q->data + q->head * q->size, q->size);
        q->head = (q->head + 1) % q->capacity;
        --q->count;
    }
    pthread_mutex_unlock(&q->lock);
    return ok;
}
void vQueueDelete(QueueHandle_t q) { pthread_mutex_destroy(&q->lock); free(q->data); free(q); --resources; }
EventGroupHandle_t xEventGroupCreate(void) {
    struct fake_group *g = allocate(sizeof(*g));
    if (g) { pthread_mutex_init(&g->lock, NULL); pthread_cond_init(&g->cond, NULL); }
    return g;
}
EventBits_t xEventGroupSetBits(EventGroupHandle_t g, EventBits_t bits) {
    pthread_mutex_lock(&g->lock);
    g->bits |= bits;
    unsigned result = g->bits;
    pthread_cond_broadcast(&g->cond);
    pthread_mutex_unlock(&g->lock);
    return result;
}
EventBits_t xEventGroupWaitBits(EventGroupHandle_t g, EventBits_t bits, int clear, int all, TickType_t timeout) {
    struct timespec deadline;
    clock_gettime(CLOCK_REALTIME, &deadline);
    deadline.tv_sec += timeout / 1000;
    deadline.tv_nsec += (timeout % 1000) * 1000000L;
    if (deadline.tv_nsec >= 1000000000L) { ++deadline.tv_sec; deadline.tv_nsec -= 1000000000L; }
    pthread_mutex_lock(&g->lock);
    while ((g->bits & bits) != bits) {
        if (pthread_cond_timedwait(&g->cond, &g->lock, &deadline) != 0) { break; }
    }
    unsigned result = g->bits;
    if (clear) { g->bits &= ~bits; }
    pthread_mutex_unlock(&g->lock);
    return result;
}
void vEventGroupDelete(EventGroupHandle_t g) {
    if (thread_created) { pthread_join(daemon_thread, NULL); thread_created = false; }
    pthread_mutex_destroy(&g->lock); pthread_cond_destroy(&g->cond); free(g); --resources;
}
static void *start_task(void *arg) { task_entry(arg); return NULL; }
int xTaskCreate(void (*fn)(void *), const char *name, int stack, void *arg, int priority, void *handle) {
    if (fail_task) { return 0; }
    assert(!thread_created);
    task_entry = fn;
    assert(pthread_create(&daemon_thread, NULL, start_task, arg) == 0);
    thread_created = true;
    return pdPASS;
}
void vTaskDelete(void *task) { pthread_exit(NULL); }
void vTaskDelay(TickType_t ms) { struct timespec delay = {ms / 1000, (ms % 1000) * 1000000L}; nanosleep(&delay, NULL); }
TickType_t xTaskGetTickCount(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1000u + t.tv_nsec / 1000000; }
const char *esp_err_to_name(int err) { return "injected"; }

int usb_host_install(const usb_host_config_t *config) {
    assert(config->peripheral_map == 1 && config->root_port_unpowered);
    if (fail_library) { return ESP_FAIL; }
    atomic_store(&host_ok, true); return ESP_OK;
}
int usb_host_uninstall(void) { assert(!atomic_load(&hid_ok)); atomic_store(&host_ok, false); return ESP_OK; }
int usb_host_lib_set_root_port_power(bool enabled) {
    assert(atomic_load(&host_ok));
    if (!enabled) {
        for (size_t i = 0; i < 32; ++i) {
            struct fake_hid *d = &fake_devices[i];
            d->alive = false;
            if (d->opened) {
                d->waiting = true;
                d->config.callback(d, HID_HOST_INTERFACE_EVENT_DISCONNECTED, d->config.callback_arg);
                assert(!d->opened);
            }
        }
    }
    return ESP_OK;
}
int usb_host_lib_handle_events(TickType_t ticks, uint32_t *flags) {
    vTaskDelay(1);
    *flags = atomic_load(&hid_ok) ? 0 : USB_HOST_LIB_EVENT_FLAGS_NO_CLIENTS;
    return ESP_OK;
}
int usb_host_lib_unblock(void) { return ESP_OK; }
int usb_host_device_free_all(void) { return atomic_load(&hid_ok) ? ESP_ERR_INVALID_STATE : ESP_OK; }
bool uiflow_usbhost_set_power(bool enabled) {
    if ((enabled && fail_enable) || (!enabled && fail_disable)) { return false; }
    rail = enabled;
    return true;
}
int hid_host_install(const hid_host_driver_config_t *config) {
    assert(config->create_background_task);
    if (fail_hid) { return ESP_FAIL; }
    atomic_store(&hid_ok, true); return ESP_OK;
}
int hid_host_uninstall(void) {
    for (size_t i = 0; i < 32; ++i) {
        if (fake_devices[i].alive || fake_devices[i].opened) { return ESP_ERR_INVALID_STATE; }
    }
    atomic_store(&hid_ok, false); return ESP_OK;
}
int hid_host_device_get_params(hid_host_device_handle_t d, hid_host_dev_params_t *p) {
    if (!d->alive) { return ESP_ERR_NOT_FOUND; } *p = d->params; return ESP_OK;
}
int hid_host_device_open(hid_host_device_handle_t d, const hid_host_device_config_t *config) {
    if (unplug_on_open) { d->alive = false; }
    if (!d->alive) { return ESP_ERR_NOT_FOUND; }
    d->config = *config; d->opened = true; return ESP_OK;
}
int hid_host_device_close(hid_host_device_handle_t d) {
    if (fail_close) { return ESP_ERR_TIMEOUT; }
    if (d->opened && !d->waiting) {
        d->waiting = true;
        d->config.callback(d, HID_HOST_INTERFACE_EVENT_DISCONNECTED, d->config.callback_arg);
    } else { d->opened = false; }
    return ESP_OK;
}
int hid_host_get_device_info(hid_host_device_handle_t d, hid_host_dev_info_t *info) { info->VID = 0x1234; info->PID = 0x5678; return ESP_OK; }
int hid_host_device_start(hid_host_device_handle_t d) { return d->alive ? ESP_OK : ESP_ERR_NOT_FOUND; }
int hid_class_request_set_protocol(hid_host_device_handle_t d, int protocol) { assert(protocol == 0); return fail_protocol ? ESP_FAIL : ESP_OK; }
int hid_class_request_set_idle(hid_host_device_handle_t d, int duration, int id) { return ESP_OK; }
int hid_host_device_get_raw_input_report_data(hid_host_device_handle_t d, uint8_t *data, size_t capacity, size_t *length) {
    *length = d->length < capacity ? d->length : capacity; memcpy(data, d->data, *length); return ESP_OK;
}

// Include the unmodified production backend so tests can inject its native callbacks.
#include "usbhost_backend.c"

static struct fake_hid *connect_device(size_t index, uint8_t protocol, uint8_t subclass) {
    struct fake_hid *d = &fake_devices[index];
    memset(d, 0, sizeof(*d));
    d->alive = true;
    d->params = (hid_host_dev_params_t){1, index, subclass, protocol};
    driver_callback(d, HID_HOST_DRIVER_EVENT_CONNECTED, NULL);
    return d;
}
static void assert_clean(void) {
    assert(resources == 0 && !thread_created && !rail);
    assert(!atomic_load(&host_ok) && !atomic_load(&hid_ok));
    assert(uiflow_usbhost_stop() == ESP_OK);
}

int main(void) {
    uiflow_hid_report_t decoded;
    uint8_t keyboard[8] = {0x22, 0, 4, 5, 0, 0, 0, 0};
    for (size_t n = 0; n < 8; ++n) { assert(!uiflow_hid_decode(1, keyboard, n, &decoded)); }
    assert(uiflow_hid_decode(1, keyboard, 8, &decoded));
    assert(decoded.modifiers == 0x22 && decoded.keys[0] == 4 && decoded.keys[1] == 5 && !decoded.rollover);
    keyboard[2] = 1;
    assert(uiflow_hid_decode(1, keyboard, 8, &decoded) && decoded.rollover);
    uint8_t mouse[] = {0xff, 0x80, 0x7f, 0};
    assert(!uiflow_hid_decode(2, mouse, 2, &decoded));
    assert(uiflow_hid_decode(2, mouse, 3, &decoded));
    assert(decoded.buttons == 7 && decoded.x == -128 && decoded.y == 127);
    assert(!uiflow_hid_decode(0, mouse, 4, &decoded));

    for (int failure = 1; failure <= 3; ++failure) {
        allocation_calls = 0; fail_allocation = failure;
        assert(uiflow_usbhost_start() == ESP_ERR_NO_MEM);
        assert_clean();
    }
    fail_allocation = 0;
    bool *failures[] = {&fail_library, &fail_task, &fail_hid, &fail_enable};
    for (size_t i = 0; i < 4; ++i) {
        *failures[i] = true; assert(uiflow_usbhost_start() != ESP_OK); *failures[i] = false; assert_clean();
    }

    for (int cycle = 0; cycle < 100; ++cycle) {
        uint32_t old = uiflow_usbhost_generation();
        assert(uiflow_usbhost_start() == ESP_OK);
        uint32_t current = uiflow_usbhost_generation();
        assert(current != old && !uiflow_usbhost_active(old) && uiflow_usbhost_active(current));
        assert(uiflow_usbhost_start() == ESP_ERR_INVALID_STATE);
        struct fake_hid *d = connect_device(0, 1, 1);
        assert(uiflow_usbhost_service() == ESP_OK);
        uiflow_hid_device_t devices[UIFLOW_HID_MAX_INTERFACES];
        assert(uiflow_usbhost_devices(devices) == 1 && devices[0].vid == 0x1234);
        uiflow_hid_event_t event;
        assert(uiflow_usbhost_read(&event) && event.event == UIFLOW_HID_CONNECTED);
        driver_callback(d, HID_HOST_DRIVER_EVENT_CONNECTED, NULL);
        assert(uiflow_usbhost_service() == ESP_OK && !uiflow_usbhost_read(&event));
        memcpy(d->data, keyboard, 8); d->length = 8;
        for (int i = 0; i < 100; ++i) { interface_callback(d, HID_HOST_INTERFACE_EVENT_INPUT_REPORT, d->config.callback_arg); }
        assert(uiflow_usbhost_dropped() == 68);
        int count = 0;
        while (uiflow_usbhost_read(&event)) { assert(event.length == 8 && event.data[0] == 0x22); ++count; }
        assert(count == 32);
        assert(uiflow_usbhost_stop() == ESP_OK);
        assert(!uiflow_usbhost_active(current));
        assert_clean();
    }
    // Unplug before processing attach, and unplug during open.
    assert(uiflow_usbhost_start() == ESP_OK);
    struct fake_hid *d = connect_device(0, 2, 1); d->alive = false;
    assert(uiflow_usbhost_service() == ESP_OK);
    d = connect_device(0, 2, 1); unplug_on_open = true;
    assert(uiflow_usbhost_service() == ESP_OK); unplug_on_open = false;
    assert(uiflow_usbhost_stop() == ESP_OK); assert_clean();
    // Failed class request must close the interface and release its slot.
    assert(uiflow_usbhost_start() == ESP_OK); connect_device(0, 1, 1); fail_protocol = true;
    assert(uiflow_usbhost_service() == ESP_OK); fail_protocol = false;
    uiflow_hid_device_t devices[UIFLOW_HID_MAX_INTERFACES];
    assert(uiflow_usbhost_devices(devices) == 0);
    assert(uiflow_usbhost_stop() == ESP_OK); assert_clean();
    // A close failure is observable and cannot leave a failed interface ready.
    assert(uiflow_usbhost_start() == ESP_OK); connect_device(0, 1, 1);
    fail_protocol = true; fail_close = true;
    assert(uiflow_usbhost_service() == ESP_ERR_TIMEOUT);
    fail_protocol = false; fail_close = false;
    assert(uiflow_usbhost_devices(devices) == 0);
    assert(uiflow_usbhost_stop() == ESP_OK); assert_clean();
    // Never silently lose an attach notification.
    assert(uiflow_usbhost_start() == ESP_OK);
    for (size_t i = 0; i < 17; ++i) { connect_device(i, 1, 1); }
    assert(uiflow_usbhost_service() == ESP_ERR_NO_MEM);
    assert(uiflow_usbhost_stop() == ESP_OK); assert_clean();
    // VBUS failure must not leave tasks referencing destroyed native queues.
    assert(uiflow_usbhost_start() == ESP_OK); fail_disable = true;
    assert(uiflow_usbhost_stop() == ESP_FAIL);
    assert(resources == 0 && !thread_created && !atomic_load(&host_ok));
    assert(uiflow_usbhost_start() == ESP_ERR_INVALID_STATE);
    fail_disable = false;
    assert(uiflow_usbhost_stop() == ESP_OK); assert_clean();
    return 0;
}
