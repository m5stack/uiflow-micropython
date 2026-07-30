# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import layout
import M5
import widgets
import esp32


class SettingsApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wifi = data
        super().__init__()

    def on_install(self):
        tab_x = 470 if layout.IS_PAPERMONO else 493
        tab_w = 100 if layout.IS_PAPERMONO else 48
        self.descriptor = app_base.Descriptor(
            x=layout.x(tab_x),
            y=layout.y(164),
            w=layout.size(tab_w),
            h=layout.size(181),
        )

    def on_launch(self):
        self.get_data()

    def on_view(self):
        layout.draw_background(layout.resource_path("config.png"))
        ssid_y = 620 if layout.IS_PAPERMONO else 630
        server_y = 737 if layout.IS_PAPERMONO else 747

        self._ssid_label = widgets.Label(
            "ssid",
            layout.x(87),
            layout.y(ssid_y),
            w=layout.size(333),
            h=layout.size(30),
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=layout.DYNAMIC_BG_COLOR,
            font=layout.settings_font(),
            parent=self._lcd,
        )
        self._ssid_label.set_long_mode(widgets.Label.LONG_DOT)
        self._ssid_label.set_text(self.ssid)

        self._server_label = widgets.Label(
            "server",
            layout.x(87),
            layout.y(server_y),
            w=layout.size(333),
            h=layout.size(30),
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=layout.DYNAMIC_BG_COLOR,
            font=layout.settings_font(),
            parent=self._lcd,
        )
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)
        self._server_label.set_text(self.server)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass

    async def _click_event_handler(self, x, y, fw):
        pass

    async def _kb_event_handler(self, event, fw):
        pass

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        self.ssid = self.nvs.get_str("ssid0")
        self.psk = self.nvs.get_str("pswd0")
        self.server = self.nvs.get_str("server")
        self.ssid_tmp = self.ssid
        self.psk_tmp = self.psk
        self.server_tmp = self.server
