# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import layout
import M5
import widgets
import asyncio
import binascii
from startup import print_access_info
import machine


try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class NetworkStatus:
    INIT = 0
    RSSI_GOOD = 1
    RSSI_MID = 2
    RSSI_WORSE = 3
    DISCONNECTED = 4


class CloudStatus:
    INIT = 0
    CONNECTED = 1
    DISCONNECTED = 2


class DevApp(app_base.AppBase):
    BACKGROUND = "flow.png"

    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wifi = data
        super().__init__()

    def on_install(self):
        tab_x = 470 if layout.IS_PAPERMONO else 493
        tab_w = 100 if layout.IS_PAPERMONO else 48
        self.descriptor = app_base.Descriptor(
            x=layout.x(tab_x),
            y=layout.y(1),
            w=layout.size(tab_w),
            h=layout.size(181),
        )

    def on_launch(self):
        self._mac_text = self._get_mac()
        self._state_text = self._get_state()
        self._nick_name_text = self._get_nick_name()
        self._access_code_text = self._get_access_code()

    def on_view(self):
        layout.draw_background(layout.resource_path(self.BACKGROUND))
        field_width = layout.size(349 if layout.IS_PAPERMONO else 360)
        field_height = layout.size(46 if layout.IS_PAPERMONO else 50)

        self._state_label = widgets.Label(
            "------",
            layout.x(89),
            layout.y(452),
            w=field_width,
            h=field_height,
            fg_color=0x000000,
            bg_color=layout.DYNAMIC_BG_COLOR,
            font=layout.large_font(),
            parent=self._lcd,
        )
        self._state_label.set_text(self._state_text)

        self._mac_label = widgets.Label(
            "aabbcc112233",
            layout.x(89),
            layout.y(572),
            w=field_width,
            h=field_height,
            fg_color=0x000000,
            bg_color=layout.DYNAMIC_BG_COLOR,
            font=layout.large_font(),
            parent=self._lcd,
        )
        self._mac_label.set_text(self._mac_text)

        self._nick_name_label = widgets.Label(
            "XXABC",
            layout.x(89),
            layout.y(812),
            w=field_width,
            h=field_height,
            fg_color=0x000000,
            bg_color=layout.DYNAMIC_BG_COLOR,
            font=layout.large_font(),
            parent=self._lcd,
        )
        self._nick_name_label.set_long_mode(self._nick_name_label.LONG_DOT)
        self._nick_name_label.set_text(self._nick_name_text)

        self._access_code_label = widgets.Label(
            "------",
            layout.x(89),
            layout.y(692),
            w=field_width,
            h=field_height,
            fg_color=0x000000,
            bg_color=layout.DYNAMIC_BG_COLOR,
            font=layout.large_font(),
            parent=self._lcd,
        )
        self._access_code_label.set_long_mode(self._access_code_label.LONG_DOT)
        self._access_code_label.set_text(self._access_code_text)

    async def on_run(self):
        while True:
            state = self._get_state()
            access_code = self._get_access_code()
            nick_name = self._get_nick_name()
            state_changed = state != self._state_text
            access_code_changed = access_code != self._access_code_text
            nick_name_changed = nick_name != self._nick_name_text

            if state_changed or access_code_changed or nick_name_changed:
                layout.begin_full_refresh()
                try:
                    if state_changed:
                        self._state_text = state
                        self._state_label.set_text(state)
                    if access_code_changed:
                        self._access_code_text = access_code
                        self._access_code_label.set_text(access_code)
                    if nick_name_changed:
                        self._nick_name_text = nick_name
                        self._nick_name_label.set_text(nick_name)
                finally:
                    layout.end_full_refresh()

            if access_code_changed or nick_name_changed:
                print_access_info(self._nick_name_text, self._access_code_text)
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        del self._state_label, self._mac_label, self._nick_name_label, self._access_code_label

    async def _click_event_handler(self, x, y, fw):
        pass

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

    @staticmethod
    def _get_state():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return "ONLINE"
            except Exception:
                pass
        return "OFFLINE"

    @staticmethod
    def _get_nick_name():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_access_code():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""
