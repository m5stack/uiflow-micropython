# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase, Descriptor
import M5
from widgets.image import Image
from widgets.label import Label
import asyncio
import requests
import os
import binascii
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


class DevApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wifi = data
        super().__init__()

    def on_install(self):
        self.descriptor = Descriptor(x=493, y=1, w=48, h=181)

    def on_launch(self):
        self._mac_text = self._get_mac()
        self._account_text = self._get_account()
        self._avatar_src = self._get_avatar()
        self._mode_text = self._get_mode()

    def on_view(self):
        M5.Lcd.drawImage("/system/paper/flow.png", 0, 0)
        # self._lcd.drawImage("/system/paper/flow.png", 0, 0)

        self._mode_label = Label(
            "------",
            89,
            476,
            w=360,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.DejaVu40,
            parent=self._lcd,
        )
        self._mode_label.set_text(self._mode_text)

        self._mac_label = Label(
            "aabbcc112233",
            89,
            611,
            w=360,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.DejaVu40,
            parent=self._lcd,
        )
        self._mac_label.set_text(self._mac_text)

        self._account_label = Label(
            "XXABC",
            89,
            747,
            w=110,
            h=60,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.DejaVu40,
            parent=self._lcd,
        )
        self._account_label.set_text(self._account_text)

        self._avatar_img = Image(use_sprite=False, parent=self._lcd)
        self._avatar_img.set_pos(379, 679)
        self._avatar_img.set_size(56, 56)
        self._avatar_img.set_scale(0.28, 0.28)
        self._avatar_img.set_src(self._avatar_src)

        # self._lcd.push(0, 0)

    async def on_run(self):
        refresh = False
        while True:
            t = self._get_mode()
            if t != self._mode_text:
                self._mode_text = t
                self._mode_label.set_text(self._mode_text)
                refresh = True

            refresh and self._mac_label.set_text(self._mac_text)

            t = self._get_account()
            if t != self._account_text or refresh:
                self._account_text = t
                self._account_label.set_text(self._account_text)
                refresh = True

            t = self._get_avatar()
            if t != self._avatar_src:
                self._avatar_src = t
                try:
                    os.stat(self._avatar_src)
                    self._avatar_img.set_src(self._avatar_src)
                except OSError:
                    self._dl_task = asyncio.create_task(self._dl_avatar(self._avatar_src))
            elif refresh:
                self._avatar_img._draw(False)

            # if refresh:
            #     self._lcd.push(0, 0)

            refresh = False
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        if hasattr(self, "_dl_task"):
            self._dl_task.cancel()
        self._task.cancel()

    def on_exit(self):
        del self._mode_label, self._mac_label, self._account_label, self._avatar_img

    async def _click_event_handler(self, x, y, fw):
        pass

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass

    async def _dl_avatar(self, dst):
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if len(infos[4]) == 0:
                self._avatar_img.set_src("/system/common/img/avatar.jpg")
            else:
                try:
                    rsp = requests.get("https://community.m5stack.com" + str(infos[4]))
                    f = open(dst, "wb")
                    f.write(rsp.content)
                    f.close()
                    rsp.close()
                    self._avatar_img.set_src(dst)
                except:
                    self._avatar_img.set_src("/system/common/img/avatar.jpg")
                finally:
                    self._lcd.push(self._origin_x, self._origin_y)
        else:
            self._avatar_img.set_src("/system/common/img/avatar.jpg")

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

    @staticmethod
    def _get_avatar():
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if len(infos[4]) == 0:
                return "/system/common/img/avatar.jpg"
            else:
                return "/system/common/img/" + str(infos[4]).split("/")[-1]
        else:
            return "/system/common/img/avatar.jpg"

    def _get_mode(self):
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if infos[0] == 0:
                return "PRIVATE"
            elif infos[0] in (1, 2):
                return "PUBLIC"
        else:
            return "PRIVATE"
