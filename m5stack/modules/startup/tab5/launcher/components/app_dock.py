# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal
from ..apps.app import AppManager
from ..common import IMAGE_SUFFIX, IconIndicator
import lvgl as lv


class AppIcon:
    def __init__(self, pos_x: int, pos_y: int, app_name: str, icon_name: str):
        self._app_name = app_name
        self._icon_pos_x = pos_x

        img = lv.image(lv.screen_active())
        img.set_src(get_hal().get_asset_path("icons/" + icon_name + IMAGE_SUFFIX))
        img.align(lv.ALIGN.TOP_LEFT, pos_x, pos_y)
        img.add_flag(lv.obj.FLAG.CLICKABLE)
        img.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)

    def _on_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        IconIndicator.create_indicator(e.get_target_obj())
        AppManager.open_app(self._app_name)


class AppDock:
    def __init__(self):
        # UIFlow app list
        self._app_app_list = AppIcon(1046, 35, "AppList", "app_list")

        # Tools
        tools = [
            ("ADC", "adc"),
            ("GPIO", "gpio"),
            ("UART", "uart"),
            ("WifiScan", "wifi_scan"),
            ("I2CScan", "i2c_scan"),
        ]
        self._tools = {}
        for i, (tool_name, icon_name) in enumerate(tools):
            x = 481 + i * 110
            self._tools[tool_name] = AppIcon(x, 35, tool_name, icon_name)
