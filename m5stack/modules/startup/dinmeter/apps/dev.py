from ..app import AppBase
from ..res import DEVELOP_PRIVATE_IMG, DEVELOP_PUBLIC_IMG, AVATAR_IMG, MontserratMedium12_VLW
from widgets.image import Image
from widgets.label import Label
import M5
import requests
import machine
import asyncio
import binascii
import os

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

        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(6, 22)
        self._bg_img.set_size(228, 107)
        self._bg_img.set_src(self._bg_src)
        self._avatar_src = self._get_avatar()

        self._mac_label = Label(
            "aabbcc112233",
            15,
            63,
            w=116,
            h=15,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium12_VLW,
        )
        self._mac_label.setText(self._mac_text)

        self._account_label = Label(
            "XXABC",
            15,
            92,
            w=90,
            h=34,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium12_VLW,
        )
        self._account_label.setText(self._account_text)

        self._avatar_img = Image(use_sprite=False)
        self._avatar_img.set_pos(110, 91)
        self._avatar_img.set_size(38, 38)
        self._avatar_img.set_scale(0.19, 0.19)
        self._avatar_img.set_src(self._avatar_src)

    def on_ready(self):
        super().on_ready()

    async def on_run(self):
        refresh = False
        while True:
            t = self._get_bg_src()
            if t != self._bg_src:
                self._bg_src = t
                self._bg_img.set_src(self._bg_src)
                refresh = True

            refresh and self._mac_label.setText(self._mac_text)

            t = self._get_account()
            if t != self._account_text or refresh:
                print(refresh)
                print(self._account_text)
                print(t)
                self._account_text = t
                self._account_label.setText(self._account_text)

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

            refresh = False
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        M5.Lcd.fillRect(30, 19, 210, 116, 0x333333)
        del self._bg_img, self._mac_label, self._account_label

    async def _dl_avatar(self, dst):
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if len(infos[4]) is 0:
                self._avatar_img.set_src(AVATAR_IMG)
            else:
                try:
                    rsp = requests.get("https://community.m5stack.com" + str(infos[4]))
                    length = int(rsp.headers["Content-Length"])
                    BLOCKLEN = 1024
                    source = rsp.raw
                    read = 0
                    with open(dst, "wb") as f:
                        # 逐块读取数据
                        while read < length:
                            to_read = BLOCKLEN if (length - read) >= BLOCKLEN else length - read
                            buf = source.read(to_read)
                            read += len(buf)
                            f.write(buf)
                    self._avatar_img.set_src(dst)
                except:
                    self._avatar_img.set_src(AVATAR_IMG)
        else:
            self._avatar_img.set_src(AVATAR_IMG)

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).upper()

    @staticmethod
    def _get_account():
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            return "None" if len(infos[1]) is 0 else infos[1]
        else:
            return "None"

    @staticmethod
    def _get_avatar():
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            print(infos)
            if len(infos[4]) is 0:
                return AVATAR_IMG
            else:
                return "/system/common/img/" + str(infos[4]).split("/")[-1]
        else:
            return AVATAR_IMG

    @staticmethod
    def _get_bg_src():
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if infos[0] is 0:
                return DEVELOP_PRIVATE_IMG
            elif infos[0] in (1, 2):
                return DEVELOP_PUBLIC_IMG
        else:
            return DEVELOP_PRIVATE_IMG
