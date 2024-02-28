from ..app import AppBase
from widgets.label import Label
from widgets.image import Image
from common.font import MontserratMedium10
from common.font import MontserratMedium16
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
    NetworkStatus.INIT: "",
    NetworkStatus.RSSI_GOOD: "/system/paper/wifi_icon_ok_40@925.jpg",
    NetworkStatus.RSSI_MID: "/system/paper/wifi_icon_ok_40@925.jpg",
    NetworkStatus.RSSI_WORSE: "/system/paper/wifi_icon_ok_40@925.jpg",
    NetworkStatus.DISCONNECTED: "/system/paper/wifi_icon_error_40@925.jpg",
}

_CLOUD_STATUS_ICOS = {
    CloudStatus.INIT: "",
    CloudStatus.CONNECTED: "/system/paper/server_icon_ok_80@925.jpg",
    CloudStatus.DISCONNECTED: "/system/paper/server_icon_error_80@925.jpg",
}


class StatusBarApp(AppBase):
    def __init__(self, icos: dict, wifi) -> None:
        self._wifi = wifi

    def on_launch(self):
        self._network_status = self._get_network_status()
        self._cloud_status = self._get_cloud_status()

    def on_view(self):
        self._network_img = Image(use_sprite=False)
        self._network_img.set_pos(40, 925)
        self._network_img.set_size(32, 26)
        self._network_img.set_src(_WIFI_STATUS_ICO[self._network_status])

        self._cloud_img = Image(use_sprite=False)
        self._cloud_img.set_pos(80, 925)
        self._cloud_img.set_size(32, 260)
        self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])

    async def on_run(self):
        while True:
            t = self._get_network_status()
            if t != self._network_status:
                self._network_img.set_src(_WIFI_STATUS_ICO[t])
                self._network_status = t

            t = self._get_cloud_status()
            if t != self._cloud_status:
                self._cloud_img.set_src(_CLOUD_STATUS_ICOS[t])

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


