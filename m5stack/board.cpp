/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "M5Unified.hpp"

extern "C" {
    #include "uiflow_utility.h"

    void board_init()
    {
        auto cfg = M5.config();
        cfg.output_power = false;
        M5.begin(cfg);
    }

    void power_init()
    {
        char power_mode[32] = {0};
        size_t len;
        bool usb_output = false;
        bool bus_output = false;

        bool ret = nvs_read_str_helper((char *)"uiflow", (char *)"power_mode", power_mode, &len);
        if (ret == false) {
            // 当 nvs 没有 "power_mode" 时，设置默认值
            usb_output = false;
            bus_output = true;
            goto set_power;
        }

        if (strncmp(power_mode, "usb_in_bus_in", strlen("usb_in_bus_in")) == 0) {
            usb_output = false;
            bus_output = false;
        } else if (strncmp(power_mode, "usb_in_bus_out", strlen("usb_in_bus_out")) == 0) {
            usb_output = false;
            bus_output = true;
        } else if (strncmp(power_mode, "usb_out_bus_in", strlen("usb_out_bus_in")) == 0) {
            usb_output = true;
            bus_output = false;
        } else if (strncmp(power_mode, "usb_out_bus_out", strlen("usb_out_bus_out")) == 0) {
            usb_output = true;
            bus_output = true;
        }

set_power:
        M5.Power.setUsbOutput(usb_output);
        M5.Power.setExtOutput(bus_output);
    }
}