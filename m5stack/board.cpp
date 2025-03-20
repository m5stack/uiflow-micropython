/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "M5Unified.hpp"

extern "C" {
    #include "uiflow_utility.h"
    // #include <driver/periph_ctrl.h>
    #include "esp_log.h"

    static void in_i2c_init(void)
    {
        gpio_num_t in_scl = (gpio_num_t)M5.getPin(m5::pin_name_t::in_i2c_scl);
        gpio_num_t in_sda = (gpio_num_t)M5.getPin(m5::pin_name_t::in_i2c_sda);
        gpio_num_t ex_scl = (gpio_num_t)M5.getPin(m5::pin_name_t::ex_i2c_scl);
        gpio_num_t ex_sda = (gpio_num_t)M5.getPin(m5::pin_name_t::ex_i2c_sda);
        i2c_port_t ex_port = I2C_NUM_0;
#if SOC_I2C_NUM == 1
        i2c_port_t in_port = I2C_NUM_0;
#else
        i2c_port_t in_port = I2C_NUM_1;
        if (in_scl == ex_scl && in_sda == ex_sda) {
            in_port = ex_port;
        }
#endif

        if (in_scl != GPIO_NUM_NC || in_sda != GPIO_NUM_NC) {
            ESP_LOGI("BOARD", "Internal I2C(%d) init", in_port);
            i2c_config_t conf;
            memset(&conf, 0, sizeof(i2c_config_t));
            conf.mode = I2C_MODE_MASTER;
            conf.sda_io_num = in_sda;
            conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
            conf.scl_io_num = in_scl;
            conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
            conf.master.clk_speed = 100000;
            // .clk_flags = 0,          /*!< Optional, you can use I2C_SCLK_SRC_FLAG_* flags to choose i2c source clock here. */
            i2c_param_config(in_port, &conf);
            i2c_driver_install(in_port, I2C_MODE_MASTER, 0, 0, 0);
        }
    }

    void board_init()
    {
        auto cfg = M5.config();
        cfg.output_power = false;
        M5.begin(cfg);
        in_i2c_init();
        M5.In_I2C.release();
    }

    void power_init()
    {
        m5::board_t board_id = M5.getBoard();
        if (
            ! (board_id == m5::board_t::board_M5StackCore2
            || board_id == m5::board_t::board_M5StackCoreS3
            || board_id == m5::board_t::board_M5StackCoreS3SE
            || board_id == m5::board_t::board_M5Paper
            || board_id == m5::board_t::board_M5Station
            || board_id == m5::board_t::board_M5StickC
            || board_id == m5::board_t::board_M5StickCPlus
            || board_id == m5::board_t::board_M5Tough)
        ) {
            ESP_LOGW("BOARD", "Power init skipped");
            return;
        }
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
