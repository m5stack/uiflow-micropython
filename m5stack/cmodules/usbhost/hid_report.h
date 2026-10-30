// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT
#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct {
    uint8_t modifiers;
    uint8_t keys[6];
    bool rollover;
    uint8_t buttons;
    int8_t x;
    int8_t y;
} uiflow_hid_report_t;

bool uiflow_hid_decode(uint8_t protocol, const uint8_t *data, size_t length, uiflow_hid_report_t *report);
