# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
from ..common import *
import lvgl as lv
import asyncio
import time


class ViewBase:
    def cleanup(self):
        pass


class ViewInit(ViewBase):
    """View for nothing when ezdata is initializing"""

    def __init__(self, parent: lv.obj):
        label = lv.label(parent)
        label.set_text("EzData Initializing...")
        label.align(lv.ALIGN.CENTER, 0, -0)
        label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)


class ViewWaitUserToken(ViewBase):
    """View for no user token, display qrcode and tips"""

    def __init__(self, parent: lv.obj, qrcode_data: str):
        qr_add = lv.qrcode(parent)
        qr_add.align(lv.ALIGN.CENTER, -167, -62)
        qr_add.set_size(280)
        qr_add.set_dark_color(lv.color_hex(0x0075B0))
        qr_add.update(qrcode_data, len(qrcode_data))

        label_qr_add = lv.label(parent)
        label_qr_add.set_text('Scan with the "Ez Data" app to begin.')
        label_qr_add.align(lv.ALIGN.CENTER, -167, 127)
        label_qr_add.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        install_url = "https://apps.apple.com/us/app/ezdata/id6738713869"
        qr_install = lv.qrcode(parent)
        qr_install.align(lv.ALIGN.CENTER, 413, -46)
        qr_install.set_size(170)
        qr_install.set_dark_color(lv.color_hex(0x0075B0))
        qr_install.update(install_url, len(install_url))

        label_qr_install = lv.label(parent)
        label_qr_install.set_width(300)
        label_qr_install.set_text('Install "Ez Data" from App Store')
        label_qr_install.align(lv.ALIGN.CENTER, 413, 110)
        label_qr_install.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        label_qr_install.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

        divider = lv.obj(parent)
        divider.set_size(6, 345)
        divider.set_style_border_width(0, lv.PART.MAIN)
        divider.align(lv.ALIGN.CENTER, 249, 0)
        divider.set_style_radius(2, lv.PART.MAIN)
        divider.set_style_bg_color(lv.color_hex(0xE5E5E5), lv.PART.MAIN)


