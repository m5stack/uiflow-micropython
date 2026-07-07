# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import M5


_MESSAGE = "Coming soon ..."
_FONT = M5.Lcd.FONTS.Montserrat24
_CONTENT_W = 320
_CONTENT_H = 160
_TEXT_COLOR = 0x008FD7
_BG_COLOR = 0xEEEEEF


def _draw_center_message(parent):
    parent.setFont(_FONT)
    parent.setTextColor(_TEXT_COLOR, _BG_COLOR)
    text_x = (_CONTENT_W - parent.textWidth(_MESSAGE)) // 2
    text_y = (_CONTENT_H - parent.fontHeight()) // 2
    parent.drawString(_MESSAGE, text_x, text_y)


class EzDataApp(app_base.AppBase):
    def __init__(self, icos) -> None:
        self._lcd = icos
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage("/system/stackchan/Selection/ezdata_unselected.png", 5 + 62 * 4, 20 + 4)
        self.descriptor = app_base.Descriptor(x=5 + 62 + 62 + 62 + 62, y=20 + 4, w=62, h=56)

    def on_view(self):
        M5.Lcd.drawImage("/system/stackchan/Selection/ezdata_selected.png", 5 + 62 * 4, 20 + 4)

        self._origin_x = 0
        self._origin_y = 80
        self._lcd.clear()
        _draw_center_message(self._lcd)
        self._lcd.push(self._origin_x, self._origin_y)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage("/system/stackchan/Selection/ezdata_unselected.png", 5 + 62 * 4, 20 + 4)
        self._lcd.clear()
        self._lcd.push(self._origin_x, self._origin_y)

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass
