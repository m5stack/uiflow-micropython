/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME "M5STACK CoreInk"
#define MICROPY_HW_MCU_NAME "ESP32-S3"

// Assert the power-hold latch (GPIO12) from app_main, before the
// MicroPython task starts - see board_init.c.
#define MICROPY_BOARD_STARTUP CoreInk_board_startup
void CoreInk_board_startup(void);

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
