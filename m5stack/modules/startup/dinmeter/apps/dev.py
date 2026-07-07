# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
import widgets
import M5
import machine
import asyncio
import binascii
from startup import print_access_info

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


_BG_COLOR = 0xFEFEFE
_SCREEN_BG_COLOR = 0xEEEEEF
_EXIT_BG_COLOR = 0x333333
_LABEL_COLOR = 0x888888
_VALUE_COLOR = 0x000000

_SCREEN_X = 0
_SCREEN_Y = 16
_SCREEN_W = 240
_SCREEN_H = 119

_TEXT_PANEL_W = 139
_PANEL_X = 0
_PANEL_Y = 18
_ROW_X = 13
_ROW_VALUE_GAP = 12
_STATUS_W = 140
_STATUS_H = 22
_STATUS_X = 3
_STATUS_Y = 19
_BG_W = 240
_BG_H = 120

_ROW_MAC_Y = 47
_ROW_CODE_Y = 77
_ROW_NICK_Y = 105


class DevApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._state = self._collect_state()

    def on_view(self):
        M5.Lcd.fillRect(_SCREEN_X, _SCREEN_Y, _SCREEN_W, _SCREEN_H, _SCREEN_BG_COLOR)

        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(_PANEL_X, _PANEL_Y)
        self._bg_img.set_size(_BG_W, _BG_H)
        self._bg_img.set_src(res.DEVELOP_BG_IMG)

        self._status_img = widgets.Image(use_sprite=False)
        self._status_img.set_pos(_STATUS_X, _STATUS_Y)
        self._status_img.set_size(_STATUS_W, _STATUS_H)
        self._status_img.set_src(self._state.get("status_src", res.DEVELOP_OFFLINE_IMG))

        self._mac_label, self._mac_value = self._create_row("Device MAC:", _ROW_MAC_Y)
        self._code_label, self._code_value = self._create_row("Access Code:", _ROW_CODE_Y)
        self._nick_label, self._nick_value = self._create_row("Nickname:", _ROW_NICK_Y)

        self._set_value(self._mac_value, self._state.get("mac", "-"))
        self._set_value(self._code_value, self._state.get("access_code", ""), fallback="")
        self._set_value(self._nick_value, self._state.get("nick_name", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

    def on_ready(self):
        super().on_ready()

    async def on_run(self):
        while True:
            new_state = self._collect_state()

            if new_state["status_src"] != self._state.get("status_src"):
                self._state["status_src"] = new_state["status_src"]
                self._status_img.set_src(new_state["status_src"])

            if new_state["access_code"] != self._state.get("access_code"):
                self._state["access_code"] = new_state["access_code"]
                self._set_value(self._code_value, new_state["access_code"], fallback="")
                print_access_info(self._state.get("nick_name", ""), new_state["access_code"])
                self._nick_label.set_text("Nickname:")
                self._set_value(self._nick_value, self._state.get("nick_name", ""), fallback="")

            if new_state["nick_name"] != self._state.get("nick_name"):
                self._state["nick_name"] = new_state["nick_name"]
                self._set_value(self._nick_value, new_state["nick_name"], fallback="")
                print_access_info(new_state["nick_name"], self._state.get("access_code", ""))

            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        M5.Lcd.fillRect(30, 19, 210, 116, _EXIT_BG_COLOR)
        del self._bg_img, self._status_img, self._mac_label, self._mac_value
        del self._code_label, self._code_value, self._nick_label, self._nick_value

    @staticmethod
    def _set_value(label, text, fallback="-"):
        text = fallback if text is None or text == "" else str(text)
        label.set_text(text)

    @staticmethod
    def _create_row(label_text, y):
        label = widgets.Label(
            label_text,
            _ROW_X,
            y,
            w=_TEXT_PANEL_W - 18,
            h=12,
            fg_color=_LABEL_COLOR,
            bg_color=_BG_COLOR,
            font=res.MontserratMedium10_VLW,
        )
        label.set_text(label_text)

        value = widgets.Label(
            "",
            _ROW_X,
            y + _ROW_VALUE_GAP,
            w=_TEXT_PANEL_W - 18,
            h=15,
            fg_color=_VALUE_COLOR,
            bg_color=_BG_COLOR,
            font=res.MontserratMedium12_VLW,
        )
        value.set_long_mode(widgets.Label.LONG_DOT)
        return label, value

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

    @staticmethod
    def _get_status_src():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return res.DEVELOP_ONLINE_IMG
            except Exception:
                pass
        return res.DEVELOP_OFFLINE_IMG

    @staticmethod
    def _get_access_code():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
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

    def _collect_state(self):
        return {
            "mac": self._get_mac(),
            "status_src": self._get_status_src(),
            "access_code": self._get_access_code(),
            "nick_name": self._get_nick_name(),
        }
