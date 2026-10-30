// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include <stdatomic.h>
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/task.h"
#include "usb/usb_host.h"
#include "usbhost.h"
#include "usbhost_bus.h"

#define BUS_DAEMON_DONE (1 << 0)
#define BUS_DEVICES_FREE (1 << 1)
#define BUS_SHUTDOWN_MS (5000)

static unsigned bus_owner;
static EventGroupHandle_t bus_lifecycle;
static bool bus_installed;
static bool bus_task_created;
static bool bus_power_owned;
static atomic_bool bus_task_stop;
static atomic_int bus_fatal_error;

static void bus_task(void *arg) {
    while (!atomic_load(&bus_task_stop)) {
        uint32_t flags = 0;
        esp_err_t err = usb_host_lib_handle_events(pdMS_TO_TICKS(50), &flags);
        if (err != ESP_OK && err != ESP_ERR_TIMEOUT) {
            atomic_store(&bus_fatal_error, err);
        }
        if (flags & USB_HOST_LIB_EVENT_FLAGS_NO_CLIENTS) {
            if (usb_host_device_free_all() == ESP_OK) {
                xEventGroupSetBits(bus_lifecycle, BUS_DEVICES_FREE);
            }
        }
        if (flags & USB_HOST_LIB_EVENT_FLAGS_ALL_FREE) {
            xEventGroupSetBits(bus_lifecycle, BUS_DEVICES_FREE);
        }
    }
    xEventGroupSetBits(bus_lifecycle, BUS_DAEMON_DONE);
    vTaskDelete(NULL);
}

unsigned uiflow_usb_bus_owner(void) {
    return bus_owner;
}

esp_err_t uiflow_usb_bus_error(void) {
    return atomic_load(&bus_fatal_error);
}

esp_err_t uiflow_usb_bus_claim(unsigned owner) {
    if (owner == UIFLOW_USB_BUS_NONE || bus_owner != UIFLOW_USB_BUS_NONE) {
        return ESP_ERR_INVALID_STATE;
    }
    bus_owner = owner;
    atomic_store(&bus_task_stop, false);
    atomic_store(&bus_fatal_error, ESP_OK);
    bus_lifecycle = xEventGroupCreate();
    if (bus_lifecycle == NULL) {
        return ESP_ERR_NO_MEM;
    }
    const usb_host_config_t config = {
        .intr_flags = ESP_INTR_FLAG_LEVEL1,
        .root_port_unpowered = true,
        // IDF peripheral 0 is the P4 high-speed controller on Tab5 USB-A.
        .peripheral_map = 1 << 0,
    };
    esp_err_t err = usb_host_install(&config);
    if (err != ESP_OK) {
        return err;
    }
    bus_installed = true;
    if (xTaskCreate(bus_task, "usbh_lib", 4096, NULL, 4, NULL) != pdPASS) {
        return ESP_ERR_NO_MEM;
    }
    bus_task_created = true;
    return ESP_OK;
}

esp_err_t uiflow_usb_bus_enable(unsigned owner) {
    if (bus_owner != owner || !bus_installed) {
        return ESP_ERR_INVALID_STATE;
    }
    // Record ownership even on failure so cleanup can retry the power write.
    bus_power_owned = true;
    if (!uiflow_usbhost_set_power(true)) {
        return ESP_FAIL;
    }
    return usb_host_lib_set_root_port_power(true);
}

esp_err_t uiflow_usb_bus_disconnect(unsigned owner) {
    if (bus_owner != owner) {
        return ESP_ERR_INVALID_STATE;
    }
    esp_err_t error = ESP_OK;
    if (bus_installed) {
        error = usb_host_lib_set_root_port_power(false);
    }
    if (bus_power_owned) {
        if (!uiflow_usbhost_set_power(false)) {
            if (error == ESP_OK) {
                error = ESP_FAIL;
            }
        } else {
            bus_power_owned = false;
        }
    }
    return error;
}

esp_err_t uiflow_usb_bus_release(unsigned owner) {
    if (bus_owner == UIFLOW_USB_BUS_NONE) {
        return ESP_OK;
    }
    if (bus_owner != owner) {
        return ESP_ERR_INVALID_STATE;
    }
    esp_err_t power_error = uiflow_usb_bus_disconnect(owner);
    if (bus_installed && bus_task_created) {
        // An ALL_FREE notification from initial startup must not satisfy teardown.
        xEventGroupClearBits(bus_lifecycle, BUS_DEVICES_FREE);
        if (usb_host_device_free_all() == ESP_OK) {
            xEventGroupSetBits(bus_lifecycle, BUS_DEVICES_FREE);
        }
        if (!(xEventGroupWaitBits(bus_lifecycle, BUS_DEVICES_FREE, pdFALSE, pdTRUE,
            pdMS_TO_TICKS(BUS_SHUTDOWN_MS)) & BUS_DEVICES_FREE)) {
            return ESP_ERR_TIMEOUT;
        }
        atomic_store(&bus_task_stop, true);
        usb_host_lib_unblock();
        if (!(xEventGroupWaitBits(bus_lifecycle, BUS_DAEMON_DONE, pdFALSE, pdTRUE,
            pdMS_TO_TICKS(BUS_SHUTDOWN_MS)) & BUS_DAEMON_DONE)) {
            return ESP_ERR_TIMEOUT;
        }
        bus_task_created = false;
    }
    if (bus_installed) {
        esp_err_t err = usb_host_uninstall();
        if (err != ESP_OK) {
            return err;
        }
        bus_installed = false;
    }
    if (bus_lifecycle != NULL) {
        vEventGroupDelete(bus_lifecycle);
        bus_lifecycle = NULL;
    }
    if (power_error == ESP_OK) {
        bus_owner = UIFLOW_USB_BUS_NONE;
    }
    return power_error;
}
