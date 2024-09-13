# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import M5
from .. import res
from . import status_bar


class EzDataApp(app_base.AppBase):
    def __init__(self, icos, data=None) -> None:
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_view(self):
        M5.Lcd.clear()
        M5.Lcd.drawImage(res.EZDATA_IMG, 0, 0)

    def on_ready(self):
        self._status_bar = status_bar.StatusBarApp(None, self._wlan)
        self._status_bar.start()

    def on_hide(self):
        self._status_bar.stop()

    def on_exit(self):
        M5.Lcd.clear()

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass
