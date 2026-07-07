# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import asyncio
import binascii
import esp32
import machine
import widgets

from .. import app_base
from .. import res
from ..layout import SCREEN_W, FONT_BIG, FONT_SMALL, draw_page_bg, is_wifi_connected
from . import status_bar
from startup import print_access_info

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


# Color palette
_LABEL_BG = 0xFEFEFE  # Matches the existing dev background (light)
_LABEL_COLOR = 0x00AA00  # green (label text)
_VALUE_COLOR = 0x000000  # black (value text)
_SERVER_COLOR = 0x008FD7  # blue for the server URL

_ROW_GAP = 80  # vertical distance between section rows
_LABEL_VALUE_GAP = 27  # distance between a label line and its value line


class _LabeledSection:
    """One section = two stacked lines: a small colored label, with a large value below."""

    def __init__(
        self,
        label_text,
        y,
        label_color=_LABEL_COLOR,
        value_color=_VALUE_COLOR,
        value_font=FONT_BIG,
    ):
        self._label_text = label_text
        self._label = widgets.Label(
            label_text,
            SCREEN_W // 2,
            y,
            w=SCREEN_W,
            h=30,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=label_color,
            bg_color=_LABEL_BG,
            font=FONT_SMALL,
        )
        self._label.set_text(label_text)

        self._value = widgets.Label(
            "",
            SCREEN_W // 2,
            y + _LABEL_VALUE_GAP,
            w=SCREEN_W - 40,
            h=50,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=value_color,
            bg_color=_LABEL_BG,
            font=value_font,
        )
        self._value.set_long_mode(widgets.Label.LONG_DOT)
        self._value_text = None

    def set_value(self, text, fallback="-"):
        text = fallback if text is None or text == "" else str(text)
        if text != self._value_text:
            self._value_text = text
            self._value.set_text(text)

    def refresh(self, text, fallback="-"):
        self._label.set_text(self._label_text)
        self._value_text = None
        self.set_value(text, fallback)


class DevApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._state = self._collect_state()
        self._bg_src = self._get_bg_src(self._state.get("wifi_ok"))

    def on_view(self):
        draw_page_bg(self._bg_src)

        self._server_label = widgets.Label(
            "",
            SCREEN_W // 2,
            155,
            w=SCREEN_W,
            h=30,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=_SERVER_COLOR,
            bg_color=_LABEL_BG,
            font=FONT_SMALL,
        )
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)
        self._server_text = None

        base_y = 188
        self._row_mac = _LabeledSection("Device MAC:", base_y + _ROW_GAP * 0)
        self._row_code = _LabeledSection("Access Code:", base_y + _ROW_GAP * 1)
        self._row_nick = _LabeledSection("Nickname:", base_y + _ROW_GAP * 2)

        self._row_mac.set_value(self._format_mac())
        self._set_server_text(self._state.get("server", "-"))
        self._row_code.set_value(self._state.get("access_code", ""), fallback="")
        self._row_nick.set_value(self._state.get("nick_name", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

    def on_ready(self):
        self._status_bar = status_bar.StatusBarApp(None, self._wlan)
        self._status_bar.start()
        super().on_ready()

    async def on_run(self):
        while True:
            new_state = self._collect_state()

            bg_src = self._get_bg_src(new_state["wifi_ok"])
            if bg_src != self._bg_src:
                self._bg_src = bg_src
                self._paint_page()

            if new_state["server"] != self._state.get("server"):
                self._state["server"] = new_state["server"]
                self._set_server_text(new_state["server"])

            if new_state["nick_name"] != self._state.get("nick_name"):
                self._state["nick_name"] = new_state["nick_name"]
                self._row_nick.set_value(new_state["nick_name"], fallback="")

            if new_state["access_code"] != self._state.get("access_code"):
                self._state["access_code"] = new_state["access_code"]
                self._row_code.set_value(new_state["access_code"])

            print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))
            self._state["wifi_ok"] = new_state["wifi_ok"]

            await asyncio.sleep_ms(1500)

    def on_hide(self):
        if hasattr(self, "_status_bar"):
            self._status_bar.stop()
        if self._task:
            self._task.cancel()

    def on_exit(self):
        del (
            self._server_label,
            self._row_mac,
            self._row_nick,
            self._row_code,
        )

    def _paint_page(self):
        draw_page_bg(self._bg_src)
        self._redraw_labels()
        self._refresh_status_bar()

    def _refresh_status_bar(self):
        if not hasattr(self, "_status_bar"):
            return
        bar = self._status_bar
        bar._time_label.set_text(bar._time_text)
        bar._draw_network_icon()
        bar._draw_server_icon()

    def _set_server_text(self, text):
        text = "-" if text in (None, "") else str(text)
        if text != self._server_text:
            self._server_text = text
            self._server_label.set_text(text)

    def _redraw_labels(self):
        self._server_text = None
        self._set_server_text(self._state.get("server", "-"))
        self._row_mac.refresh(self._format_mac())
        self._row_code.refresh(self._state.get("access_code", ""), fallback="")
        self._row_nick.refresh(self._state.get("nick_name", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

    @staticmethod
    def _get_bg_src(wifi_ok):
        if wifi_ok:
            return res.DEVELOP_ONLINE_IMG
        return res.DEVELOP_OFFLINE_IMG

    @staticmethod
    def _format_mac():
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

    @staticmethod
    def _get_server():
        try:
            value = esp32.NVS("uiflow").get_str("server")
            return value or "-"
        except Exception:
            return "-"

    def _collect_state(self):
        wifi_ok = is_wifi_connected(self._wlan)

        nick = ""
        code = ""
        if _HAS_SERVER and wifi_ok:
            try:
                if M5Things.status() == 2:
                    nick = M5Things.nick_name() or ""
                    code = M5Things.accesscode() or ""
            except Exception:
                pass

        return {
            "wifi_ok": wifi_ok,
            "nick_name": nick,
            "access_code": code,
            "server": self._get_server(),
        }
