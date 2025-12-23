# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup
import M5
from . import framework
import time

from .apps.status_bar import StatusBarApp
from .apps.settings import SettingsApp
from .apps.dev import DevApp
from .apps.app_list import ListApp


class PaperS3_Startup:
    def __init__(self) -> None:
        self._wlan = Startup()

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self._wlan.connect_network(
            ssid, pswd, protocol=protocol, ip=ip, netmask=netmask, gateway=gateway, dns=dns
        )
        M5.Lcd.drawImage("/system/papers3/startup.png", 0, 0)
        time.sleep(1)

        # M5.Lcd.clear(0x000000)
        # sprite = M5.Lcd.newCanvas(540, 960, 4, True)

        fw = framework.Framework()
        settings_app = SettingsApp(M5.Lcd, data=self._wlan)
        dev_app = DevApp(M5.Lcd, data=self._wlan)
        list_app = ListApp(M5.Lcd)
        fw.install_bar(StatusBarApp(None, self._wlan))
        fw.install_launcher(dev_app)
        fw.install(settings_app)
        fw.install(dev_app)
        fw.install(list_app)
        fw.start()
