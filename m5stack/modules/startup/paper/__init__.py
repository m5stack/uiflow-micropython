# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup
import M5
import network
from widgets.label import Label
from widgets.image import Image
from .framework import Framework
import time

from .apps.status_bar import StatusBarApp
from .apps.settings import SettingsApp
from .apps.dev import DevApp
from .apps.app_list import ListApp


class Paper_Startup:
    def __init__(self) -> None:
        self._wlan = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wlan.connect_network(ssid, pswd)
        M5.Lcd.drawImage("/system/paper/startup.jpg", 0, 0)
        time.sleep(1)

        # M5.Lcd.clear(0x000000)
        # sprite = M5.Lcd.newCanvas(540, 960, 4, True)

        fw = Framework()
        settings_app = SettingsApp(M5.Lcd, data=self._wlan)
        dev_app = DevApp(M5.Lcd, data=self._wlan)
        list_app = ListApp(M5.Lcd)
        fw.install_bar(StatusBarApp(None, self._wlan))
        fw.install_launcher(dev_app)
        fw.install(settings_app)
        fw.install(dev_app)
        fw.install(list_app)
        fw.start()
