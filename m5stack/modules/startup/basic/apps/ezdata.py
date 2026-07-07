# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
import M5


_MESSAGE = "Coming soon..."
_FONT = M5.Lcd.FONTS.Montserrat24
_CONTENT_W = 320
_CONTENT_H = 184


def _draw_center_message(parent, x, y, w, h):
    parent.setFont(_FONT)
    parent.setTextColor(0x008FD7, 0x000000)
    text_x = x + (w - parent.textWidth(_MESSAGE)) // 2
    text_y = y + (h - parent.fontHeight()) // 2
    parent.drawString(_MESSAGE, text_x, text_y)


class EzDataApp(app_base.AppBase):
    def __init__(self, icos) -> None:
        self._lcd = icos
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage(res.EZDATA_UNSELECTED_IMG, 5 + 62 * 4, 0)

    def on_view(self):
        M5.Lcd.drawImage(res.EZDATA_SELECTED_IMG, 5 + 62 * 4, 0)

        self._origin_x = 0
        self._origin_y = 56
        M5.Lcd.fillRect(self._origin_x, self._origin_y, _CONTENT_W, _CONTENT_H, 0x000000)
        _draw_center_message(M5.Lcd, self._origin_x, self._origin_y, _CONTENT_W, _CONTENT_H)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage(res.EZDATA_UNSELECTED_IMG, 5 + 62 * 4, 0)
        del self._origin_x, self._origin_y

    # async def _btna_event_handler(self, fw):
    #     pass

    # async def _btnb_event_handler(self, fw):
    #     pass

    # async def _btnc_event_handler(self, fw):
    #     pass
