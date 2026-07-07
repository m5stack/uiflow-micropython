/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "mpy_lgfx_lvgl_font.hpp"

#include <algorithm>
#include <vector>

#include "lgfx/v1/LGFXBase.hpp"
#include "lvgl/src/font/lv_font_fmt_txt.h"

extern "C" {

static uint32_t m5_get_lvgl_glyph_id(const lv_font_t *font, uint32_t unicode_letter) {
    auto fdsc = static_cast < const lv_font_fmt_txt_dsc_t * > (font->dsc);

    for (uint32_t i = 0; i < fdsc->cmap_num; ++i) {
        const lv_font_fmt_txt_cmap_t *cmap = &fdsc->cmaps[i];
        if (unicode_letter < cmap->range_start ||
            unicode_letter >= cmap->range_start + cmap->range_length) {
            continue;
        }

        uint32_t relative = unicode_letter - cmap->range_start;

        if (cmap->unicode_list == nullptr) {
            if (cmap->glyph_id_ofs_list == nullptr) {
                return cmap->glyph_id_start + relative;
            }

            const uint8_t *ofs = static_cast < const uint8_t * > (cmap->glyph_id_ofs_list);
            return cmap->glyph_id_start + ofs[relative];
        }

        auto begin = cmap->unicode_list;
        auto end = cmap->unicode_list + cmap->list_length;
        auto found = std::lower_bound(begin, end, relative);
        if (found == end || *found != relative) {
            continue;
        }

        uint32_t idx = found - begin;
        if (cmap->glyph_id_ofs_list == nullptr) {
            return cmap->glyph_id_start + idx;
        }

        const uint16_t *ofs = static_cast < const uint16_t * > (cmap->glyph_id_ofs_list);
        return cmap->glyph_id_start + ofs[idx];
    }

    return 0;
}

bool __attribute__((weak)) lv_font_get_glyph_dsc_fmt_txt(const lv_font_t *font,
    lv_font_glyph_dsc_t *dsc_out,
    uint32_t unicode_letter,
    uint32_t unicode_letter_next) {
    (void)unicode_letter_next;

    if (font == nullptr || font->dsc == nullptr || dsc_out == nullptr) {
        return false;
    }

    auto fdsc = static_cast < const lv_font_fmt_txt_dsc_t * > (font->dsc);
    uint32_t gid = m5_get_lvgl_glyph_id(font, unicode_letter);
    if (gid == 0) {
        return false;
    }

    const lv_font_fmt_txt_glyph_dsc_t *gdsc = &fdsc->glyph_dsc[gid];
    dsc_out->adv_w = gdsc->adv_w >> 4;
    dsc_out->box_w = gdsc->box_w;
    dsc_out->box_h = gdsc->box_h;
    dsc_out->ofs_x = gdsc->ofs_x;
    dsc_out->ofs_y = gdsc->ofs_y;
    dsc_out->format = fdsc->bpp == 1 ? LV_FONT_GLYPH_FORMAT_A1 :
        fdsc->bpp == 2 ? LV_FONT_GLYPH_FORMAT_A2 :
        fdsc->bpp == 4 ? LV_FONT_GLYPH_FORMAT_A4 :
        fdsc->bpp == 8 ? LV_FONT_GLYPH_FORMAT_A8 :
        LV_FONT_GLYPH_FORMAT_NONE;
    dsc_out->gid.index = gid;
    dsc_out->resolved_font = font;
    dsc_out->is_placeholder = false;
    return dsc_out->format != LV_FONT_GLYPH_FORMAT_NONE;
}

const void *__attribute__((weak)) lv_font_get_bitmap_fmt_txt(lv_font_glyph_dsc_t *g_dsc, lv_draw_buf_t *draw_buf) {
    (void)draw_buf;

    if (g_dsc == nullptr || g_dsc->resolved_font == nullptr || g_dsc->resolved_font->dsc == nullptr) {
        return nullptr;
    }

    auto fdsc = static_cast < const lv_font_fmt_txt_dsc_t * > (g_dsc->resolved_font->dsc);
    const lv_font_fmt_txt_glyph_dsc_t *gdsc = &fdsc->glyph_dsc[g_dsc->gid.index];
    return &fdsc->glyph_bitmap[gdsc->bitmap_index];
}

}

