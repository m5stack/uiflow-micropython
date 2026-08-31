/*
* SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "py/mpconfig.h"
#include "esp_log.h"
#include "driver/gpio.h"

// CoreInk latches its own power rail on with GPIO12: running on battery, the
// rail stays up only while that pin is driven high - or while the user keeps
// the power button pressed. Out of reset the pad is an input, so there is a
// window on every boot during which nothing holds the rail up.
//
// M5GFX does assert the pin, but only as a side effect of board autodetect,
// which is reached from M5.begin() around 2s into a MicroPython boot. The
// rail does not survive unaided for anything like that long. On battery the
// consequences are that the board switches itself off after any reset, and
// that powering it on means holding the power button down for seconds rather
// than pressing it.
//
// Asserting the latch here - the first thing app_main does, before the
// MicroPython task is created - closes that window to ~50ms.
#define COREINK_POWER_HOLD_PIN  GPIO_NUM_12

void CoreInk_board_startup(void) {
    gpio_config_t power_hold = {
        .pin_bit_mask = 1ULL << COREINK_POWER_HOLD_PIN,
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&power_hold);
    gpio_set_level(COREINK_POWER_HOLD_PIN, 1);
    ESP_LOGI("CoreInk", "power hold (GPIO12) asserted");

    boardctrl_startup();
}
