# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .apps import (
    AppManager,
    AppWifi,
    AppAppList,
    AppI2cScan,
    AppWifiScan,
    AppUart,
    AppGpio,
    AppAdc,
    AppEzdata,
    AppEzdataSettings,
)
from .components import StatusBar, AppDock, EzdataDock
from .common import Ezdata
import lvgl as lv
import asyncio
import M5


class Launcher:
    def __init__(self):
        self._init_background()
        self._create_app_panel()

        # Create main loop
        asyncio.run(self._main())

    def _init_background(self):
        screen = lv.screen_active()
        screen.set_style_bg_color(lv.color_hex(0x4D4D4D), lv.PART.MAIN)

        self._bottom_bar = lv.obj(screen)
        self._bottom_bar.set_size(lv.pct(100), 35)
        self._bottom_bar.set_style_bg_color(lv.color_hex(0x008FD7), lv.PART.MAIN)
        self._bottom_bar.set_style_radius(0, lv.PART.MAIN)
        self._bottom_bar.set_style_border_width(0, lv.PART.MAIN)
        self._bottom_bar.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self._bottom_bar.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self._bottom_bar.set_style_pad_left(12, lv.PART.MAIN)

        self._bottom_label = lv.label(self._bottom_bar)
        self._bottom_label.set_text("UIFLOW2")
        self._bottom_label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        self._bottom_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._bottom_label.align(lv.ALIGN.LEFT_MID, 0, 0)

        self._divider_1 = lv.obj(screen)
        self._divider_1.set_size(5, 120)
        self._divider_1.set_style_bg_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN)
        self._divider_1.align(lv.ALIGN.TOP_RIGHT, -245, 25)
        self._divider_1.set_style_radius(0, lv.PART.MAIN)
        self._divider_1.set_style_border_width(0, lv.PART.MAIN)

        self._divider_2 = lv.obj(screen)
        self._divider_2.set_size(5, 120)
        self._divider_2.set_style_bg_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN)
        self._divider_2.align(lv.ALIGN.TOP_RIGHT, -810, 25)
        self._divider_2.set_style_radius(0, lv.PART.MAIN)
        self._divider_2.set_style_border_width(0, lv.PART.MAIN)

        self._label_dock_uiflow = lv.label(screen)
        self._label_dock_uiflow.set_text("UIFLOW")
        self._label_dock_uiflow.set_style_text_font(lv.font_montserrat_22, lv.PART.MAIN)
        self._label_dock_uiflow.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._label_dock_uiflow.align(lv.ALIGN.TOP_MID, 457, 6)

        self._label_dock_tools = lv.label(screen)
        self._label_dock_tools.set_text("TOOLS")
        self._label_dock_tools.set_style_text_font(lv.font_montserrat_22, lv.PART.MAIN)
        self._label_dock_tools.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._label_dock_tools.align(lv.ALIGN.TOP_MID, -110, 6)

        self._label_dock_ezdata = lv.label(screen)
        self._label_dock_ezdata.set_text("EzData")
        self._label_dock_ezdata.set_style_text_font(lv.font_montserrat_22, lv.PART.MAIN)
        self._label_dock_ezdata.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._label_dock_ezdata.align(lv.ALIGN.TOP_MID, -565, 6)

    def _create_app_panel(self):
        self._app_panel = lv.obj(lv.screen_active())
        self._app_panel.set_size(1150, 520)
        self._app_panel.set_style_radius(10, lv.PART.MAIN)
        self._app_panel.set_style_bg_color(lv.color_hex(0xF6F6F6), lv.PART.MAIN)
        self._app_panel.set_style_border_width(0, lv.PART.MAIN)
        self._app_panel.align(lv.ALIGN.CENTER, -55, 55)
        self._app_panel.set_style_pad_all(10, lv.PART.MAIN)

    async def _main(self):
        # Set a lvgl object as app panel
        AppManager.set_app_panel(self._app_panel)

        # Install apps
        AppManager.install_app("Wifi", AppWifi)
        AppManager.install_app("AppList", AppAppList)
        AppManager.install_app("I2CScan", AppI2cScan)
        AppManager.install_app("WifiScan", AppWifiScan)
        AppManager.install_app("UART", AppUart)
        AppManager.install_app("GPIO", AppGpio)
        AppManager.install_app("ADC", AppAdc)
        AppManager.install_app("EzData", AppEzdata)
        AppManager.install_app("EzDataSettings", AppEzdataSettings)

        # Create components
        self._status_bar = StatusBar()
        self._ezdata_dock = EzdataDock()
        self._app_dock = AppDock()

        # Start ezdata service
        Ezdata.start()

        try:
            # Keep app manager running
            while True:
                await asyncio.sleep_ms(50)
                await AppManager.update()
        except KeyboardInterrupt:
            M5.Lcd.lvgl_deinit()