void M5LvglFont::getDefaultMetric(lgfx::FontMetrics *metrics) const {
    if (_font == nullptr) {
        metrics->width = 0;
        metrics->x_advance = 0;
        metrics->x_offset = 0;
        metrics->height = 0;
        metrics->y_advance = 0;
        metrics->y_offset = 0;
        metrics->baseline = 0;
        return;
    }

    metrics->height = _font->line_height;
    metrics->y_advance = _font->line_height;
    metrics->baseline = _font->line_height - _font->base_line;
    metrics->y_offset = -metrics->baseline;
    metrics->width = (_font->line_height * 5) >> 3;
    metrics->x_advance = metrics->width;
    metrics->x_offset = 0;
}

bool M5LvglFont::updateFontMetric(lgfx::FontMetrics *metrics, uint16_t uniCode) const {
    if (_font == nullptr || _font->get_glyph_dsc == nullptr) {
        metrics->x_offset = 0;
        metrics->width = metrics->x_advance = 0;
        return false;
    }

    lv_font_glyph_dsc_t gd;
    if (!_font->get_glyph_dsc(_font, &gd, uniCode, 0)) {
        metrics->x_offset = 0;
        metrics->width = metrics->x_advance = (metrics->height * 5) >> 3;
        return false;
    }

    metrics->x_offset = gd.ofs_x;
    metrics->width = gd.box_w;
    metrics->x_advance = gd.adv_w;
    return true;
}

