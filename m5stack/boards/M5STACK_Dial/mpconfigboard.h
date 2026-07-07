/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME               "M5STACK Dial"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3-FN8"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
// #define MICROPY_HW_ENABLE_UART_REPL         (1)

#define MICROPY_HW_I2C0_SCL                 (15)
#define MICROPY_HW_I2C0_SDA                 (13)

#define MICROPY_HW_USB_VID 0x303A
#define MICROPY_HW_USB_PID 0x81DD
#define MICROPY_HW_USB_MANUFACTURER_STRING "M5Stack"
#define MICROPY_HW_USB_PRODUCT_FS_STRING "Dial(UiFlow2)"
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "Dial(UiFlow2)"

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
