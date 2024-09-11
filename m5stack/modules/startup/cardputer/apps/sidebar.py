# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
import M5


class SidebarApp(app_base.AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        return super().on_launch()

    def on_view(self):
        M5.Lcd.fillRoundRect(2, 4, 28, 127, 15, 0xC4C4C4)
        M5.Lcd.drawImage(res.Aa0_IMG, 5, 20)
        M5.Lcd.drawImage(res.FN0_IMG, 5, 39)
        M5.Lcd.drawImage(res.CTRL0_IMG, 5, 58)
        M5.Lcd.drawImage(res.OPT0_IMG, 5, 77)
        M5.Lcd.drawImage(res.ALT0_IMG, 5, 96)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_key(self, state):
        if state.shift:
            M5.Lcd.drawImage(res.Aa_IMG, 5, 20)
        else:
            M5.Lcd.drawImage(res.Aa0_IMG, 5, 20)

        if state.fn:
            M5.Lcd.drawImage(res.FN_IMG, 5, 39)
        else:
            M5.Lcd.drawImage(res.FN0_IMG, 5, 39)

        if state.ctrl:
            M5.Lcd.drawImage(res.CTRL_IMG, 5, 58)
        else:
            M5.Lcd.drawImage(res.CTRL0_IMG, 5, 58)

        if state.opt:
            M5.Lcd.drawImage(res.OPT_IMG, 5, 77)
        else:
            M5.Lcd.drawImage(res.OPT0_IMG, 5, 77)

        if state.alt:
            M5.Lcd.drawImage(res.ALT_IMG, 5, 96)
        else:
            M5.Lcd.drawImage(res.ALT0_IMG, 5, 96)
