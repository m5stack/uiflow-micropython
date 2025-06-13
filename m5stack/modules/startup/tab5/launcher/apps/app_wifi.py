# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
import lvgl as lv
import asyncio


COLOR_TEXT_AREA_BG = 0xE6E2E6
COLOR_LABEL = 0x038FD5
COLOR_BTN_BG = 0x1DA4E7

TEXT_AREA_CONFIG = [
    {"x": 30, "y": 40, "label": "WiFi SSID :"},
    {"x": 600, "y": 40, "label": "WiFi Password :"},
    {"x": 30, "y": 135, "label": "UIFlow Server :"},
]


class AppWifi(AppBase):
    async def main(self):
        self._network_config = get_hal().get_network_config()

        # Text areas
        self._text_areas: list[lv.textarea] = []
        self._labels: list[lv.label] = []
        for config in TEXT_AREA_CONFIG:
            self._text_areas.append(lv.textarea(self.get_app_panel()))
            self._text_areas[-1].align(lv.ALIGN.TOP_LEFT, config["x"], config["y"])
            self._text_areas[-1].set_width(500)
            self._text_areas[-1].set_one_line(True)
            self._text_areas[-1].set_style_border_width(0, lv.PART.MAIN)
            self._text_areas[-1].set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
            self._text_areas[-1].set_style_bg_color(lv.color_hex(COLOR_TEXT_AREA_BG), lv.PART.MAIN)
            self._text_areas[-1].add_event_cb(self._ta_event_cb, lv.EVENT.ALL, None)

            self._labels.append(lv.label(self.get_app_panel()))
            self._labels[-1].set_text(config["label"])
            self._labels[-1].align_to(self._text_areas[-1], lv.ALIGN.OUT_TOP_LEFT, 10, -15)
            self._labels[-1].set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
            self._labels[-1].set_style_text_color(lv.color_hex(COLOR_LABEL), lv.PART.MAIN)

        # Enable * for password
        self._text_areas[1].set_password_mode(True)

        # Create keyboard
        self._kb = lv.keyboard(self.get_app_panel())
        self._kb.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._kb.set_height(lv.pct(60))
        self._kb.add_event_cb(self._on_kb_clicked, lv.EVENT.CLICKED, None)

        # Create confirm button
        self._btn = lv.button(self.get_app_panel())
        self._btn.align(lv.ALIGN.TOP_LEFT, 890, 135)
        self._btn.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn.set_width(200)
        self._btn.set_style_bg_color(lv.color_hex(COLOR_BTN_BG), lv.PART.MAIN)
        self._btn.add_event_cb(self._on_confim, lv.EVENT.CLICKED, None)
        self._btn_label = lv.label(self._btn)
        self._btn_label.set_text("Save And Link")
        self._btn_label.set_align(lv.ALIGN.CENTER)
        self._btn_label.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)

        self._update_text_areas()

    def _update_text_areas(self):
        self._text_areas[0].set_text(self._network_config.ssid)
        self._text_areas[1].set_text(self._network_config.password)
        self._text_areas[2].set_text(self._network_config.server)

    def _ta_event_cb(self, e: lv.event_t):
        code = e.get_code()
        ta = e.get_target_obj()
        if code == lv.EVENT.CLICKED or code == lv.EVENT.FOCUSED:
            # Remove border from all textareas first
            for textarea in self._text_areas:
                textarea.set_style_border_width(0, lv.PART.MAIN)
            # Set keyboard to current textarea
            self._kb.set_textarea(ta)

    def _on_kb_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()

    def _on_confim(self, e: lv.event_t):
        get_hal().play_click_sfx()
        self._network_config.ssid = self._text_areas[0].get_text()
        self._network_config.password = self._text_areas[1].get_text()
        self._network_config.server = self._text_areas[2].get_text()
        get_hal().set_network_config(self._network_config)

    def on_cleanup(self):
        for ta in self._text_areas:
            ta.delete()
        self._text_areas.clear()

        for label in self._labels:
            label.delete()
        self._labels.clear()

        self._kb.delete()
        self._kb = None

        self._btn_label.delete()
        self._btn_label = None

        self._btn.delete()
        self._btn = None
