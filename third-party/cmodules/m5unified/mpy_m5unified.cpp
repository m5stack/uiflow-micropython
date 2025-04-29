/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/


#include <M5Unified.h>
#include <esp_log.h>
#include <sdkconfig.h>
#include <BOX3GFX.hpp>


extern "C"
{
#include "mpy_m5unified.h"
#include "mphalport.h"
#include "hal/gpio_hal.h"


/* *FORMAT-OFF* */
gfx_obj_t m5_display = {&mp_gfxdevice_type, &(box3GFX), NULL};
touch_obj_t m5_touch = {&mp_touch_type,     &(box3GFX.Touch)};
/* *FORMAT-ON* */


static void pinMode(uint8_t pin, uint8_t mode)
{

    gpio_hal_context_t gpiohal;
    gpiohal.dev = GPIO_LL_GET_HW(GPIO_PORT_0);

    gpio_config_t conf = {
        .pin_bit_mask = (1ULL<<pin),                 /*!< GPIO pin: set with bit mask, each bit maps to a GPIO */
        .mode = GPIO_MODE_DISABLE,                   /*!< GPIO mode: set input/output mode                     */
        .pull_up_en = GPIO_PULLUP_DISABLE,           /*!< GPIO pull-up                                         */
        .pull_down_en = GPIO_PULLDOWN_DISABLE,       /*!< GPIO pull-down                                       */
        .intr_type = (gpio_int_type_t)gpiohal.dev->pin[pin].int_type  /*!< GPIO interrupt type - previously set                 */
    };
    if (mode < 0x20) {//io
        conf.mode = (gpio_mode_t)(mode & (0x01 | 0x03)); // 0x01 OUTPUT 0x03 OUTPUT
        if (mode & 0x10) { // OPEN_DRAIN
            conf.mode = (gpio_mode_t) (conf.mode | GPIO_MODE_DEF_OD);
        }
        if (mode & 0x04) { // PULLUP
            conf.pull_up_en = GPIO_PULLUP_ENABLE;
        }
        if (mode & 0x08) { // PULLDOWN
            conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
        }
    }
    if(gpio_config(&conf) != ESP_OK)
    {
        ESP_LOGE("pinMode", "GPIO config failed");
        return;
    }
}


// TODO: pass configuration parameters
mp_obj_t m5_begin(size_t n_args, const mp_obj_t *args)
{
#if 0
    mp_obj_t config_obj = mp_const_none;

    auto cfg = M5.config();
    cfg.external_display_value = 0; // disable all external display

    // initial
    M5.begin(cfg);
    M5.In_I2C.release();

    M5.Display.clear();
    // default display
    m5_display.gfx = (void *)(&(M5.Display));
    // set default font to DejaVu9, keep same style with UIFlow website UI design.
    M5.Display.setTextFont(&fonts::DejaVu9);
#endif
    // https://github.com/lovyan03/LovyanGFX/issues/569

    if (!box3GFX._touch_instance.init()) {
        auto cfg = box3GFX._touch_instance.config();
        cfg.i2c_addr = 0x5D; // addr change (0x14 or 0x5D)
        box3GFX._touch_instance.config(cfg);
    }

    pinMode(48, 0x05); // INPUT_PULLUP
    box3GFX.begin();
    box3GFX.setRotation(2);
    box3GFX.setBrightness(127);
    m5_display.gfx = (void *)(&(box3GFX));
    box3GFX.setTextFont(&fonts::DejaVu9);
    box3GFX.fillScreen(0x000000);

    box3GFX.Touch.begin(&box3GFX);

    return mp_const_none;
}


mp_obj_t m5_update(void) {
    // M5.update();

    auto ms = m5gfx::millis();

    if (box3GFX.Touch.isEnabled())
    {
        box3GFX.Touch.update(ms);
    }

    return mp_const_none;
}

mp_obj_t m5_end(void) {
    return mp_const_none;
}

mp_obj_t m5_getBoard(void) {
    return mp_obj_new_int(BOARD_ID);
}
}