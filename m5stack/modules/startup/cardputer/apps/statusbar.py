from ..app import AppBase
from ..res import (
    BATTERY_BLACK_CHARGE_IMG,
    BATTERY_BLACK_IMG,
    BATTERY_GREEN_CHARGE_IMG,
    BATTERY_GREEN_IMG,
    BATTERY_RED_CHARGE_IMG,
    BATTERY_RED_IMG,
    SERVER_EMPTY_IMG,
    SERVER_ERROR_IMG,
    SERVER_GREEN_IMG,
    WIFI_DISCONNECTED_IMG,
    WIFI_EMPTY_IMG,
    WIFI_GOOD_IMG,
    WIFI_MID_IMG,
    WIFI_WORSE_IMG,
)
from widgets.label import Label
from widgets.image import Image

import M5
import network
import asyncio
import time

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
        M5.Lcd.fillRoundRect(32, 3, 206, 16, 10, 0xEEEEEF)
        self._time_label = Label(
            "12:23",
            32 + 206 // 2,
            4,
            w=48,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xEEEEEF,
            font="/system/common/font/Montserrat-Medium-12.vlw",
        )
        self._time_label.setText(self._time_text)

        self._network_img = Image(use_sprite=False)
        self._network_img.set_pos(41, 3)
        self._network_img.set_size(16, 16)
        self._network_img.set_src(_WIFI_STATUS_ICO[self._network_status])

        self._cloud_img = Image(use_sprite=False)
        self._cloud_img.set_pos(59, 3)
        self._cloud_img.set_size(16, 16)
        self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])

        self._battery_img = Image(use_sprite=False)
        self._battery_img.set_pos(186, 3)
        self._battery_img.set_size(45, 16)
        self._battery_img.set_src(self._battery_src)

        self._battery_label = Label(
            "78%",
            203,
            5,
            w=26 + 4,
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

    @staticmethod
    def _get_battery_src(battery, charging):
        src = ""
        if battery > 0 and battery <= 100:
            if battery < 20:
                src = (
                    BATTERY_RED_CHARGE_IMG
                    if charging
                    else BATTERY_RED_IMG
                )
            elif battery <= 100:
                src = (
                    BATTERY_GREEN_CHARGE_IMG
                    if charging
                    else BATTERY_GREEN_IMG
                )
        else:
            src = (
                BATTERY_BLACK_CHARGE_IMG
                if charging
                else BATTERY_BLACK_IMG
            )
        return src

    @staticmethod
    def _get_battery_text(battery):
        if battery > 0 and battery <= 100:
            return "{:d}%".format(battery)
        else:
            return ""