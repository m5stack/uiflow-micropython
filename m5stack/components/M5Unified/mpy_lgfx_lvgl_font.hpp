/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#pragma once

#include <M5GFX.h>
#include "lvgl/lvgl.h"

class M5LvglFont : public lgfx::IFont {
public:
    constexpr M5LvglFont(const lv_font_t *font = nullptr) : _font(font) {}

    font_type_t getType(void) const override { return ft_lvgl; }
    void getDefaultMetric(lgfx::FontMetrics *metrics) const override;
    bool updateFontMetric(lgfx::FontMetrics *metrics, uint16_t uniCode) const override;
    size_t drawChar(lgfx::LGFXBase *gfx, int32_t x, int32_t y, uint16_t c,
                    const lgfx::TextStyle *style, lgfx::FontMetrics *metrics,
                    int32_t &filled_x) const override;

private:
    const lv_font_t *_font;
};