class DataItem:
    """Item class to render a data key-value pair"""

    def __init__(self, parent: lv.obj, data, pos_x: int, pos_y: int):
        # Transparent container for easier position handle
        container = lv.obj(parent)
        container.set_size(140, 210)
        container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        container.set_style_border_width(0, lv.PART.MAIN)
        container.remove_flag(lv.obj.FLAG.SCROLLABLE)
        container.align(lv.ALIGN.TOP_LEFT, pos_x, pos_y)

        panel = lv.obj(container)
        panel.align(lv.ALIGN.CENTER, 0, -20)
        panel.set_size(140, 170)
        panel.set_style_radius(18, lv.PART.MAIN)
        panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        panel.remove_flag(lv.obj.FLAG.SCROLLABLE)

        value_panel = lv.obj(panel)
        value_panel.set_size(120, 110)
        value_panel.align(lv.ALIGN.CENTER, 0, -12)
        value_panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        value_panel.set_style_border_width(0, lv.PART.MAIN)
        value_panel.set_scroll_dir(lv.DIR.VER)

        label_value = lv.label(value_panel)
        label_value.set_width(100)
        label_value.align(lv.ALIGN.CENTER, 0, 0)
        label_value.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        label_value.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

        if not self._check_data_valid(data):
            label_value.set_text("Invalid data")
            return

        self._label_last_update = lv.label(panel)
        self._label_last_update.align(lv.ALIGN.CENTER, 0, 60)
        self._label_last_update.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_last_update.set_style_text_color(lv.color_hex(0x6E6E6E), lv.PART.MAIN)

        label_name = lv.label(container)
        label_name.align(lv.ALIGN.CENTER, 0, 88)
        label_name.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)

        # Apply texts
        label_value.set_text(str(data.get("value")))
        label_name.set_text(data.get("alias"))
        self._update_time = data.get("updateTime")
        self.update_update_time()

    def _check_data_valid(self, data) -> bool:
        if not data:
            return False
        keys = ["alias", "value", "updateTime", "valueType"]
        for key in keys:
            if key not in data:
                return False
        return True

    def _get_time_since_last_update(self, last_update_str):
        try:
            year, month, day = (
                int(last_update_str[0:4]),
                int(last_update_str[5:7]),
                int(last_update_str[8:10]),
            )
            hour, minute, second = (
                int(last_update_str[11:13]),
                int(last_update_str[14:16]),
                int(last_update_str[17:19]),
            )
            last_time = time.mktime((year, month, day, hour, minute, second, 0, 0))

            now = time.time()
            diff = int(now - last_time)

            if diff >= 3600:
                return "{}H".format(min(diff // 3600, 99))
            elif diff >= 60:
                return "{}Min".format(min(diff // 60, 99))
            else:
                return "{}Sec".format(min(diff, 99))
        except Exception as e:
            print(e)
            return ""

    def update_update_time(self):
        self._label_last_update.set_text(self._get_time_since_last_update(self._update_time))

    def cleanup(self):
        self._label_last_update = None


class ViewData(ViewBase):
    """View for a data group, render key-value pairs by api json response"""

    def __init__(self, parent: lv.obj):
        self._parent = parent
        self._last_data = None
        self._data_items = []

    def update(self, data):
        if self._last_data == data:
            return

        self._create_data_items(data)
        self._last_data = data

    def update_data_update_time(self):
        for item in self._data_items:
            item.update_update_time()

    def _create_data_items(self, data):
        # Clean up old items
        for item in self._data_items:
            item.cleanup()
        self._data_items.clear()
        self._parent.clean()

        # Create new items
        start_x, start_y = 56, 30
        offset_x, offset_y = 220, 237
        items_per_row = 5
        for i, item in enumerate(data):
            row = i // items_per_row
            col = i % items_per_row
            x = start_x + col * offset_x
            y = start_y + row * offset_y
            self._data_items.append(DataItem(self._parent, item, x, y))

    def cleanup(self):
        self._parent = None


class AppEzdata(AppBase):
    async def main(self):
        self._last_ezdata_state = None
        self._view = None
        self._last_update_time = 0
        self._last_data_update_time = 0

        while True:
            self._update_view()
            await asyncio.sleep(0.5)

    def _destroy_view(self):
        if self._view:
            self._view.cleanup()
            self._view = None
            self.get_app_panel().clean()

    def _update_view(self):
        # If state changed
        state = Ezdata.get_state()
        if state != self._last_ezdata_state:
            # Destroy old
            self._destroy_view()
            # Create new
            if state == Ezdata.State.INIT:
                self._view = ViewInit(self.get_app_panel())
            elif state == Ezdata.State.WAIT_USER_TOKEN:
                self._view = ViewWaitUserToken(self.get_app_panel(), Ezdata.get_add_user_qr_code())
            elif state == Ezdata.State.NORMAL:
                self._view = ViewData(self.get_app_panel())

            self._last_ezdata_state = state
            self._last_update_time = 0

        # If is data view, update data
        if isinstance(self._view, ViewData):
            go_refresh = False

            # If some thing changed, refresh data
            if EzdataAppState.needs_refresh():
                EzdataAppState.clear_needs_refresh()
                go_refresh = True

            # Auto refresh in every 10s
            if time.time() - self._last_update_time > 10:
                go_refresh = True

            if go_refresh:
                new_data = Ezdata.get_user_data_list(EzdataAppState.get_current_group_id())
                self._view.update(new_data)
                self._last_update_time = time.time()

            # Update data's last update time in every 10s
            if time.time() - self._last_data_update_time > 10:
                self._view.update_data_update_time()
                self._last_data_update_time = time.time()

    def on_cleanup(self):
        self._destroy_view()


class AppEzdataSettings(AppBase):
    async def main(self):
        btn_reset_ezdata = lv.button(self.get_app_panel())
        btn_reset_ezdata.align(lv.ALIGN.TOP_MID, -350, 80)
        btn_reset_ezdata.set_size(280, 42)
        btn_reset_ezdata.set_style_bg_color(lv.color_hex(0xF1677B), lv.PART.MAIN)
        btn_reset_ezdata.set_style_shadow_width(0, lv.PART.MAIN)
        btn_reset_ezdata.add_event_cb(
            self._handle_btn_reset_ezdata_clicked, lv.EVENT.CLICKED, None
        )

        label_reset_ezdata = lv.label(btn_reset_ezdata)
        label_reset_ezdata.set_align(lv.ALIGN.CENTER)
        label_reset_ezdata.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        label_reset_ezdata.set_text("Reset Ezdata")

    def _handle_btn_reset_ezdata_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        Ezdata.reset_user_token()