static size_t draw_alpha_bitmap_common(lgfx::LGFXBase *gfx,
    int32_t x,
    int32_t y,
    const lgfx::TextStyle *style,
    lgfx::FontMetrics *metrics,
    int32_t &filled_x,
    int32_t xAdvance,
    int32_t xoffset,
    int32_t yoffset,
    uint32_t box_w,
    uint32_t box_h,
    const uint8_t *bitmap,
    uint32_t glyph_stride,
    uint32_t alpha_max) {
    int32_t sy = 65536 * style->size_y;
    int32_t sx = 65536 * style->size_x;

    auto cc = gfx->getColorConverter();
    uint32_t col_back = cc->convert(style->back_rgb888);
    uint32_t col_fore = cc->convert(style->fore_rgb888);
    bool fillbg = (style->back_rgb888 != style->fore_rgb888);
    int32_t glyph_w_scaled = (box_w * sx) >> 16;

    int32_t left = 0;
    int32_t right = 0;
    if (fillbg) {
        left = std::max < int > (filled_x, x + (xoffset < 0 ? xoffset : 0));
        right = x + std::max < int > (glyph_w_scaled + xoffset, xAdvance);
        filled_x = right;
    }

    int32_t draw_x = x + xoffset;

    uint32_t back_rgb = fillbg ? style->back_rgb888 : gfx->getBaseColor();
    int32_t fore_r = (style->fore_rgb888 >> 16) & 0xFF;
    int32_t fore_g = (style->fore_rgb888 >> 8) & 0xFF;
    int32_t fore_b = style->fore_rgb888 & 0xFF;
    int32_t back_r = (back_rgb >> 16) & 0xFF;
    int32_t back_g = (back_rgb >> 8) & 0xFF;
    int32_t back_b = back_rgb & 0xFF;

    gfx->startWrite();

    if (fillbg && left < right) {
        gfx->setRawColor(col_back);
        if (yoffset > 0) {
            gfx->writeFillRect(left, y, right - left, (yoffset * sy) >> 16);
        }
        int32_t y0 = ((yoffset + (int32_t)box_h) * sy) >> 16;
        int32_t y1 = (metrics->height * sy) >> 16;
        if (y0 < y1) {
            gfx->writeFillRect(left, y + y0, right - left, y1 - y0);
        }
    }

    if (bitmap != nullptr && box_w && box_h) {
        for (uint32_t py = 0; py < box_h; ++py) {
            int32_t y0 = ((yoffset + (int32_t)py) * sy) >> 16;
            int32_t y1 = ((yoffset + (int32_t)py + 1) * sy) >> 16;
            if (y1 <= y0) {
                continue;
            }

            if (fillbg && left < right) {
                gfx->setRawColor(col_back);
                if (left < draw_x) {
                    gfx->writeFillRect(left, y + y0, draw_x - left, y1 - y0);
                }
                int32_t draw_right = draw_x + glyph_w_scaled;
                if (draw_right < right) {
                    gfx->writeFillRect(draw_right, y + y0, right - draw_right, y1 - y0);
                }
            }

            for (uint32_t px = 0; px < box_w; ++px) {
                uint32_t alpha = bitmap[py * glyph_stride + px];

                if (!fillbg && alpha == 0) {
                    continue;
                }

                int32_t x0 = ((int32_t)px * sx) >> 16;
                int32_t x1 = (((int32_t)px + 1) * sx) >> 16;
                if (x1 <= x0) {
                    continue;
                }

                uint32_t raw;
                if (alpha == 0) {
                    raw = col_back;
                } else if (alpha >= alpha_max) {
                    raw = col_fore;
                } else {
                    int32_t r = back_r + ((fore_r - back_r) * (int32_t)alpha + (int32_t)(alpha_max >> 1)) / (int32_t)alpha_max;
                    int32_t g = back_g + ((fore_g - back_g) * (int32_t)alpha + (int32_t)(alpha_max >> 1)) / (int32_t)alpha_max;
                    int32_t b = back_b + ((fore_b - back_b) * (int32_t)alpha + (int32_t)(alpha_max >> 1)) / (int32_t)alpha_max;
                    raw = cc->convert(((uint32_t)r << 16) | ((uint32_t)g << 8) | (uint32_t)b);
                }
                gfx->setRawColor(raw);
                gfx->writeFillRect(draw_x + x0, y + y0, x1 - x0, y1 - y0);
            }
        }
    }

    gfx->endWrite();
    return xAdvance;
}

static uint8_t get_lvgl_glyph_bpp(lv_font_glyph_format_t format) {
    switch (format) {
        case LV_FONT_GLYPH_FORMAT_A1:
        case LV_FONT_GLYPH_FORMAT_A1_ALIGNED:
            return 1;
        case LV_FONT_GLYPH_FORMAT_A2:
        case LV_FONT_GLYPH_FORMAT_A2_ALIGNED:
            return 2;
        case LV_FONT_GLYPH_FORMAT_A4:
        case LV_FONT_GLYPH_FORMAT_A4_ALIGNED:
            return 4;
        case LV_FONT_GLYPH_FORMAT_A8:
        case LV_FONT_GLYPH_FORMAT_A8_ALIGNED:
            return 8;
        default:
            return 0;
    }
}

static bool is_lvgl_glyph_byte_aligned(lv_font_glyph_format_t format) {
    switch (format) {
        case LV_FONT_GLYPH_FORMAT_A1_ALIGNED:
        case LV_FONT_GLYPH_FORMAT_A2_ALIGNED:
        case LV_FONT_GLYPH_FORMAT_A4_ALIGNED:
        case LV_FONT_GLYPH_FORMAT_A8_ALIGNED:
            return true;
        default:
            return false;
    }
}

