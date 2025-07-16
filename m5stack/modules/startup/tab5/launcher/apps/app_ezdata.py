# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..common import Ezdata, debug_print
import lvgl as lv
import asyncio
import time


class ViewBase:
    def __init__(self, parent: lv.obj, data: dict):
        self._parent = parent

        self._data_update_time = data.get("updateTime")
        self._data_update_time = float(self._data_update_time) / 1000  # Convert to seconds

        self._label_last_update_time: lv.obj | None = None
        self._create_last_update_time_label()
        self._update_last_update_time()

    def cleanup(self):
        self._label_last_update_time = None

    def update(self):
        self._update_last_update_time()

    def _get_time_since_last_update(self, data_update_time: float):
        try:
            now = time.time()
            diff = int(now - data_update_time)

            if diff >= 3600:
                return "{}H".format(min(diff // 3600, 99))
            elif diff >= 60:
                return "{}Min".format(min(diff // 60, 99))
            else:
                return "{}Sec".format(min(diff, 99))
        except Exception as e:
            print(e)
            return ""

    def _create_last_update_time_label(self):
        self._label_last_update_time = lv.label(self._parent)
        self._label_last_update_time.align(lv.ALIGN.CENTER, 520, 226)
        self._label_last_update_time.set_style_text_color(lv.color_hex(0x9EA4B5), lv.PART.MAIN)
        self._label_last_update_time.set_style_text_font(lv.font_montserrat_22, lv.PART.MAIN)
        self._label_last_update_time.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    def _update_last_update_time(self):
        if self._label_last_update_time:
            self._label_last_update_time.set_text(
                self._get_time_since_last_update(self._data_update_time)
            )


class ViewString(ViewBase):
    def __init__(self, parent: lv.obj, data: dict):
        super().__init__(parent, data)

        label = lv.label(parent)
        label.set_text(str(data.get("value")))
        label.align(lv.ALIGN.CENTER, 0, -10)
        label.set_style_text_color(lv.color_hex(0x272F43), lv.PART.MAIN)
        label.set_style_text_font(lv.font_montserrat_30, lv.PART.MAIN)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


class ViewNumber(ViewBase):
    def __init__(self, parent: lv.obj, data: dict):
        super().__init__(parent, data)

        label = lv.label(parent)
        label.set_text(str(data.get("value")))
        label.align(lv.ALIGN.CENTER, 0, -10)
        label.set_style_text_color(lv.color_hex(0x272F43), lv.PART.MAIN)
        label.set_style_text_font(lv.font_montserrat_30, lv.PART.MAIN)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


class ViewArray(ViewBase):
    class _Item:
        def __init__(self, parent: lv.obj, data: str, pos_y: int):
            panel = lv.obj(parent)
            panel.set_size(1044, 55)
            panel.align(lv.ALIGN.TOP_LEFT, 0, pos_y)
            panel.set_style_radius(16, lv.PART.MAIN)
            panel.set_style_bg_color(lv.color_hex(0xE0EDFF), lv.PART.MAIN)
            panel.set_style_border_width(0, lv.PART.MAIN)
            panel.set_style_pad_all(0, lv.PART.MAIN)

            label = lv.label(panel)
            label.set_text(data)
            label.align(lv.ALIGN.LEFT_MID, 34, 0)
            label.set_style_text_color(lv.color_hex(0x272F43), lv.PART.MAIN)
            label.set_style_text_font(lv.font_montserrat_30, lv.PART.MAIN)

    def __init__(self, parent: lv.obj, data: list):
        super().__init__(parent, data)

        panel = lv.obj(parent)
        panel.set_size(1092, 429)
        panel.align(lv.ALIGN.CENTER, 0, -20)
        panel.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_pad_all(0, lv.PART.MAIN)
        panel.set_style_pad_left(24, lv.PART.MAIN)
        panel.set_style_pad_top(28, lv.PART.MAIN)

        data_array = data.get("value")
        for i, item in enumerate(data_array):
            self._Item(panel, str(item), i * 84)


class ViewDict(ViewBase):
    class _Item:
        def __init__(self, parent: lv.obj, data: str, pos_y: int):
            panel = lv.obj(parent)
            panel.set_size(1044, 55)
            panel.align(lv.ALIGN.TOP_LEFT, 0, pos_y)
            panel.set_style_radius(16, lv.PART.MAIN)
            panel.set_style_bg_color(lv.color_hex(0xE0EDFF), lv.PART.MAIN)
            panel.set_style_border_width(0, lv.PART.MAIN)
            panel.set_style_pad_all(0, lv.PART.MAIN)

            label = lv.label(panel)
            label.set_text(data)
            label.align(lv.ALIGN.LEFT_MID, 34, 0)
            label.set_style_text_color(lv.color_hex(0x272F43), lv.PART.MAIN)
            label.set_style_text_font(lv.font_montserrat_30, lv.PART.MAIN)

    def __init__(self, parent: lv.obj, data: dict):
        super().__init__(parent, data)

        panel = lv.obj(parent)
        panel.set_size(1092, 429)
        panel.align(lv.ALIGN.CENTER, 0, -20)
        panel.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_pad_all(0, lv.PART.MAIN)
        panel.set_style_pad_left(24, lv.PART.MAIN)
        panel.set_style_pad_top(28, lv.PART.MAIN)

        data_dict = data.get("value")
        for i, (key, value) in enumerate(data_dict.items()):
            self._Item(panel, f"{str(key)}:  {str(value)}", i * 84)


class AppEzdata(AppBase):
    async def main(self):
        self._view = None

        self._create_view()
        Ezdata.on_selected_data_changed.connect(self._handle_data_changed)

        while True:
            await asyncio.sleep(10)
            if self._view:
                self._view.update()

    def on_cleanup(self):
        Ezdata.on_selected_data_changed.disconnect(self._handle_data_changed)
        self._destroy_view()

    def _destroy_view(self):
        if self._view:
            self._view.cleanup()
            self._view = None
        self.get_app_panel().clean()

    def _create_view(self):
        self._destroy_view()

        data = Ezdata.get_selected_data()
        value = data.get("value")

        if isinstance(value, str):
            self._view = ViewString(self.get_app_panel(), data)
        elif isinstance(value, int) or isinstance(value, float):
            self._view = ViewNumber(self.get_app_panel(), data)
        elif isinstance(value, list):
            self._view = ViewArray(self.get_app_panel(), data)
        elif isinstance(value, dict):
            self._view = ViewDict(self.get_app_panel(), data)
        else:
            print("unsupported data type:", type(value))

    def _handle_data_changed(self):
        debug_print("data changed")
        self._create_view()
