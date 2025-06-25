# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
import lvgl as lv
import asyncio


class OutputTestPanel:
    def __init__(self, parent: lv.obj, pin: int, pos_x: int, pos_y: int):
        self._pin = pin
        self._is_on = False

        panel = lv.obj(parent)
        panel.remove_flag(lv.obj.FLAG.SCROLLABLE)
        panel.set_style_bg_color(lv.color_hex(0xE4E3E4), lv.PART.MAIN)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_radius(10, lv.PART.MAIN)
        panel.set_style_pad_all(0, lv.PART.MAIN)
        panel.align(lv.ALIGN.TOP_MID, pos_x, pos_y)
        panel.set_size(230, 62)

        label_io_num = lv.label(panel)
        label_io_num.align(lv.ALIGN.CENTER, -67, 0)
        label_io_num.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        label_io_num.set_style_text_color(lv.color_hex(0x262626), lv.PART.MAIN)
        label_io_num.set_text(f"G{pin}")

        self._btn_io_toggle = lv.button(panel)
        self._btn_io_toggle.align(lv.ALIGN.CENTER, 47, 0)
        self._btn_io_toggle.set_style_radius(6, lv.PART.MAIN)
        self._btn_io_toggle.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_io_toggle.set_size(114, 42)
        self._btn_io_toggle.add_event_cb(self._handle_toggle, lv.EVENT.CLICKED, None)

        self._label_btn = lv.label(self._btn_io_toggle)
        self._label_btn.align(lv.ALIGN.CENTER, 0, 0)
        self._label_btn.set_style_text_font(lv.font_montserrat_22, lv.PART.MAIN)

        self._update_btn_style()

        # Setup pin
        get_hal().gpio_deinit(self._pin)
        get_hal().gpio_init(self._pin, 1)
        get_hal().gpio_set_level(self._pin, False)

    def _update_btn_style(self):
        if self._is_on:
            self._btn_io_toggle.set_style_bg_color(lv.color_hex(0xFF5959), lv.PART.MAIN)
            self._label_btn.set_text("HIGH")
        else:
            self._btn_io_toggle.set_style_bg_color(lv.color_hex(0x58B358), lv.PART.MAIN)
            self._label_btn.set_text("LOW")

    def _handle_toggle(self, e: lv.event_t):
        self._is_on = not self._is_on
        self._update_btn_style()
        get_hal().gpio_set_level(self._pin, self._is_on)

    def cleanup(self):
        self._btn_io_toggle.delete()
        self._btn_io_toggle = None
        get_hal().gpio_deinit(self._pin)


class ExtPortPanel:
    _PINS = [49, 50, 0, 1, 54, 53]

    def __init__(self, parent: lv.obj):
        panel = lv.obj(parent)
        panel.set_size(273, 460)
        panel.align(lv.ALIGN.CENTER, -321, 0)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        panel.set_style_radius(10, lv.PART.MAIN)

        label_title = lv.label(panel)
        label_title.align(lv.ALIGN.TOP_MID, 0, 0)
        label_title.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        label_title.set_text("Ext.Port1")

        self._test_panels = []
        for i, pin in enumerate(self._PINS):
            self._test_panels.append(OutputTestPanel(panel, pin, 0, 40 + 81 * i))

    def cleanup(self):
        for panel in self._test_panels:
            panel.cleanup()
        self._test_panels = []


class MbusPanel:
    _PINS = [18, 19, 5, 38, 7, 3, 2, 47, 16, 17, 45, 52, 37, 6, 4, 48, 35, 51]

    def __init__(self, parent: lv.obj):
        panel = lv.obj(parent)
        panel.set_size(520, 460)
        panel.align(lv.ALIGN.CENTER, 230, 0)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        panel.set_style_radius(10, lv.PART.MAIN)

        label_title = lv.label(panel)
        label_title.align(lv.ALIGN.TOP_MID, 0, 0)
        label_title.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        label_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        label_title.set_text("MBUS")

        self._test_panels = []
        for i, pin in enumerate(self._PINS):
            self._test_panels.append(
                OutputTestPanel(panel, pin, 124 if i > 8 else -124, 40 + 81 * (i % 9))
            )

    def cleanup(self):
        for panel in self._test_panels:
            panel.cleanup()
        self._test_panels = []


class AppGpio(AppBase):
    async def main(self):
        self._panel_ext = ExtPortPanel(self.get_app_panel())
        self._panel_mbus = MbusPanel(self.get_app_panel())

    def on_cleanup(self):
        self._panel_ext.cleanup()
        self._panel_mbus.cleanup()
