// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include <stdatomic.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "usb/usb_host.h"
#include "usb/hid_host.h"
#include "usbhost.h"
#include "usbhost_bus.h"
#include "uvc_camera.h"

#define SHUTDOWN_MS (5000)

typedef struct {
    hid_host_device_handle_t handle;
    uiflow_hid_device_t device;
    bool ready;
} hid_slot_t;

// All callbacks own only native storage. No Python object crosses task boundaries.
static hid_slot_t slots[UIFLOW_HID_MAX_INTERFACES];
static portMUX_TYPE slots_lock = portMUX_INITIALIZER_UNLOCKED;
static QueueHandle_t connections;
static QueueHandle_t reports;
static bool hid_installed;
static uint32_t generation;
static atomic_bool stopping;
static atomic_uint dropped;
static atomic_int fatal_error;

static void emit(const uiflow_hid_event_t *event) {
    if (atomic_load(&stopping)) {
        return;
    }
    if (xQueueSend(reports, event, 0) != pdTRUE) {
        uiflow_hid_event_t discarded;
        if (xQueueReceive(reports, &discarded, 0) == pdTRUE) {
            atomic_fetch_add(&dropped, 1);
        }
        if (xQueueSend(reports, event, 0) != pdTRUE) {
            atomic_fetch_add(&dropped, 1);
        }
    }
}

static void interface_callback(hid_host_device_handle_t handle, hid_host_interface_event_t event, void *arg) {
    hid_slot_t *slot = arg;
    uiflow_hid_event_t report = {0};
    portENTER_CRITICAL(&slots_lock);
    bool known = slot->handle == handle;
    bool ready = slot->ready;
    report.device = slot->device;
    if (known && event == HID_HOST_INTERFACE_EVENT_DISCONNECTED) {
        slot->handle = NULL;
        slot->ready = false;
    }
    portEXIT_CRITICAL(&slots_lock);
    if (!known) {
        return;
    }
    if (event == HID_HOST_INTERFACE_EVENT_DISCONNECTED) {
        report.event = UIFLOW_HID_DISCONNECTED;
        emit(&report);
        esp_err_t err = hid_host_device_close(handle);
        if (err != ESP_OK) {
            atomic_store(&fatal_error, err);
        }
    } else if (event == HID_HOST_INTERFACE_EVENT_INPUT_REPORT && ready) {
        size_t length = 0;
        report.error = hid_host_device_get_raw_input_report_data(handle, report.data, sizeof(report.data), &length);
        report.length = length;
        report.event = report.error == ESP_OK ? UIFLOW_HID_INPUT : UIFLOW_HID_ERROR;
        emit(&report);
    } else if (event == HID_HOST_INTERFACE_EVENT_TRANSFER_ERROR) {
        report.event = UIFLOW_HID_ERROR;
        report.error = ESP_FAIL;
        emit(&report);
    }
}

static void driver_callback(hid_host_device_handle_t handle, hid_host_driver_event_t event, void *arg) {
    if (event == HID_HOST_DRIVER_EVENT_CONNECTED && !atomic_load(&stopping)) {
        if (xQueueSend(connections, &handle, 0) != pdTRUE) {
            // A lost attach notification must be observable; power-off during stop
            // still lets the driver reclaim interfaces that were never opened.
            atomic_store(&fatal_error, ESP_ERR_NO_MEM);
        }
    }
}

