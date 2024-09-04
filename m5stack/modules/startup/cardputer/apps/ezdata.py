# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app
from .. import res
import widgets
import M5


class EzDataApp(app.AppBase):
    def __init__(self, icos, data=None) -> None:
        super().__init__()

    def on_install(self):
        pass

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)
        self._text_label = widgets.Label(
            "aabbcc112233",
            120,
            69,
            w=240,
            h=22,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=res.MontserratMedium18_VLW,
        )
        self._text_label.set_text("Please stay tuned")

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass
