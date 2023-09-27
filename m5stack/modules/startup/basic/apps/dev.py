from ..app import AppBase
import M5
from M5 import Widgets
from widgets.image import Image
from widgets.label import Label
import uasyncio as asyncio
import urequests as requests
import os
import binascii
import machine
import network

from ..res import (
    WIFI_EMPTY_IMG,
    WIFI_GOOD_IMG,
    WIFI_MID_IMG,
    WIFI_WORSE_IMG,
    WIFI_DISCONNECTED_IMG,
    SERVER_EMPTY_IMG,
    SERVER_GREEN_IMG,
    SERVER_ERROR_IMG,
    DEVELOP_UNSELECTED_IMG,
    DEVELOP_SELECTED_IMG,
    DEVELOP_PRIVATE_IMG,
    DEVELOP_PUBLIC_IMG,
    BAR2_IMG,
    BAR3_IMG,
    BATTERY_RED_CHARGE_IMG,
    BATTERY_RED_IMG,
    BATTERY_GREEN_CHARGE_IMG,
    BATTERY_GREEN_IMG,
    BATTERY_BLACK_CHARGE_IMG,
    BATTERY_BLACK_IMG,
    AVATAR_IMG,
    USER_AVATAR_PATH,
)

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


_NETWORK_STATUS_ICOS = {
    NetworkStatus.INIT: WIFI_EMPTY_IMG,
    NetworkStatus.RSSI_GOOD: WIFI_GOOD_IMG,
    NetworkStatus.RSSI_MID: WIFI_MID_IMG,
    NetworkStatus.RSSI_WORSE: WIFI_WORSE_IMG,
    NetworkStatus.DISCONNECTED: WIFI_DISCONNECTED_IMG,
}

_CLOUD_STATUS_ICOS = {
    CloudStatus.INIT: SERVER_EMPTY_IMG,
    CloudStatus.CONNECTED: SERVER_GREEN_IMG,
    CloudStatus.DISCONNECTED: SERVER_ERROR_IMG,
}


class DevApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wifi = data
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage(DEVELOP_UNSELECTED_IMG, 5 + 62 * 1, 0)

    def on_launch(self):
        self._mac_text = self._get_mac()
        self._account_text = self._get_account()
        self._bg_src = self._get_bg_src()
        self._status_bar_src = self._get_bar_src()
        self._network_status = self._get_network_status()
        self._cloud_status = self._get_cloud_status()
        self._battery_src = self._get_battery_src(
            M5.Power.getBatteryLevel(), M5.Power.isCharging()
        )
        self._battery_text = self._get_battery_text(M5.Power.getBatteryLevel())
        self._avatar_src = self._get_avatar()

    def on_view(self):
        M5.Lcd.drawImage(DEVELOP_SELECTED_IMG, 5 + 62 * 1, 0)
        self._origin_x = 0
        self._origin_y = 56

        M5.Lcd.fillRect(self._origin_x, self._origin_y, 320, 184, 0x000000)

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(self._origin_x + 4, self._origin_y + 4)
        self._bg_img.set_size(312, 156)
        self._bg_img.set_src(self._bg_src)

        self._mac_label = Label(
            "aabbcc112233",
            4 + 6,
            self._origin_y + 4 + 57,
            w=177,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=Widgets.FONTS.DejaVu18,
        )
        self._mac_label.setText(self._mac_text)

        self._account_label = Label(
            "XXABC",
            4 + 6,
            self._origin_y + 4 + 57 + 40,
            w=110,
            h=60,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=Widgets.FONTS.DejaVu18,
        )
        self._account_label.setText(self._account_text)

        self._avatar_img = Image(use_sprite=False)
        self._avatar_img.set_pos(130, self._origin_y + 100)
        self._avatar_img.set_size(56, 56)
        self._avatar_img.set_scale(0.28, 0.28)
        try:
            os.stat(self._avatar_src)
            self._avatar_img.set_src(self._avatar_src)
        except OSError:
            self._avatar_img.set_src(AVATAR_IMG)

        self._bar_img = Image(use_sprite=False)
        self._bar_img.set_pos(0, self._origin_y + 164)
        self._bar_img.set_size(320, 20)
        self._bar_img.set_src(self._status_bar_src)

        self._network_img = Image(use_sprite=False)
        self._network_img.set_pos(320 - 56 - 20 - 5 - 20 - 5, self._origin_y + 164)
        self._network_img.set_size(20, 20)
        self._network_img.set_src(_NETWORK_STATUS_ICOS[self._network_status])

        self._cloud_img = Image(use_sprite=False)
        self._cloud_img.set_pos(320 - 56 - 20 - 5, self._origin_y + 164)
        self._cloud_img.set_size(20, 20)
        self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])

        self._battery_img = Image(use_sprite=False)
        self._battery_img.set_pos(320 - 56, self._origin_y + 164)
        self._battery_img.set_size(56, 20)
        self._battery_img.set_src(self._battery_src)

        self._battery_label = Label(
            "0%",
            320 - 56 + 22,
            220 + 6,
            w=22,
            h=10,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu9,
        )
        self._battery_label.setText(self._battery_text)

    async def on_run(self):
        refresh_bg = False
        refresh_bar = False
        while True:
            t = self._get_bg_src()
            if t != self._bg_src:
                self._bg_src = t
                self._bg_img.set_src(self._bg_src)
                refresh_bg = True

            refresh_bg and self._mac_label.setText(self._mac_text)

            t = self._get_account()
            if t != self._account_text or refresh_bg:
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
            elif refresh_bg:
                self._avatar_img._draw(False)

            t = self._get_bar_src()
            if t != self._status_bar_src:
                self._status_bar_src = t
                self._bar_img.set_src(self._status_bar_src)
                refresh_bar = True

            t = self._get_network_status()
            if t != self._network_status:
                self._network_status = t
                self._network_img.set_src(_NETWORK_STATUS_ICOS[self._network_status])
            elif refresh_bar:
                self._network_img._draw(False)

            t = self._get_cloud_status()
            if t != self._cloud_status:
                self._cloud_status = t
                self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])
            elif refresh_bar:
                self._cloud_img._draw(False)

            t = self._get_battery_src(M5.Power.getBatteryLevel(), M5.Power.isCharging())
            if t != self._battery_src:
                self._battery_src = t
                self._battery_img.set_src(self._battery_src)
            elif refresh_bar:
                self._battery_img._draw(False)

            t = self._get_battery_text(M5.Power.getBatteryLevel())
            if t != self._battery_text or refresh_bar:
                self._battery_text = t
                self._battery_label.setText(self._battery_text)

            refresh_bg = False
            refresh_bar = False
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        if hasattr(self, "_dl_task"):
            self._dl_task.cancel()
        self._task.cancel()

    def on_exit(self):
        M5.Lcd.drawImage(DEVELOP_UNSELECTED_IMG, 5 + 62 * 1, 0)
        del self._bg_img, self._mac_label, self._account_label, self._avatar_img
        del self._bar_img, self._network_img, self._cloud_img, self._battery_img
        del self._battery_label
        del self._origin_x, self._origin_y
        del self._mac_text
        del self._account_text
        del self._bg_src
        del self._status_bar_src
        del self._network_status
        del self._cloud_status
        del self._battery_src
        del self._battery_text
        del self._avatar_src

    async def _btna_event_handler(self, fw):
        # print("_btna_event_handler")
        pass

    async def _btnb_event_handler(self, fw):
        # print("_btnb_event_handler")
        pass

    async def _btnc_event_handler(self, fw):
        # print("_btnc_event_handler")
        pass

    async def _dl_avatar(self, dst):
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if len(infos[4]) is 0:
                self._avatar_img.set_src(AVATAR_IMG)
            else:
                try:
                    rsp = requests.get("http://community.m5stack.com" + str(infos[4]))
                    f = open(dst, "wb")
                    f.write(rsp.content)
                    f.close()
                    self._avatar_img.set_src(dst)
                except Exception as e:
                    print(e)
                    os.remove(dst)
                    self._avatar_img.set_src(AVATAR_IMG)
                finally:
                    rsp.close()
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
            if len(infos[4]) is 0:
                return AVATAR_IMG
            else:
                return USER_AVATAR_PATH + str(infos[4]).split("/")[-1]
        else:
            return AVATAR_IMG

    def _get_bg_src(self):
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if infos[0] is 0:
                return DEVELOP_PRIVATE_IMG
            elif infos[0] in (1, 2):
                return DEVELOP_PUBLIC_IMG
        else:
            return DEVELOP_PRIVATE_IMG

    def _get_bar_src(self):
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if infos[0] is 0:
                return BAR2_IMG
            elif infos[0] in (1, 2):
                return BAR3_IMG
        else:
            return BAR2_IMG

    def _get_network_status(self):
        status = self._wifi.connect_status()
        if status is network.STAT_GOT_IP:
            rssi = self._wifi.get_rssi()
            if rssi <= -80:
                return NetworkStatus.RSSI_WORSE
            elif rssi <= -60:
                return NetworkStatus.RSSI_MID
            else:
                return NetworkStatus.RSSI_GOOD
        else:
            return NetworkStatus.DISCONNECTED

    def _get_cloud_status(self):
        if _HAS_SERVER is True:
            status = M5Things.status()
            return {
                -2: CloudStatus.DISCONNECTED,
                -1: CloudStatus.DISCONNECTED,
                0: CloudStatus.INIT,
                1: CloudStatus.INIT,
                2: CloudStatus.CONNECTED,
                3: CloudStatus.DISCONNECTED,
            }[status]
        else:
            return CloudStatus.DISCONNECTED

    @staticmethod
    def _get_battery_src(battery, charging):
        src = ""
        if battery > 0 and battery <= 100:
            if battery < 20:
                src = BATTERY_RED_CHARGE_IMG if charging else BATTERY_RED_IMG
            elif battery <= 100:
                src = BATTERY_GREEN_CHARGE_IMG if charging else BATTERY_GREEN_IMG
        else:
            src = BATTERY_BLACK_CHARGE_IMG if charging else BATTERY_BLACK_IMG
        return src

    @staticmethod
    def _get_battery_text(battery):
        if battery > 0 and battery <= 100:
            return "{:d}%".format(battery)
        else:
            return ""
