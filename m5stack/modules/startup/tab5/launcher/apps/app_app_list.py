# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
import lvgl as lv
import asyncio


class PyAppOption:
    def __init__(self, parent: lv.obj, py_app_name: str, pos_y: int, on_clicked):
        self._py_app_name = py_app_name
        self._on_clicked = on_clicked

        self._btn = lv.button(parent)
        self._btn.set_size(740, 54)
        self._btn.align(lv.ALIGN.TOP_MID, 0, pos_y)
        self._btn.set_style_bg_color(lv.color_hex(0xEDEDED), lv.PART.MAIN)
        self._btn.set_style_radius(10, lv.PART.MAIN)
        self._btn.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn.set_style_border_color(lv.color_hex(0x119FE6), lv.PART.MAIN)
        self._btn.set_style_border_width(3, lv.PART.MAIN)
        self._btn.add_event_cb(self._on_btn_clicked, lv.EVENT.CLICKED, None)

        self._label = lv.label(self._btn)
        self._label.set_text(py_app_name)
        self._label.align(lv.ALIGN.LEFT_MID, 0, 0)
        self._label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        self._label.set_style_text_color(lv.color_hex(0x4A4A4A), lv.PART.MAIN)

        self.reset_border()

    def reset_border(self):
        self._btn.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN)

    def get_py_app_name(self) -> str:
        return self._py_app_name

    def _on_btn_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._on_clicked:
            self._on_clicked(self._py_app_name)
        self._btn.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)

    def cleanup(self):
        self._label.delete()
        self._label = None
        self._btn.delete()
        self._btn = None


class AppAppList(AppBase):
    async def main(self):
        self._selected_option = None

        self._btn_run_once = lv.button(self.get_app_panel())
        self._btn_run_once.set_size(200, 150)
        self._btn_run_once.align(lv.ALIGN.TOP_RIGHT, -45, 100)
        self._btn_run_once.set_style_bg_color(lv.color_hex(0x119FE6), lv.PART.MAIN)
        self._btn_run_once.set_style_radius(10, lv.PART.MAIN)
        self._btn_run_once.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_run_once.add_event_cb(self._on_run_once_clicked, lv.EVENT.CLICKED, None)

        self._label_run_once = lv.label(self._btn_run_once)
        self._label_run_once.set_text("RUN ONCE")
        self._label_run_once.set_align(lv.ALIGN.CENTER)
        self._label_run_once.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        self._btn_run_always = lv.button(self.get_app_panel())
        self._btn_run_always.set_size(200, 150)
        self._btn_run_always.align(lv.ALIGN.TOP_RIGHT, -45, 310)
        self._btn_run_always.set_style_bg_color(lv.color_hex(0xF1677B), lv.PART.MAIN)
        self._btn_run_always.set_style_radius(10, lv.PART.MAIN)
        self._btn_run_always.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_run_always.add_event_cb(self._on_run_always_clicked, lv.EVENT.CLICKED, None)

        self._label_run_always = lv.label(self._btn_run_always)
        self._label_run_always.set_text("RUN ALWAYS")
        self._label_run_always.set_align(lv.ALIGN.CENTER)
        self._label_run_always.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        self._py_app_panel = lv.obj(self.get_app_panel())
        self._py_app_panel.set_size(800, 440)
        self._py_app_panel.align(lv.ALIGN.LEFT_MID, 30, 0)
        self._py_app_panel.set_style_radius(10, lv.PART.MAIN)
        self._py_app_panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._py_app_panel.set_style_border_width(0, lv.PART.MAIN)

        self._app_options = []
        for i, app_name in enumerate(get_hal().get_py_app_list()):
            self._app_options.append(
                PyAppOption(
                    self._py_app_panel,
                    app_name,
                    10 + i * 70,
                    self._on_py_app_option_clicked,
                )
            )

    def _on_py_app_option_clicked(self, py_app_name: str):
        if self._selected_option:
            self._selected_option.reset_border()
        self._selected_option = next(
            option for option in self._app_options if option.get_py_app_name() == py_app_name
        )

    def _on_run_once_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._selected_option:
            get_hal().run_py_app(self._selected_option.get_py_app_name(), True)

    def _on_run_always_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._selected_option:
            get_hal().run_py_app(self._selected_option.get_py_app_name(), False)

    def on_cleanup(self):
        self._label_run_once.delete()
        self._label_run_once = None
        self._btn_run_once.delete()
        self._btn_run_once = None

        self._label_run_always.delete()
        self._label_run_always = None
        self._btn_run_always.delete()
        self._btn_run_always = None

        for option in self._app_options:
            option.cleanup()
        self._app_options.clear()

        self._py_app_panel.delete()
        self._py_app_panel = None
