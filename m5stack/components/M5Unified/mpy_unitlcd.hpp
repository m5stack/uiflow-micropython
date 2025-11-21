/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/
#pragma once

// If you want to use a set of functions to handle SD/SPIFFS/HTTP,
//  please include <SD.h>,<SPIFFS.h>,<HTTPClient.h> before <M5GFX.h>
// #include <SD.h>
// #include <SPIFFS.h>
// #include <HTTPClient.h>

#if defined (ESP_PLATFORM)
 #include <sdkconfig.h>
#else
 #include "lgfx/v1/platforms/sdl/Panel_sdl.hpp"
#endif

#include "mpy_i2cbus.hpp"
#include "lgfx/v1/panel/Panel_M5UnitLCD.hpp"
#include "M5GFX.h"

extern "C" {
#include "py/obj.h"
#include "py/runtime.h"
}

#ifndef M5UNITLCD_ADDR
#define M5UNITLCD_ADDR 0x3E
#endif

class MPY_M5UnitLCD : public M5GFX
{
    MPY_Bus_I2C::config_t _bus_cfg;

public:

    struct config_t
    {
        uint8_t i2c_addr = M5UNITLCD_ADDR;
        mp_obj_t readfrom_into_method[2];
        mp_obj_t writeto_method[2];
    };

    config_t config(void) const { return config_t(); }

    MPY_M5UnitLCD(const config_t &cfg)
    {
        memcpy(_bus_cfg.readfrom_into_method, cfg.readfrom_into_method, sizeof(cfg.readfrom_into_method));
        memcpy(_bus_cfg.writeto_method, cfg.writeto_method, sizeof(cfg.writeto_method));
        setup(cfg.i2c_addr);
    }

    MPY_M5UnitLCD(uint8_t i2c_addr = M5UNITLCD_ADDR)
    {
        setup(i2c_addr);
    }

    using lgfx::LGFX_Device::init;
    bool init(uint8_t i2c_addr = M5UNITLCD_ADDR)
    {
        setup(i2c_addr);
        // Call the base class init() explicitly to avoid infinite recursion due to default parameter
        return lgfx::LGFX_Device::init();
    }

    void setup(uint8_t i2c_addr = M5UNITLCD_ADDR)
    {
        _board = lgfx::board_t::board_M5UnitLCD;

        {
            _bus_cfg.i2c_addr = i2c_addr;
            _bus_cfg.prefix_len = 0;
        }
    }

    bool init_impl(bool use_reset, bool use_clear)
    {
        if (_panel_last.get() != nullptr) {
            return true;
        }
        auto p = new lgfx::Panel_M5UnitLCD;
        auto b = new MPY_Bus_I2C();
        b->config(_bus_cfg);
        b->init();
        {
            p->bus(b);
            auto cfg = p->config();
            cfg.memory_width     = 135;
            cfg.memory_height    = 240;
            cfg.panel_width      = 135;
            cfg.panel_height     = 240;
            cfg.offset_x         =   0;
            cfg.offset_rotation  =   0;
            cfg.bus_shared       = false;
            p->config(cfg);
        }
        setPanel(p);
        if (lgfx::LGFX_Device::init_impl(use_reset, use_clear)) {
            _panel_last.reset(p);
            _bus_last.reset(b);
            return true;
        }
        setPanel(nullptr);
        delete p;
        delete b;
        return false;
    }

};
