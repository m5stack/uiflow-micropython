/*
* SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME               "M5STACK StampS3Bat"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3-PICO-1-N8R8"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
#define MICROPY_HW_ENABLE_UART_REPL         (0)

#define MICROPY_HW_I2C0_SCL                 (47)
#define MICROPY_HW_I2C0_SDA                 (48)

#define MICROPY_HW_USB_VID 0x303A
#define MICROPY_HW_USB_PID 0x816B
#define MICROPY_HW_USB_MANUFACTURER_STRING "M5Stack"
#define MICROPY_HW_USB_PRODUCT_FS_STRING "StampS3Bat(UiFlow2)"
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "StampS3Bat(UiFlow2)"

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