static void attach(hid_host_device_handle_t handle) {
    hid_host_dev_params_t params;
    if (hid_host_device_get_params(handle, &params) != ESP_OK) {
        return; // Unplugged before the application serviced the notification.
    }
    uiflow_hid_event_t event = {.device = {
                                    .address = params.addr, .interface = params.iface_num, .protocol = params.proto,
                                }};
    if (params.sub_class != HID_SUBCLASS_BOOT_INTERFACE ||
        (params.proto != HID_PROTOCOL_KEYBOARD && params.proto != HID_PROTOCOL_MOUSE)) {
        event.event = UIFLOW_HID_UNSUPPORTED;
        emit(&event);
        return;
    }
    hid_slot_t *slot = NULL;
    portENTER_CRITICAL(&slots_lock);
    for (size_t i = 0; i < UIFLOW_HID_MAX_INTERFACES; ++i) {
        if (slots[i].handle == handle) {
            portEXIT_CRITICAL(&slots_lock);
            return;
        }
    }
    for (size_t i = 0; i < UIFLOW_HID_MAX_INTERFACES; ++i) {
        if (slots[i].handle == NULL) {
            slot = &slots[i];
            slot->handle = handle;
            slot->device = event.device;
            slot->ready = false;
            break;
        }
    }
    portEXIT_CRITICAL(&slots_lock);
    if (slot == NULL) {
        event.event = UIFLOW_HID_ERROR;
        event.error = ESP_ERR_NO_MEM;
        emit(&event);
        return;
    }
    const hid_host_device_config_t config = {.callback = interface_callback, .callback_arg = slot};
    esp_err_t err = hid_host_device_open(handle, &config);
    if (err != ESP_OK) {
        portENTER_CRITICAL(&slots_lock);
        if (slot->handle == handle) {
            slot->handle = NULL;
        }
        portEXIT_CRITICAL(&slots_lock);
    } else {
        hid_host_dev_info_t info;
        err = hid_host_get_device_info(handle, &info);
        if (err == ESP_OK) {
            event.device.vid = info.VID;
            event.device.pid = info.PID;
            err = hid_class_request_set_protocol(handle, HID_REPORT_PROTOCOL_BOOT);
        }
        if (err == ESP_OK && params.proto == HID_PROTOCOL_KEYBOARD) {
            err = hid_class_request_set_idle(handle, 0, 0);
        }
        if (err == ESP_OK) {
            portENTER_CRITICAL(&slots_lock);
            if (slot->handle == handle) {
                slot->device = event.device;
                slot->ready = true;
            } else {
                err = ESP_ERR_NOT_FOUND;
            }
            portEXIT_CRITICAL(&slots_lock);
        }
        if (err == ESP_OK) {
            event.event = UIFLOW_HID_CONNECTED;
            emit(&event);
            err = hid_host_device_start(handle);
        }
        if (err != ESP_OK) {
            // The driver's close callback also removes this slot.
            portENTER_CRITICAL(&slots_lock);
            bool known = slot->handle == handle;
            if (known) {
                slot->ready = false;
            }
            portEXIT_CRITICAL(&slots_lock);
            if (known) {
                esp_err_t close_error = hid_host_device_close(handle);
                if (close_error != ESP_OK) {
                    atomic_store(&fatal_error, close_error);
                }
            }
        }
    }
    if (err != ESP_OK) {
        event.event = UIFLOW_HID_ERROR;
        event.error = err;
        emit(&event);
    }
}

esp_err_t uiflow_usbhost_service(void) {
    if (!hid_installed || atomic_load(&stopping)) {
        return ESP_ERR_INVALID_STATE;
    }
    int err = uiflow_usb_bus_error();
    if (err == ESP_OK) {
        err = atomic_load(&fatal_error);
    }
    if (err != ESP_OK) {
        return err;
    }
    // Control requests block waiting for the HID driver's background task.
    // Run them from the VM's polling call, never from that task's callbacks.
    hid_host_device_handle_t handle;
    while (xQueueReceive(connections, &handle, 0) == pdTRUE) {
        attach(handle);
    }
    return atomic_load(&fatal_error);
}

