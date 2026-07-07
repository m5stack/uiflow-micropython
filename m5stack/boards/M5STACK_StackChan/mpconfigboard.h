/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME               "M5STACK StackChan"
#define MICROPY_HW_MCU_NAME                 "ESP32S3"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
#define MICROPY_HW_ENABLE_UART_REPL         (0)

#define MICROPY_HW_I2C0_SCL                 (1)
#define MICROPY_HW_I2C0_SDA                 (2)

// #define MICROPY_HW_ENABLE_USBDEV            (1)
// #define MICROPY_HW_USB_CDC                  (1)
// #define MICROPY_HW_ESP_USB_SERIAL_JTAG      (0)
// #define MICROPY_HW_USB_CDC_1200BPS_TOUCH    (1)

// https://github.com/espressif/usb-pids/blob/main/allocated-pids.txt#L290
#define MICROPY_HW_USB_VID 0x303A
#define MICROPY_HW_USB_PID 0x811A
#define MICROPY_HW_USB_MANUFACTURER_STRING "M5Stack"
#define MICROPY_HW_USB_PRODUCT_FS_STRING "StackChan(UiFlow2)"
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "StackChan(UiFlow2)"

// #define MICROPY_PY_LVGL_BENCHMARK (1)

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
