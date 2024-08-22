/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "M5Unified.hpp"

extern "C" {
    #include "uiflow_utility.h"
    #include <driver/periph_ctrl.h>

    void board_init()
    {
        auto cfg = M5.config();
        cfg.output_power = false;
        M5.begin(cfg);
        if (M5.getBoard() == m5::board_t::board_M5StackCoreS3 || M5.getBoard() == m5::board_t::board_M5StackCoreS3SE) {
            periph_module_disable(PERIPH_I2C1_MODULE);
            i2c_config_t conf;
            memset(&conf, 0, sizeof(i2c_config_t));
            conf.mode = I2C_MODE_MASTER;
            conf.sda_io_num = GPIO_NUM_12;
            conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
            conf.scl_io_num = GPIO_NUM_11;
            conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
            conf.master.clk_speed = 100000;
            // .clk_flags = 0,          /*!< Optional, you can use I2C_SCLK_SRC_FLAG_* flags to choose i2c source clock here. */
            i2c_param_config(I2C_NUM_1, &conf);
            i2c_driver_install(I2C_NUM_1, I2C_MODE_MASTER, 0, 0, 0);
        }
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
