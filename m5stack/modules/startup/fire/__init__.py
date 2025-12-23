# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup
import M5
from . import framework
from .apps.settings import SettingsApp
from .apps.dev import DevApp
from .apps.app_run import RunApp
from .apps.app_list import ListApp
from .apps.ezdata import EzDataApp
import time
from .res import LOGO_IMG


class Sprite:
    def __init__(self, x, y, w, h, bpp, psram, parent=M5.Lcd) -> None:
        self._sprite = parent.newCanvas(w, h, bpp, psram)
        self._x = x
        self._y = y

    def refresh(self):
        self._sprite.push(self._x, self._y)


class Fire_Startup:
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
        M5.Speaker.setVolume(80)
        M5.Speaker.tone(4000, 50)

        M5.Lcd.drawImage(LOGO_IMG)
        time.sleep_ms(200)

        sprite = M5.Lcd.newCanvas(320, 184, 16, True)

        fw = framework.Framework()
        settings_app = SettingsApp(sprite, data=self._wlan)
        dev_app = DevApp(sprite, data=self._wlan)
        run_app = RunApp(None)
        list_app = ListApp(sprite)
        fw.install_launcher(dev_app)
        fw.install(settings_app)
        fw.install(dev_app)
        fw.install(run_app)
        fw.install(list_app)
        fw.install(EzDataApp(sprite))
        fw.start()
