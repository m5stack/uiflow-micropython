# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase
from widgets.label import Label
from widgets.image import Image
import time
import M5
import network
import asyncio

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
    NetworkStatus.INIT: "/system/box3/WiFi/wifi_empty.png",
    NetworkStatus.RSSI_GOOD: "/system/box3/WiFi/wifi_good.png",
    NetworkStatus.RSSI_MID: "/system/box3/WiFi/wifi_mid.png",
    NetworkStatus.RSSI_WORSE: "/system/box3/WiFi/wifi_worse.png",
    NetworkStatus.DISCONNECTED: "/system/box3/WiFi/wifi_disconnected.png",
}

_CLOUD_STATUS_ICOS = {
    CloudStatus.INIT: "/system/box3/Server/server_empty.png",
    CloudStatus.CONNECTED: "/system/box3/Server/Server_Green.png",
    CloudStatus.DISCONNECTED: "/system/box3/Server/server_error.png",
}


class StatusBarApp(AppBase):
    def __init__(self, icos: dict, wifi) -> None:
        self._wifi = wifi

    def on_launch(self):
        self._time_text = self._get_local_time_text()
        self._network_status = self._get_network_status()
        self._cloud_status = self._get_cloud_status()

    def on_view(self):
        M5.Lcd.drawImage("/system/box3/Title/title_blue.png", 0, 0)

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
        self._time_label.set_text(self._time_text)

        self._network_img = Image(use_sprite=False)
        self._network_img.set_pos(320 - 20 - 5 - 20 - 5, 0)
        self._network_img.set_size(20, 20)
        self._network_img.set_src(_WIFI_STATUS_ICO[self._network_status])

        self._cloud_img = Image(use_sprite=False)
        self._cloud_img.set_pos(320 - 20 - 5, 0)
        self._cloud_img.set_size(20, 20)
        self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])

    async def on_run(self):
        while True:
            t = self._get_local_time_text()
            if t != self._time_text:
                self._time_label.set_text(t)
                self._time_text = t

            t = self._get_network_status()
            if t != self._network_status:
                self._network_img.set_src(_WIFI_STATUS_ICO[t])
                self._network_status = t

            t = self._get_cloud_status()
            if t != self._cloud_status:
                self._cloud_img.set_src(_CLOUD_STATUS_ICOS[t])

            await asyncio.sleep_ms(5000)

    def _update_time(self, struct_time):
        self._time_label.set_text("{:02d}:{:02d}".format(struct_time[3], struct_time[4]))

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
