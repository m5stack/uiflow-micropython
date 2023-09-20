from startup import Startup
from .framework import Framework

from .apps.status_bar import StatusBarApp
from .apps.settings import SettingsApp
from .apps.dev import DevApp
from .apps.app_run import RunApp
from .apps.app_list import ListApp
from .apps.ezdata import EzDataApp
import M5

import time


class CoreS3_Startup:
    def __init__(self) -> None:
        self._wlan = Startup()
        # self._status_bar = StatusBarApp(None, self._wifi)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wlan.connect_network(ssid, pswd)
        M5.Lcd.drawImage("/system/cores3/boot.png", 0, 0)
        time.sleep(0.2)

        M5.Lcd.clear(0x000000)
        sprite = M5.Lcd.newCanvas(320, 160, 16, True)

        fw = Framework()
        settings_app = SettingsApp(sprite, data=self._wlan)
        dev_app = DevApp(sprite, data=self._wlan)
        run_app = RunApp(None)
        list_app = ListApp(sprite)
        fw.install_bar(StatusBarApp(None, self._wlan))
        fw.install_launcher(dev_app)
        fw.install(settings_app)
        fw.install(dev_app)
        fw.install(run_app)
        fw.install(list_app)
        fw.install(EzDataApp(sprite))
        fw.start()
