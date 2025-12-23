# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import framework
from .apps.settings import SettingsApp
from .apps.dev import DevApp
from .apps.launcher import LauncherApp
from .apps.app_run import RunApp
from .apps.app_list import ListApp
from .apps.statusbar import StatusBarApp
from .apps.ezdata import EzDataApp
from startup import Startup
import M5
import time

# from .res import LOGO_IMG


class CardputerADV_Startup:
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
        M5.Speaker.setVolume(60)
        M5.Speaker.tone(4000, 50)
        M5.Lcd.setRotation(1)
        # M5.Lcd.drawImage(LOGO_IMG)
        time.sleep_ms(200)

        M5.Lcd.clear(0x333333)
        fw = framework.Framework()
        # sidebar = SidebarApp()
        setting_app = SettingsApp(None, data=self._wlan)
        dev_app = DevApp(None, data=self._wlan)
        launcher = LauncherApp()
        run_app = RunApp(None, data=self._wlan)
        list_app = ListApp(None, data=self._wlan)
        ezdata_app = EzDataApp(None, data=self._wlan)
        fw.install_bar(StatusBarApp(None, self._wlan))
        # fw.install_sidebar(sidebar)
        fw.install_launcher(launcher)
        fw.install(launcher)
        fw.install(setting_app)
        fw.install(dev_app)
        fw.install(run_app)
        fw.install(list_app)
        fw.install(ezdata_app)
        fw.start()
