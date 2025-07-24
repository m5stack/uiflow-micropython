# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..common import Ezdata, debug_print
from ..hal import get_hal
import lvgl as lv
import asyncio
import requests
import time
import os


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


class WidgetImage:
    _panel: lv.obj | None = None
    _img: lv.image | None = None
    _is_maximized: bool = False

    @staticmethod
    def is_maximized():
        return WidgetImage._is_maximized

    @staticmethod
    def create(img_src: str):
        WidgetImage.destroy()

        WidgetImage._panel = lv.obj(lv.screen_active())
        WidgetImage._apply_size_style()
        WidgetImage._panel.set_style_border_width(0, lv.PART.MAIN)
        WidgetImage._panel.set_style_pad_all(0, lv.PART.MAIN)
        WidgetImage._panel.set_style_radius(0, lv.PART.MAIN)
        WidgetImage._panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.ACTIVE)
        WidgetImage._panel.add_event_cb(WidgetImage._handle_on_click, lv.EVENT.CLICKED, None)

        WidgetImage._img = lv.image(WidgetImage._panel)
        WidgetImage._img.set_src(img_src)
        WidgetImage._img.align(lv.ALIGN.CENTER, 0, 0)

    @staticmethod
    def _apply_size_style():
        if WidgetImage._is_maximized:
            WidgetImage._panel.set_size(1280, 720)
            WidgetImage._panel.align(lv.ALIGN.CENTER, 0, 0)
            WidgetImage._panel.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        else:
            WidgetImage._panel.set_size(1100, 430)
            WidgetImage._panel.align(lv.ALIGN.TOP_LEFT, 35, 181)
            WidgetImage._panel.set_style_bg_color(lv.color_hex(0xF6F6F6), lv.PART.MAIN)

    @staticmethod
    def destroy():
        if WidgetImage._img:
            WidgetImage._img.delete()
            WidgetImage._img = None
        if WidgetImage._panel:
            WidgetImage._panel.delete()
            WidgetImage._panel = None

    @staticmethod
    def _handle_on_click(e: lv.event_t):
        get_hal().play_click_sfx()
        WidgetImage._is_maximized = not WidgetImage._is_maximized
        WidgetImage._apply_size_style()


class ViewFile(ViewBase):
    class _FileType:
        UNSUPPORTED = 0
        PNG = 1
        JPG = 2

    def __init__(self, parent: lv.obj, data: dict):
        super().__init__(parent, data)

        self._parent = parent
        self._url = data.get("value")
        self._temp_path = None

        label_link = lv.label(parent)
        label_link.set_text("URL: " + str(data.get("value")))
        label_link.align(lv.ALIGN.LEFT_MID, 20, 226)
        label_link.set_style_text_color(lv.color_hex(0x9EA4B5), lv.PART.MAIN)
        label_link.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
        label_link.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

        file_type = self._get_file_type(self._url)
        if file_type == self._FileType.UNSUPPORTED:
            self._handle_type_unsupported()
        elif file_type == self._FileType.PNG:
            self._handle_type_png()
        elif file_type == self._FileType.JPG:
            self._handle_type_jpg()

    def _get_file_type(self, file_name: str) -> _FileType:
        if file_name.endswith(".png"):
            return self._FileType.PNG
        elif file_name.endswith(".jpg"):
            return self._FileType.JPG
        elif file_name.endswith(".jpeg"):
            return self._FileType.JPG
        else:
            return self._FileType.UNSUPPORTED

    def _handle_type_unsupported(self):
        self._handle_error("Unsupported file type\nCurrent supported file types: PNG, JPG")

    def _handle_type_png(self):
        self._handle_type_image()

    def _handle_type_jpg(self):
        self._handle_type_image()

    def _handle_type_image(self):
        url = self._url
        try:

            def get_file_name(url: str) -> str:
                if "." in url:
                    suffix = "." + url.split(".")[-1].split("?")[0]
                else:
                    raise Exception("Invalid file name")
                return "ezdata_img" + suffix

            def download_image(file_name: str):
                get_hal().create_temp_dir()

                temp_path = get_hal().get_os_temp_file_path(file_name)

                debug_print(f"temp_path: {temp_path}")

                # Get image from url
                resp = requests.get(url, timeout=10)
                if resp.status_code != 200:
                    raise Exception(f"HTTP {resp.status_code}")

                # Write image to file
                with open(temp_path, "wb") as f:
                    f.write(resp.content)

                self._temp_path = temp_path

            def create_image(file_name: str):
                path = get_hal().get_lvgl_temp_file_path(file_name)

                # Due to the same image path will be cached, cache drop is needed
                lv.image.cache_drop(path)

                WidgetImage.create(path)

            file_name = get_file_name(url)
            download_image(file_name)
            create_image(file_name)

        except Exception as e:
            self._handle_error(f"Image loading failed:\n{e}")

    def _handle_error(self, error_msg: str):
        label = lv.label(self._parent)
        label.set_text(error_msg)
        label.align(lv.ALIGN.CENTER, 0, -32)
        label.set_style_text_color(lv.color_hex(0x272F43), lv.PART.MAIN)
        label.set_style_text_font(lv.font_montserrat_30, lv.PART.MAIN)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    def cleanup(self):
        WidgetImage.destroy()
        if self._temp_path:
            os.remove(self._temp_path)
        super().cleanup()


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
        # print("data:", data)

        if isinstance(value, str):
            if data.get("dataType") == "file":
                self._view = ViewFile(self.get_app_panel(), data)
            else:
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