static bool unpack_lvgl_raw_bitmap(const uint8_t *raw,
    lv_font_glyph_format_t format,
    uint32_t box_w,
    uint32_t box_h,
    std::vector < uint8_t > &out) {
    uint8_t bpp = get_lvgl_glyph_bpp(format);
    if (raw == nullptr || bpp == 0 || box_w == 0 || box_h == 0) {
        return false;
    }

    out.assign(box_w * box_h, 0);
    bool byte_aligned = is_lvgl_glyph_byte_aligned(format);
    uint32_t bit_pos = 0;
    uint32_t mask = (1U << bpp) - 1U;

    for (uint32_t py = 0; py < box_h; ++py) {
        if (byte_aligned && (bit_pos & 7U)) {
            bit_pos = (bit_pos + 7U) & ~7U;
        }

        for (uint32_t px = 0; px < box_w; ++px) {
            uint32_t byte_index = bit_pos >> 3;
            uint8_t bit_offset = bit_pos & 7U;
            uint8_t value;

            if (bpp == 8) {
                value = raw[byte_index];
            } else {
                uint8_t shift = 8U - bpp - bit_offset;
                value = (raw[byte_index] >> shift) & mask;
            }

            uint32_t max_value = mask;
            out[py * box_w + px] = max_value ? ((uint32_t)value * 255U + (max_value >> 1)) / max_value : 0;
            bit_pos += bpp;
        }
    }

    return true;
}

size_t M5LvglFont::drawChar(lgfx::LGFXBase *gfx, int32_t x, int32_t y, uint16_t uniCode,
    const lgfx::TextStyle *style, lgfx::FontMetrics *metrics,
    int32_t &filled_x) const {
    if (_font == nullptr || _font->get_glyph_dsc == nullptr || _font->get_glyph_bitmap == nullptr) {
        return drawCharDummy(gfx, x, y, metrics->x_advance, metrics->height, style, filled_x);
    }

    int32_t sy = 65536 * style->size_y;
    int32_t sx = 65536 * style->size_x;
    y += (metrics->y_offset * sy) >> 16;

    lv_font_glyph_dsc_t gd;
    if (!_font->get_glyph_dsc(_font, &gd, uniCode, 0)) {
        return drawCharDummy(gfx, x, y, metrics->x_advance, metrics->height, style, filled_x);
    }

    int32_t adv_px = gd.adv_w;
    int32_t xAdvance = (adv_px * sx) >> 16;
    int32_t xoffset = (gd.ofs_x * sx) >> 16;

    if (gd.box_w == 0 || gd.box_h == 0) {
        bool fillbg = (style->back_rgb888 != style->fore_rgb888);
        if (fillbg) {
            int32_t left = std::max < int > (filled_x, x);
            int32_t right = x + xAdvance;
            if (left < right) {
                uint32_t col_back = gfx->getColorConverter()->convert(style->back_rgb888);
                gfx->startWrite();
                gfx->setRawColor(col_back);
                gfx->writeFillRect(left, y, right - left, (metrics->height * sy) >> 16);
                gfx->endWrite();
            }
            filled_x = right;
        }
        return xAdvance;
    }

    gd.req_raw_bitmap = 1;
    gd.resolved_font = _font;
    uint32_t glyph_stride = gd.box_w;
    std::vector < uint8_t > glyph_buf;
    lv_draw_buf_t draw_buf {};
    const void *bmp_res = _font->get_glyph_bitmap(&gd, &draw_buf);
    if (bmp_res == nullptr ||
        !unpack_lvgl_raw_bitmap(static_cast < const uint8_t * > (bmp_res), gd.format, gd.box_w, gd.box_h, glyph_buf)) {
        return drawCharDummy(gfx, x, y, metrics->x_advance, metrics->height, style, filled_x);
    }
    const uint8_t *bitmap = glyph_buf.data();

    int32_t yoffset = metrics->baseline - (gd.ofs_y + gd.box_h);
    return draw_alpha_bitmap_common(gfx, x, y, style, metrics, filled_x, xAdvance, xoffset,
        yoffset, gd.box_w, gd.box_h, bitmap, glyph_stride, 255U);
}
