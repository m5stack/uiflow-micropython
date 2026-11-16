/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#define MICROPY_HW_BOARD_NAME "M5STACK BASIC"
#define MICROPY_HW_MCU_NAME "ESP32"

// Basic shares internal RAM between Python and HTTPS. Start with smaller
// GC areas so transient Python allocations leave room for the TLS handshake;
// the split heap can still grow on demand.
#define MICROPY_GC_INITIAL_HEAP_SIZE (36 * 1024)

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"
