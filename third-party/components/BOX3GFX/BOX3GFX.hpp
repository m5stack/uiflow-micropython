#pragma once

#include <M5Unified.h>
#include <lgfx/v1/panel/Panel_ILI9342.hpp>
#include <lgfx/v1/touch/Touch_GT911.hpp>
#include <utility/Touch_Class.hpp>

class BOX3GFX: public lgfx::LGFX_Device {
    lgfx::Panel_ILI9342 _panel_instance;
    // lgfx::Touch_GT911   _touch_instance;
    lgfx::Bus_SPI       _spi_bus_instance;
    lgfx::Light_PWM     _light_instance;

public:
    lgfx::Touch_GT911   _touch_instance;

    m5::Touch_Class Touch;

    BOX3GFX() {

        {
            auto cfg = _light_instance.config();
            cfg.pin_bl = 47;
            cfg.invert = false;
            cfg.freq = 1000;
            cfg.pwm_channel = 7;

            ESP_LOGE("LIGHT","bl: %d invert: %s freq: %d chn: %d", cfg.pin_bl, cfg.invert ? "true" : "false", cfg.freq, cfg.pwm_channel);
            _light_instance.config(cfg);
        }

        {
            auto cfg = _spi_bus_instance.config();

            // cfg.spi_host = (spi_host_device_t)2;
            // cfg.spi_mode = 0;
            cfg.freq_write = 40000000;
            cfg.freq_read = 16000000;
            cfg.spi_3wire = true;
            // cfg.use_lock = true;
            // cfg.dma_channel = 3; // AUTO
            cfg.pin_sclk = 7;
            cfg.pin_mosi = 6;
            cfg.pin_miso = -1;
            cfg.pin_dc = 4;

            _spi_bus_instance.config(cfg);
        }

        {
            auto cfg = _panel_instance.config();

            cfg.invert       = false;
            cfg.pin_cs       = 5;
            cfg.pin_rst      = -1;
            cfg.pin_busy     = -1;
            cfg.panel_width  = 320;
            cfg.panel_height = 240;
            cfg.offset_x     = 0;
            cfg.offset_y     = 0;

            // cfg.offset_rotation = 0;
            // cfg.dummy_read_pixel = 8;
            // cfg.dummy_read_bits = 1;
            // cfg.readable = true;
            // cfg.invert = false;
            cfg.rgb_order = false;
            // cfg.dlen_16bit = false;
            // cfg.bus_shared = false;

            _panel_instance.setBus(&_spi_bus_instance);
            _panel_instance.config(cfg);
        }

        {
            auto cfg = _touch_instance.config();
            cfg.pin_int  = -1;
            cfg.pin_sda  = GPIO_NUM_8;
            cfg.pin_scl  = GPIO_NUM_18;
            cfg.i2c_addr = 0x5d;
            cfg.i2c_port = I2C_NUM_0;
            cfg.x_min = 0;
            cfg.x_max = 319;
            cfg.y_min = 0;
            cfg.y_max = 279;
            cfg.offset_rotation = 2;
            cfg.bus_shared = false;
            _touch_instance.config(cfg);
            // if (!_touch_instance.init()) {
            //     cfg.i2c_addr = 0x5D; // addr change (0x14 or 0x5D)
            //     _touch_instance.config(cfg);
            // }
            _panel_instance.touch(&_touch_instance);
        }

        _panel_instance.setLight(&_light_instance);
        setPanel(&_panel_instance);
    };
};

extern BOX3GFX box3GFX;