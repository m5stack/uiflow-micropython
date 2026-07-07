# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import M5
import widgets
import esp32
import sys
import machine
import os
import time
from .. import res


class RunApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage(res.APPRUN_UNSELECTED_IMG, 5 + 62 * 2, 0)

    def on_launch(self):
        self._mtime_text, self._ver_text = self._get_file_info("main.py")

    def on_view(self):
        M5.Lcd.drawImage(res.APPRUN_SELECTED_IMG, 5 + 62 * 2, 0)

        M5.Lcd.drawImage(res.RUN_IMG, 4, 56 + 4)
        M5.Lcd.drawImage(res.BAR4_IMG, 0, 220)

        self._name_label = widgets.Label(
            "name",
            4 + 10,
            (56 + 4) + 4,
            w=312,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font="/system/common/font/Montserrat-Medium-18.vlw",
        )
        self._name_label.set_text("main.py")

        self._mtime_label = widgets.Label(
            "Time: 2023/5/14 12:23:43",
            4 + 10 + 8,
            (56 + 4) + 4 + 20 + 6,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._mtime_label.set_text(self._mtime_text)

        self._ver_label = widgets.Label(
            "Ver: UIFLOW2.0 a18",
            4 + 10 + 8,
            (56 + 4) + 4 + 20 + 6 + 18,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._ver_label.set_text(self._ver_text)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage(res.APPRUN_UNSELECTED_IMG, 5 + 62 * 2, 0)
        del self._name_label, self._mtime_label, self._ver_label

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    async def _btnc_event_handler(self, fw):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 2)
        nvs.commit()
        machine.reset()

    @staticmethod
    def _get_file_info(path):
        mtime = None
        ver = f"Ver: UIFLOW2 {esp32.firmware_info()[3]}"

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

        with open(path, "r") as f:
            for line in f:
                if line.find("Ver") != -1:
                    ver = line.split(":")[1].strip()
                    break

        return (mtime, ver)
