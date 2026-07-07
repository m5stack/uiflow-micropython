/*
* SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME               "M5STACK StopWatch"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3R8"

#define MICROPY_PY_MACHINE_DAC              (0)

#define MICROPY_HW_ENABLE_UART_REPL         (0)

#define MICROPY_HW_I2C0_SCL                 (48)
#define MICROPY_HW_I2C0_SDA                 (47)

#define MICROPY_HW_USB_VID 0x303A
#define MICROPY_HW_USB_PID 0x832F
#define MICROPY_HW_USB_MANUFACTURER_STRING "M5Stack"
#define MICROPY_HW_USB_PRODUCT_FS_STRING "StopWatch(UiFlow2)"
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "StopWatch(UiFlow2)"

#include "./../mpconfiglvgl.h"
