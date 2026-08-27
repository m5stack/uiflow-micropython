/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#define MICROPY_HW_BOARD_NAME    "M5Stack CoreMatrix"
#define MICROPY_HW_MCU_NAME      "ESP32-C61HR8"

#define MICROPY_PY_MACHINE_DAC   (0)
#define MICROPY_PY_MACHINE_I2S   (0)

#define MICROPY_HW_I2C0_SCL      (1)
#define MICROPY_HW_I2C0_SDA      (0)

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