esp_err_t uiflow_usbhost_stop(void) {
    atomic_store(&stopping, true);
    esp_err_t power_error = ESP_OK;
    if (uiflow_usb_bus_owner() == UIFLOW_USB_BUS_HID) {
        power_error = uiflow_usb_bus_disconnect(UIFLOW_USB_BUS_HID);
    }
    if (hid_installed) {
        TickType_t start = xTaskGetTickCount();
        esp_err_t err;
        do {
            err = hid_host_uninstall();
            if (err == ESP_OK) {
                break;
            }
            if (err != ESP_ERR_INVALID_STATE) {
                return err;
            }
            vTaskDelay(pdMS_TO_TICKS(10));
        } while (xTaskGetTickCount() - start < pdMS_TO_TICKS(SHUTDOWN_MS));
        if (err != ESP_OK) {
            return err;
        }
        hid_installed = false;
    }
    if (uiflow_usb_bus_owner() == UIFLOW_USB_BUS_HID) {
        esp_err_t err = uiflow_usb_bus_release(UIFLOW_USB_BUS_HID);
        if (err != ESP_OK) {
            return err;
        }
    }
    if (connections != NULL) {
        vQueueDelete(connections);
        connections = NULL;
    }
    if (reports != NULL) {
        vQueueDelete(reports);
        reports = NULL;
    }
    memset(slots, 0, sizeof(slots));
    return power_error;
}

esp_err_t uiflow_usbhost_start(void) {
    if (connections != NULL || uiflow_usb_bus_owner() != UIFLOW_USB_BUS_NONE) {
        return ESP_ERR_INVALID_STATE;
    }
    atomic_store(&stopping, false);
    atomic_store(&dropped, 0);
    atomic_store(&fatal_error, ESP_OK);
    esp_err_t err = uiflow_usb_bus_claim(UIFLOW_USB_BUS_HID);
    if (err != ESP_OK) {
        goto fail;
    }
    connections = xQueueCreate(16, sizeof(hid_host_device_handle_t));
    reports = xQueueCreate(32, sizeof(uiflow_hid_event_t));
    if (connections == NULL || reports == NULL) {
        err = ESP_ERR_NO_MEM;
        goto fail;
    }
    const hid_host_driver_config_t hid_config = {
        .create_background_task = true,
        .task_priority = 5,
        .stack_size = 4096,
        .core_id = tskNO_AFFINITY,
        .callback = driver_callback,
    };
    err = hid_host_install(&hid_config);
    if (err != ESP_OK) {
        goto fail;
    }
    hid_installed = true;
    err = uiflow_usb_bus_enable(UIFLOW_USB_BUS_HID);
    if (err != ESP_OK) {
        goto fail;
    }
    ++generation;
    return ESP_OK;

fail:
    // Keep native resources alive if cleanup fails; never leave tasks pointing
    // at freed queues, and let deinit() retry a failed cleanup.
    esp_err_t cleanup_error = uiflow_usbhost_stop();
    if (cleanup_error != ESP_OK) {
        ESP_LOGE("usbhost", "Start rollback failed: %s", esp_err_to_name(cleanup_error));
    }
    return err;
}

bool uiflow_usbhost_active(uint32_t expected_generation) {
    return hid_installed && !atomic_load(&stopping) && generation == expected_generation;
}

uint32_t uiflow_usbhost_generation(void) {
    return generation;
}

bool uiflow_usbhost_read(uiflow_hid_event_t *event) {
    return xQueueReceive(reports, event, 0) == pdTRUE;
}

size_t uiflow_usbhost_devices(uiflow_hid_device_t *devices) {
    size_t count = 0;
    portENTER_CRITICAL(&slots_lock);
    for (size_t i = 0; i < UIFLOW_HID_MAX_INTERFACES; ++i) {
        if (slots[i].ready) {
            devices[count++] = slots[i].device;
        }
    }
    portEXIT_CRITICAL(&slots_lock);
    return count;
}

uint32_t uiflow_usbhost_dropped(void) {
    return atomic_load(&dropped);
}

void uiflow_usbhost_deinit_all(void) {
    esp_err_t err = uiflow_uvc_deinit();
    if (err != ESP_OK) {
        ESP_LOGE("usbhost", "UVC Host cleanup failed: %s", esp_err_to_name(err));
    }
    err = uiflow_usbhost_stop();
    if (err != ESP_OK) {
        ESP_LOGE("usbhost", "HID Host cleanup failed: %s", esp_err_to_name(err));
    }
}
