# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import startup
from . import framework
from . import apps
import M5
import time


class CoreS3_Startup:
    def __init__(self) -> None:
        self._wlan = startup.Startup()
        # self._status_bar = StatusBarApp(None, self._wifi)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wlan.connect_network(ssid, pswd)
        M5.Lcd.drawImage("/system/cores3/boot.png", 0, 0)
        time.sleep(0.2)

        M5.Lcd.clear(0x000000)
        sprite = M5.Lcd.newCanvas(320, 160, 16, True)

        fw = framework.Framework()
        dev_app = apps.DevApp(sprite, data=self._wlan)
        fw.install_bar(apps.StatusBarApp(None, self._wlan))
        fw.install_launcher(dev_app)
        fw.install(apps.SettingsApp(sprite, data=self._wlan))
        fw.install(dev_app)
        fw.install(apps.RunApp(None))
        fw.install(apps.ListApp(sprite))
        fw.install(apps.EzDataApp(sprite))
        fw.start()
