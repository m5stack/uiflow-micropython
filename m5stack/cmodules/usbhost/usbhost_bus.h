// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT
#pragma once
#include "esp_err.h"
#include <stdint.h>

enum { UIFLOW_USB_BUS_NONE, UIFLOW_USB_BUS_HID, UIFLOW_USB_BUS_UVC };

// Called from the VM only. One class owns the directly connected USB-A port.
esp_err_t uiflow_usb_bus_claim(unsigned owner);
esp_err_t uiflow_usb_bus_enable(unsigned owner);
esp_err_t uiflow_usb_bus_disconnect(unsigned owner);
esp_err_t uiflow_usb_bus_release(unsigned owner);
unsigned uiflow_usb_bus_owner(void);
esp_err_t uiflow_usb_bus_error(void);
