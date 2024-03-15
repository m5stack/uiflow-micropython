/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

// This configuration is for a generic ESP32C3 board with 4MiB (or more) of flash.

#define MICROPY_HW_BOARD_NAME               "M5STACK C3"
#define MICROPY_HW_MCU_NAME                 "ESP32C3"

#define MICROPY_HW_ENABLE_SDCARD            (0)
#define MICROPY_PY_MACHINE_DAC              (0)
#define MICROPY_PY_MACHINE_I2S              (0)

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
