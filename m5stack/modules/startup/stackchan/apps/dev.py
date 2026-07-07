# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
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


_BG_COLOR = 0xEEEEEF
_LABEL_COLOR = 0x008FD7
_VALUE_COLOR = 0x000000
_LABEL_FONT = "/system/common/font/Montserrat-Medium-14.vlw"
_VALUE_FONT = "/system/common/font/Montserrat-Medium-18.vlw"
_BG_SRC = "/system/stackchan/Develop/bg.png"
_TEXT_PANEL_W = 181


class DevApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wifi = data
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage("/system/stackchan/Selection/develop_unselected.png", 5 + 62, 20 + 4)
        self.descriptor = app_base.Descriptor(x=5 + 62, y=20 + 4, w=62, h=56)

    def on_launch(self):
        self._state = self._collect_state()

    def on_view(self):
        M5.Lcd.drawImage("/system/stackchan/Selection/develop_selected.png", 5 + 62, 20 + 4)
        self._origin_x = 0
        self._origin_y = 80
        self._lcd.clear(_BG_COLOR)

        self._bg_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._bg_img.set_pos(4, 4)
        self._bg_img.set_size(312, 156)
        self._bg_img.set_src(_BG_SRC)
        self._lcd.fillRect(4, 4, _TEXT_PANEL_W, 156, _BG_COLOR)

        self._mac_label, self._mac_value = self._create_row("Device MAC:", 8)
        self._code_label, self._code_value = self._create_row("Access Code:", 59)
        self._nick_label, self._nick_value = self._create_row("Nickname:", 110)

        self._set_value(self._mac_value, self._state.get("mac", "-"))
        self._set_value(self._code_value, self._state.get("access_code", ""), fallback="")
        self._set_value(self._nick_value, self._state.get("nick_name", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

        self._lcd.push(self._origin_x, self._origin_y)

    async def on_run(self):
        while True:
            new_state = self._collect_state()
            refresh = False

            if new_state["access_code"] != self._state.get("access_code"):
                self._state["access_code"] = new_state["access_code"]
                self._set_value(self._code_value, new_state["access_code"], fallback="")
                print_access_info(self._state.get("nick_name", ""), new_state["access_code"])
                refresh = True

            if new_state["nick_name"] != self._state.get("nick_name"):
                self._state["nick_name"] = new_state["nick_name"]
                self._set_value(self._nick_value, new_state["nick_name"], fallback="")
                print_access_info(new_state["nick_name"], self._state.get("access_code", ""))
                refresh = True

            if refresh:
                self._lcd.push(self._origin_x, self._origin_y)

            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        M5.Lcd.drawImage("/system/stackchan/Selection/develop_unselected.png", 5 + 62, 20 + 4)
        del (
            self._bg_img,
            self._mac_label,
            self._mac_value,
            self._code_label,
            self._code_value,
            self._nick_label,
            self._nick_value,
        )

    async def _click_event_handler(self, x, y, fw):
        pass

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass

    def _create_row(self, label_text, y):
        label = widgets.Label(
            label_text,
            12,
            y,
            w=_TEXT_PANEL_W - 18,
            h=20,
            fg_color=_LABEL_COLOR,
            bg_color=_BG_COLOR,
            font=_LABEL_FONT,
            parent=self._lcd,
        )
        label.set_text(label_text)

        value = widgets.Label(
            "",
            12,
            y + 22,
            w=_TEXT_PANEL_W - 18,
            h=26,
            fg_color=_VALUE_COLOR,
            bg_color=_BG_COLOR,
            font=_VALUE_FONT,
            parent=self._lcd,
        )
        value.set_long_mode(widgets.Label.LONG_DOT)
        return label, value

    @staticmethod
    def _set_value(label, text, fallback="-"):
        text = fallback if text is None or text == "" else str(text)
        label.set_text(text)

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

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
            "access_code": self._get_access_code(),
            "nick_name": self._get_nick_name(),
        }
