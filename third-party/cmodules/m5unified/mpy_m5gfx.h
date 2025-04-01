/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>
#include <py/stream.h>
#include <py/builtin.h>

enum user_panel_t {
    PANEL_UNKNOWN,
    SPI_LCD_ILI9342,
    SPI_LCD_ST7735,
    SPI_LCD_ST7735S,
    SPI_LCD_ST7789,
    SPI_LCD_GC9A01,
    SPI_LCD_GC9107,
    SPI_EINK_GDEW0154M09,
    SPI_EINK_IT8951,
    // SPI LCD add here
    SPI_PANEL_TYPE_MAX,
    I2C_OLED_SSD1306,
    I2C_OLED_SH110x,
    // I2C LCD add here
    I2C_PANEL_TYPE_MAX,
};

enum user_tp_t {
    TP_UNKNOWN,
    I2C_TP_FT5X06,
    I2C_TP_GT911,
    TP_TYPE_MAX
};

typedef struct _gfx_obj_t {
    mp_obj_base_t base;
    void *gfx;
    void *font_wrapper;
} gfx_obj_t;

typedef struct _font_obj_t {
    mp_obj_base_t base;
    const void *font;
} font_obj_t;


extern const mp_obj_type_t mp_gfxcanvas_type;
extern const mp_obj_type_t m5_user_display;
extern const mp_obj_type_t mp_gfxdevice_type;

extern const font_obj_t gfx_font_0_obj;
extern const font_obj_t gfx_font_DejaVu9_obj;
extern const font_obj_t gfx_font_DejaVu12_obj;
extern const font_obj_t gfx_font_DejaVu18_obj;
extern const font_obj_t gfx_font_DejaVu24_obj;
extern const font_obj_t gfx_font_DejaVu40_obj;
extern const font_obj_t gfx_font_DejaVu56_obj;
extern const font_obj_t gfx_font_DejaVu72_obj;
extern const font_obj_t gfx_font_efontCN_14_obj;
extern const font_obj_t gfx_font_efontCN_24_obj;
extern const font_obj_t gfx_font_efontJA_14_obj;
extern const font_obj_t gfx_font_efontJA_24_obj;
extern const font_obj_t gfx_font_efontKR_14_obj;
extern const font_obj_t gfx_font_efontKR_24_obj;
// extern const font_obj_t gfx_font_montserrat_6_obj;
// extern const font_obj_t gfx_font_montserrat_7_obj;
// extern const font_obj_t gfx_font_montserrat_8_obj;
// extern const font_obj_t gfx_font_montserrat_9_obj;
// extern const font_obj_t gfx_font_montserrat_10_obj;
