# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app
import M5
from M5 import Widgets
import sys
import machine
import os
import time
import boot_option
from .. import res


try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class RunApp(app.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage(res.APPRUN_UNSELECTED_IMG, 5 + 62 * 2, 0)

    def on_launch(self):
        self._mtime_text, self._account_text, self._ver_text = self._get_file_info("main.py")

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 56
        M5.Lcd.drawImage(res.APPRUN_SELECTED_IMG, 5 + 62 * 2, 0)
        M5.Lcd.fillRect(self._origin_x, self._origin_y, 320, 184, 0x000000)
        M5.Lcd.drawImage(res.RUN_IMG, self._origin_x + 4, self._origin_y + 4)
        M5.Lcd.drawImage(res.BAR4_IMG, self._origin_x, 220)

        # file name
        M5.Lcd.setFont(Widgets.FONTS.DejaVu18)
        M5.Lcd.setTextColor(0x000000, 0xEEEEEF)
        M5.Lcd.drawString("main.py", 4 + 10, self._origin_y + 4 + 4)

        M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
        M5.Lcd.setTextColor(0x000000, 0xDCDDDD)
        M5.Lcd.drawString(self._mtime_text, 4 + 10 + 8, self._origin_y + 4 + 4 + 20 + 6)

        M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
        M5.Lcd.setTextColor(0x000000, 0xDCDDDD)
        M5.Lcd.drawString(self._account_text, 4 + 10 + 8, self._origin_y + 4 + 4 + 20 + 6 + 18)

        M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
        M5.Lcd.setTextColor(0x000000, 0xDCDDDD)
        M5.Lcd.drawString(self._ver_text, 4 + 10 + 8, self._origin_y + 4 + 4 + 20 + 6 + 18 + 18)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage(res.APPRUN_UNSELECTED_IMG, 5 + 62 * 2, 0)
        del self._origin_x, self._origin_y
        del self._mtime_text, self._account_text, self._ver_text

    # async def _btna_event_handler(self, fw):
    #     # print("_btna_event_handler")
    #     pass

    async def _btnb_event_handler(self, fw):
        # print("_btnb_event_handler")
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        sys.exit(0)

    async def _btnc_event_handler(self, fw):
        # print("_btnc_event_handler")
        boot_option.set_boot_option(2)
        machine.reset()

    @staticmethod
    def _get_file_info(path) -> tuple(str, str, str):
        mtime = None
        account = None
        ver = None

        try:
            stat = os.stat(path)
            mtime = time.localtime(stat[8])
        except OSError:
            pass

        if mtime is None or mtime[0] < 2023 and mtime[1] < 9:
            mtime = "Time: ----/--/-- --:--:--"
        else:
            mtime = "Time: {:04d}/{:d}/{:d} {:02d}:{:02d}:{:02d}".format(
                mtime[0], mtime[1], mtime[2], mtime[3], mtime[4], mtime[5]
            )

        # with open(path, "r") as f:
        #     for line in f:
        #         if line.find("Account") != -1:
        #             account = line.split(":")[1].strip()
        #         if line.find("Ver") != -1:
        #             ver = line.split(":")[1].strip()
        #         if account is not None and ver is not None:
        #             break

        if account is None and _HAS_SERVER and M5Things.status() == 2:
            infos = M5Things.info()
            account = "Account: None" if len(infos[1]) == 0 else "Account: {:s}".format(infos[1])
        else:
            account = "Account: None"

        if ver is None:
            ver = "Ver: None"

        return (mtime, account, ver)
