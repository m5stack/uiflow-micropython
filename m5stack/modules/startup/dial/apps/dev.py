# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import M5
import widgets
import asyncio
import binascii
import esp32
import machine
import network
from .. import res
from . import status_bar
from startup import print_access_info

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


_PANEL_BG = 0xFEFEFE
_LABEL_COLOR = 0x00AA00
_VALUE_COLOR = 0x000000
_TITLE_FONT = "/system/common/font/Montserrat-Medium-18.vlw"
_LABEL_FONT = "/system/common/font/Montserrat-Medium-14.vlw"
_VALUE_FONT = "/system/common/font/Montserrat-Medium-16.vlw"
_CODE_FONT = "/system/common/font/Montserrat-Medium-18.vlw"


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
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._state = self._collect_state()
        self._bg_src = self._get_bg_src()

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 0
        self._bg_src = self._get_bg_src()

        self._draw_page_bg(self._bg_src)

        self._server_label = widgets.Label(
            "",
            120,
            82,
            w=220,
            h=20,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x008FD7,
            bg_color=_PANEL_BG,
            font=_LABEL_FONT,
        )
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)

        self._mac_title_label = widgets.Label(
            "Device MAC:",
            120,
            100,
            w=210,
            h=18,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_LABEL_COLOR,
            bg_color=_PANEL_BG,
            font=_LABEL_FONT,
        )

        self._mac_value_label = widgets.Label(
            "",
            120,
            117,
            w=210,
            h=20,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_VALUE_COLOR,
            bg_color=_PANEL_BG,
            font=_LABEL_FONT,
        )
        self._mac_value_label.set_long_mode(widgets.Label.LONG_DOT)

        self._nick_title_label = widgets.Label(
            "Nickname:",
            120,
            182,
            w=210,
            h=18,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_LABEL_COLOR,
            bg_color=_PANEL_BG,
            font=_LABEL_FONT,
        )

        self._nick_value_label = widgets.Label(
            "",
            120,
            199,
            w=190,
            h=20,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_VALUE_COLOR,
            bg_color=_PANEL_BG,
            font=_LABEL_FONT,
        )
        self._nick_value_label.set_long_mode(widgets.Label.LONG_DOT)

        self._access_label = widgets.Label(
            "Access code:",
            120,
            141,
            w=210,
            h=18,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_LABEL_COLOR,
            bg_color=_PANEL_BG,
            font=_LABEL_FONT,
        )

        self._code_value_label = widgets.Label(
            "",
            120,
            158,
            w=190,
            h=22,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_VALUE_COLOR,
            bg_color=_PANEL_BG,
            font=_VALUE_FONT,
        )
        self._code_value_label.set_long_mode(widgets.Label.LONG_DOT)
        self._redraw_labels()

    def on_ready(self):
        self._status_bar = status_bar.StatusBarApp(None, self._wlan)
        self._status_bar.start()
        super().on_ready()

    async def on_run(self):
        while True:
            new_state = self._collect_state()
            refresh = False

            t = self._get_bg_src()
            if t != self._bg_src:
                self._bg_src = t
                self._draw_page_bg(self._bg_src)
                refresh = True

            for key in ("server", "mac", "nick_name", "access_code"):
                if new_state[key] != self._state.get(key):
                    self._state[key] = new_state[key]
                    refresh = True

            if refresh:
                self._redraw_labels()
                self._refresh_status_bar()

            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._status_bar.stop()
        self._task.cancel()

    def on_exit(self):
        del (
            self._server_label,
            self._mac_title_label,
            self._mac_value_label,
            self._nick_title_label,
            self._nick_value_label,
            self._access_label,
            self._code_value_label,
        )

    @staticmethod
    def _draw_page_bg(src):
        M5.Lcd.drawImage(src, 0, 0)

    def _redraw_labels(self):
        self._set_value(self._server_label, self._state.get("server", ""), fallback="")
        self._mac_title_label.set_text("Device MAC:")
        self._set_value(self._mac_value_label, self._state.get("mac", ""), fallback="")
        self._access_label.set_text("Access code:")
        self._set_value(
            self._code_value_label,
            self._state.get("access_code", ""),
            fallback="",
        )
        self._nick_title_label.set_text("Nickname:")
        self._set_value(self._nick_value_label, self._state.get("nick_name", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

    def _refresh_status_bar(self):
        if not hasattr(self, "_status_bar"):
            return
        self._status_bar._time_label.set_text(self._status_bar._time_text)
        self._status_bar._network_img._draw(False)
        self._status_bar._cloud_img._draw(False)

    @staticmethod
    def _set_value(label, text, fallback="-"):
        text = fallback if text is None or text == "" else str(text)
        label.set_text(text)

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

    @staticmethod
    def _get_server():
        try:
            value = esp32.NVS("uiflow").get_str("server")
            if not value:
                return ""
            if value.startswith("http://") or value.startswith("https://"):
                return value
            return "https://" + value
        except Exception:
            return ""

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

    def _collect_state(self):
        return {
            "server": self._get_server(),
            "mac": self._get_mac(),
            "nick_name": self._get_nick_name(),
            "access_code": self._get_access_code(),
        }

    def _is_wifi_connected(self):
        try:
            if self._wlan.network.isconnected():
                return True
            status = self._wlan.connect_status()
            return status in (network.STAT_GOT_IP, self._wlan.STAT_GOT_IP)
        except Exception:
            return False

    def _get_bg_src(self):
        if self._is_wifi_connected():
            return res.DEVELOP_ONLINE_IMG
        return res.DEVELOP_OFFLINE_IMG
