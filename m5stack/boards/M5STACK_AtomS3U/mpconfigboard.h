/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME               "M5STACK AtomS3U"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3-FN8"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
#define MICROPY_HW_ENABLE_UART_REPL         (0)

#define MICROPY_HW_I2C0_SCL                 (1)
#define MICROPY_HW_I2C0_SDA                 (2)

// https://github.com/espressif/usb-pids/blob/main/allocated-pids.txt#L399
#define MICROPY_HW_USB_VID 0x303A
#define MICROPY_HW_USB_PID 0x8187
#define MICROPY_HW_USB_MANUFACTURER_STRING "M5Stack"
#define MICROPY_HW_USB_PRODUCT_FS_STRING "AtomS3U(UiFlow2)"
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "AtomS3U(UiFlow2)"

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
