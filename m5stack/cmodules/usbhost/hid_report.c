// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include <string.h>
#include "hid_report.h"

bool uiflow_hid_decode(uint8_t protocol, const uint8_t *data, size_t length, uiflow_hid_report_t *report) {
    memset(report, 0, sizeof(*report));
    if (protocol == 1 && length == 8) {
        report->modifiers = data[0];
        memcpy(report->keys, data + 2, sizeof(report->keys));
        for (size_t i = 0; i < sizeof(report->keys); ++i) {
            if (report->keys[i] >= 1 && report->keys[i] <= 3) {
                report->rollover = true;
            }
        }
        return true;
    }
    if (protocol == 2 && length >= 3) {
        report->buttons = data[0] & 7;
        report->x = (int8_t)data[1];
        report->y = (int8_t)data[2];
        return true;
    }
    return false;
}
