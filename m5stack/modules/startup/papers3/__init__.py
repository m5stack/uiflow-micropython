# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup
import M5
import time


if M5.getBoard() == M5.BOARD.M5PaperMono:
    from M5 import Widgets

    M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)
    Widgets.setRotation(0)
    Widgets.fillScreen(0xFFFFFF)
    print(
        "PaperMono startup display: {}x{}, rotation={}".format(
            M5.Display.width(), M5.Display.height(), M5.Display.getRotation()
        )
    )

from . import framework
from . import layout

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
        layout.set_full_refresh_mode()
        layout.draw_background(layout.resource_path("startup.png"))
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
        if layout.IS_PAPERMONO:
            from .apps.power_off import PowerOffButton

            fw.install_overlay(PowerOffButton(M5.Lcd))
        fw.start()
