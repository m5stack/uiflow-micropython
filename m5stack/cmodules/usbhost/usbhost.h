// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT
#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "esp_err.h"

#define UIFLOW_HID_MAX_INTERFACES (8)

enum {
    UIFLOW_HID_CONNECTED,
    UIFLOW_HID_DISCONNECTED,
    UIFLOW_HID_INPUT,
    UIFLOW_HID_ERROR,
    UIFLOW_HID_UNSUPPORTED,
};

typedef struct {
    uint8_t address;
    uint8_t interface;
    uint8_t protocol;
    uint16_t vid;
    uint16_t pid;
} uiflow_hid_device_t;

typedef struct {
    uiflow_hid_device_t device;
    uint8_t event;
    uint8_t length;
    uint8_t data[8];
    esp_err_t error;
} uiflow_hid_event_t;

esp_err_t uiflow_usbhost_start(void);
esp_err_t uiflow_usbhost_stop(void);
esp_err_t uiflow_usbhost_service(void);
bool uiflow_usbhost_active(uint32_t generation);
uint32_t uiflow_usbhost_generation(void);
bool uiflow_usbhost_read(uiflow_hid_event_t *event);
size_t uiflow_usbhost_devices(uiflow_hid_device_t *devices);
uint32_t uiflow_usbhost_dropped(void);
bool uiflow_usbhost_set_power(bool enable);
void uiflow_usbhost_deinit_all(void);
