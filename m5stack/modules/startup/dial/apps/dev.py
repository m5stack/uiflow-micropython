# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import widgets
import asyncio
import binascii
import machine
from .. import res
from . import status_bar

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
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._mac_text = self._get_mac()
        self._account_text = self._get_account()
        self._bg_src = self._get_bg_src()

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 0

        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(0, 0)
        self._bg_img.set_size(240, 240)
        self._bg_img.set_src(self._bg_src)

        self._mac_label = widgets.Label(
            "aabbcc112233",
            12,
            140,
            w=120,
            h=20,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._mac_label.set_text(self._mac_text)

        self._account_label = widgets.Label(
            "XXABC",
            55,
            176,
            w=100,
            h=40,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._account_label.set_text(self._account_text)

    def on_ready(self):
        self._status_bar = status_bar.StatusBarApp(None, self._wlan)
        self._status_bar.start()
        super().on_ready()

    async def on_run(self):
        refresh = False
        while True:
            t = self._get_bg_src()
            if t != self._bg_src:
                self._bg_src = t
                self._bg_img.set_src(self._bg_src)
                refresh = True

            refresh and self._mac_label.set_text(self._mac_text)

            t = self._get_account()
            if t != self._account_text or refresh:
                self._account_text = t
                self._account_label.set_text(self._account_text)

            refresh = False
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._status_bar.stop()
        self._task.cancel()

    def on_exit(self):
        del self._bg_img, self._mac_label, self._account_label

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).upper()

    @staticmethod
    def _get_account():
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            return "None" if len(infos[1]) == 0 else infos[1]
        else:
            return "None"

    def _get_bg_src(self):
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if infos[0] == 0:
                return res.DEVELOP_PRIVATE_IMG
            elif infos[0] in (1, 2):
                return res.DEVELOP_PUBLIC_IMG
        else:
            return res.DEVELOP_PRIVATE_IMG
