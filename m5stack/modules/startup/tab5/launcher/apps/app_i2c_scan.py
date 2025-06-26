# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import get_hal
import lvgl as lv
import asyncio


class AppI2cScan(AppBase):
    async def main(self):
        get_hal().i2c_init()

        img_panel_port_a = lv.image(self.get_app_panel())
        img_panel_port_a.set_src(get_hal().get_asset_path("utils/i2c_panel_port_a.png"))
        img_panel_port_a.align(lv.ALIGN.CENTER, -279, 34)

        # img_panel_internal = lv.image(self.get_app_panel())
        # img_panel_internal.set_src(get_hal().get_asset_path("utils/i2c_panel_internal.png"))
        # img_panel_internal.align(lv.ALIGN.CENTER, 279, 34)

        btn_scan_port_a = lv.button(self.get_app_panel())
        btn_scan_port_a.set_size(260, 54)
        btn_scan_port_a.align(lv.ALIGN.CENTER, -279, -158)
        btn_scan_port_a.set_style_bg_color(lv.color_hex(0xFD909F), lv.PART.MAIN)
        btn_scan_port_a.set_style_shadow_width(0, lv.PART.MAIN)
        btn_scan_port_a.add_event_cb(self._handle_scan_port_a, lv.EVENT.CLICKED, None)

        btn_label_port_a = lv.label(btn_scan_port_a)
        btn_label_port_a.set_text("SCAN  PORT.A")
        btn_label_port_a.align(lv.ALIGN.CENTER, 0, 0)
        btn_label_port_a.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        btn_label_port_a.set_style_text_color(lv.color_hex(0x373737), lv.PART.MAIN)

        # btn_scan_internal = lv.button(self.get_app_panel())
        # btn_scan_internal.set_size(260, 54)
        # btn_scan_internal.align(lv.ALIGN.CENTER, 279, -158)
        # btn_scan_internal.set_style_bg_color(lv.color_hex(0xFFD733), lv.PART.MAIN)
        # btn_scan_internal.set_style_shadow_width(0, lv.PART.MAIN)
        # btn_scan_internal.add_event_cb(self._handle_scan_internal, lv.EVENT.CLICKED, None)

        # btn_label_internal = lv.label(btn_scan_internal)
        # btn_label_internal.set_text("SCAN  INTERNAL")
        # btn_label_internal.align(lv.ALIGN.CENTER, 0, 0)
        # btn_label_internal.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        # btn_label_internal.set_style_text_color(lv.color_hex(0x373737), lv.PART.MAIN)

        self._addr_labels_port_a: list[lv.label] = []
        self._addr_labels_internal: list[lv.label] = []

        self._update_internal = False
        self._update_port_a = False

        while True:
            await asyncio.sleep_ms(100)
            if self._update_internal:
                self._update_addr_labels(0, get_hal().i2c_scan(0))
                self._update_internal = False
            if self._update_port_a:
                self._update_addr_labels(1, get_hal().i2c_scan(1))
                self._update_port_a = False

    def _handle_scan_port_a(self, e: lv.event_t):
        get_hal().play_click_sfx()
        self._update_port_a = True

    def _handle_scan_internal(self, e: lv.event_t):
        get_hal().play_click_sfx()
        self._update_internal = True

    def _clear_addr_labels_port_a(self):
        for label in self._addr_labels_port_a:
            label.delete()
        self._addr_labels_port_a.clear()

    def _clear_addr_labels_internal(self):
        for label in self._addr_labels_internal:
            label.delete()
        self._addr_labels_internal.clear()

    def _update_addr_labels(self, port: int, scan_result: list[int]):
        """port: 0 for internal, 1 for port A"""

        if port == 0:
            self._clear_addr_labels_internal()
        else:
            self._clear_addr_labels_port_a()

        for addr in scan_result:
            label = lv.label(self.get_app_panel())
            label.set_text(f"{addr:02X}")
            label.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
            label.set_style_text_color(lv.color_hex(0x352B2A), lv.PART.MAIN)

            row = addr >> 4
            col = addr & 0x0F
            x = col * 27
            if port == 0:
                x = x + 100
            else:
                x = x - 458
            y = row * 27 - 39
            label.align(lv.ALIGN.CENTER, int(x), int(y))

            if port == 0:
                self._addr_labels_internal.append(label)
            else:
                self._addr_labels_port_a.append(label)

    def on_cleanup(self):
        get_hal().i2c_deinit()

        self._clear_addr_labels_port_a()
        self._clear_addr_labels_internal()
