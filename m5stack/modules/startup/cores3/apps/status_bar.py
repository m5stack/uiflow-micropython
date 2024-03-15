# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase
from widgets.label import Label
from widgets.image import Image

# from common.font import MontserratMedium10
# from common.font import MontserratMedium16
import time
import M5
import network
import uasyncio as asyncio

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


_WIFI_STATUS_ICO = {
    NetworkStatus.INIT: "/system/cores3/WiFi/wifi_empty.png",
    NetworkStatus.RSSI_GOOD: "/system/cores3/WiFi/wifi_good.png",
    NetworkStatus.RSSI_MID: "/system/cores3/WiFi/wifi_mid.png",
    NetworkStatus.RSSI_WORSE: "/system/cores3/WiFi/wifi_worse.png",
    NetworkStatus.DISCONNECTED: "/system/cores3/WiFi/wifi_disconnected.png",
}

_CLOUD_STATUS_ICOS = {
    CloudStatus.INIT: "/system/cores3/Server/server_empty.png",
    CloudStatus.CONNECTED: "/system/cores3/Server/Server_Green.png",
    CloudStatus.DISCONNECTED: "/system/cores3/Server/server_error.png",
}


class StatusBarApp(AppBase):
    def __init__(self, icos: dict, wifi) -> None:
        self._wifi = wifi

    def on_launch(self):
        self._time_text = self._get_local_time_text()
        self._network_status = self._get_network_status()
        self._cloud_status = self._get_cloud_status()
        self._battery_src = self._get_battery_src(
            M5.Power.getBatteryLevel(), M5.Power.isCharging()
        )
        self._battery_text = self._get_battery_text(M5.Power.getBatteryLevel())

    def on_view(self):
        M5.Lcd.drawImage("/system/cores3/Title/title_blue.png", 0, 0)

        self._time_label = Label(
            "12:23",
            160,
            2,
            w=312,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xEEEEEF,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._time_label.setText(self._time_text)

        self._network_img = Image(use_sprite=False)
        self._network_img.set_pos(320 - 56 - 20 - 5 - 20 - 5, 0)
        self._network_img.set_size(20, 20)
        self._network_img.set_src(_WIFI_STATUS_ICO[self._network_status])

        self._cloud_img = Image(use_sprite=False)
        self._cloud_img.set_pos(320 - 56 - 20 - 5, 0)
        self._cloud_img.set_size(20, 20)
        self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])

        self._battery_img = Image(use_sprite=False)
        self._battery_img.set_pos(320 - 56, 0)
        self._battery_img.set_size(56, 20)
        self._battery_img.set_src(self._battery_src)

        self._battery_label = Label(
            "78%",
            320 - 56 + 22,
            4,
            w=312,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-10.vlw",
        )
        self._battery_label.setText(self._battery_text)

    async def on_run(self):
        refresh = False
        while True:
            t = self._get_local_time_text()
            if t != self._time_text:
                self._time_label.setText(t)
                self._time_text = t

            t = self._get_network_status()
            if t != self._network_status:
                self._network_img.set_src(_WIFI_STATUS_ICO[t])
                self._network_status = t

            t = self._get_cloud_status()
            if t != self._cloud_status:
                self._cloud_img.set_src(_CLOUD_STATUS_ICOS[t])

            t = self._get_battery_src(M5.Power.getBatteryLevel(), M5.Power.isCharging())
            if t != self._battery_src:
                self._battery_img.set_src(t)
                self._battery_src = t
                refresh = True

            t = self._get_battery_text(M5.Power.getBatteryLevel())
            if t != self._battery_text or refresh:
                self._battery_label.setText(t)
                self._battery_text = t
                refresh = False

            await asyncio.sleep_ms(5000)

    def _update_time(self, struct_time):
        self._time_label.setText("{:02d}:{:02d}".format(struct_time[3], struct_time[4]))

    def _update_wifi(self, status):
        self._wifi_status = status
        src = _WIFI_STATUS_ICO.get(self._wifi_status)
        M5.Lcd.drawImage(src.src, src.x, src.y)

    def _update_server(self, status):
        self._server_status = status
        src = _CLOUD_STATUS_ICOS.get(self._server_status)
        M5.Lcd.drawImage(src.src, src.x, src.y)

    @staticmethod
    def _get_local_time_text():
        struct_time = time.localtime()
        return "{:02d}:{:02d}".format(struct_time[3], struct_time[4])

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

    @staticmethod
    def _get_cloud_status():
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

    def _get_battery_src(self, battery, charging):
        src = ""
        if battery > 0 and battery <= 100:
            if battery < 20:
                src = (
                    "/system/cores3/Battery/battery_Red_Charge.png"
                    if charging
                    else "/system/cores3/Battery/battery_Red.png"
                )
            elif battery <= 100:
                src = (
                    "/system/cores3/Battery/battery_Green_Charge.png"
                    if charging
                    else "/system/cores3/Battery/battery_Green.png"
                )
        else:
            src = (
                "/system/cores3/Battery/battery_Black_Charge.png"
                if charging
                else "/system/cores3/Battery/battery_Black.png"
            )
        return src

    @staticmethod
    def _get_battery_text(battery):
        if battery > 0 and battery <= 100:
            return "{:d}%".format(battery)
        else:
            return ""
