# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup
import M5
from .framework import Framework
from .apps.settings import SettingsApp, WiFiSetting
from .apps.dev import DevApp
from .apps.app_run import RunApp
from .apps.app_list import ListApp

# from .apps.ezdata import EzDataApp
import time
from .res import LOGO_IMG


class Dial_Startup:
    def __init__(self) -> None:
        self._wlan = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wlan.connect_network(ssid, pswd)
        M5.Speaker.setVolume(80)
        M5.Speaker.tone(4000, 50)

        M5.Lcd.drawImage(LOGO_IMG)
        time.sleep_ms(200)

        fw = Framework()
        wifi_app = WiFiSetting(None, data=self._wlan)
        setting_app = SettingsApp(None, data=self._wlan)
        dev_app = DevApp(None, data=self._wlan)
        run_app = RunApp(None, data=self._wlan)
        list_app = ListApp(None, data=self._wlan)
        # ezdata_app = EzDataApp(None, data=self._wlan)
        fw.install_launcher(dev_app)
        fw.install(wifi_app)
        fw.install(setting_app)
        fw.install(dev_app)
        fw.install(run_app)
        fw.install(list_app)
        # fw.install(ezdata_app)
        fw.start()
