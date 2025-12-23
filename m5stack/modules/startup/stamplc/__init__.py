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


class StampPLC_Startup:
    def __init__(self) -> None:
        pass

    def startup(
        self,
        net_mode: str = "WIFI",
        ssid: str = "",
        pswd: str = "",
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self._net_if = Startup(network_type=net_mode)  # type: ignore
        if net_mode == "WIFI":
            self._net_if.connect_network(
                ssid, pswd, protocol=protocol, ip=ip, netmask=netmask, gateway=gateway, dns=dns
            )
        elif net_mode == "ETH":
            from stamplc import PoEStamPLC

            lan_if = PoEStamPLC()
            self._net_if.connect_network(ssid, pswd, lan_if, protocol, ip, netmask, gateway, dns)

        # M5.Lcd.setRotation(0)
        # M5.Lcd.drawImage(LOGO_IMG)
        time.sleep_ms(200)
        M5.Lcd.clear(0x333333)

        fw = framework.Framework()
        setting_app = SettingsApp(None, data=self._net_if)
        dev_app = DevApp(None, data=self._net_if)
        launcher = LauncherApp()
        run_app = RunApp(None, data=self._net_if)
        list_app = ListApp(None, data=self._net_if)
        ezdata_app = EzDataApp(None, data=self._net_if)
        fw.install_bar(StatusBarApp(None, self._net_if))
        fw.install_launcher(launcher)
        fw.install(launcher)
        fw.install(setting_app)
        fw.install(dev_app)
        fw.install(run_app)
        fw.install(list_app)
        fw.install(ezdata_app)
        fw.start()
