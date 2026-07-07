# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
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


class DevApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wifi = data
        super().__init__()

    def on_install(self):
        self.descriptor = app_base.Descriptor(x=493, y=1, w=48, h=181)

    def on_launch(self):
        self._mac_text = self._get_mac()
        self._state_text = self._get_state()
        self._nick_name_text = self._get_nick_name()
        self._access_code_text = self._get_access_code()

    def on_view(self):
        M5.Lcd.drawImage("/system/paper/flow.png", 0, 0)
        # self._lcd.drawImage("/system/paper/flow.png", 0, 0)

        self._state_label = widgets.Label(
            "------",
            89,
            452,
            w=360,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=self._lcd,
        )
        self._state_label.set_text(self._state_text)

        self._mac_label = widgets.Label(
            "aabbcc112233",
            89,
            572,
            w=360,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=self._lcd,
        )
        self._mac_label.set_text(self._mac_text)

        self._nick_name_label = widgets.Label(
            "XXABC",
            89,
            812,
            w=360,
            h=50,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=self._lcd,
        )
        self._nick_name_label.set_long_mode(self._nick_name_label.LONG_DOT)
        self._nick_name_label.set_text(self._nick_name_text)

        self._access_code_label = widgets.Label(
            "------",
            89,
            692,
            w=360,
            h=50,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=self._lcd,
        )
        self._access_code_label.set_long_mode(self._access_code_label.LONG_DOT)
        self._access_code_label.set_text(self._access_code_text)

        # self._lcd.push(0, 0)

    async def on_run(self):
        refresh = False
        while True:
            t = self._get_state()
            if t != self._state_text:
                self._state_text = t
                self._state_label.set_text(self._state_text)
                refresh = True

            refresh and self._mac_label.set_text(self._mac_text)

            t = self._get_access_code()
            if t != self._access_code_text or refresh:
                self._access_code_text = t
                self._access_code_label.set_text(self._access_code_text)
                print_access_info(self._nick_name_text, self._access_code_text)
                refresh = True

            t = self._get_nick_name()
            if t != self._nick_name_text or refresh:
                self._nick_name_text = t
                self._nick_name_label.set_text(self._nick_name_text)
                print_access_info(self._nick_name_text, self._access_code_text)
                refresh = True

            # if refresh:
            #     self._lcd.push(0, 0)

            refresh = False
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
