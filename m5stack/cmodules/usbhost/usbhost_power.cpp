// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include <M5Unified.h>

extern "C" bool uiflow_usbhost_set_power(bool enable) {
    auto board = M5.getBoard();
    if (board != m5::board_t::board_M5Tab5 && board != m5::board_t::board_M5Tab5X) {
        return false;
    }
    return M5.Power.setExtOutput(enable, m5::ext_port_mask_t::ext_USB);
}
