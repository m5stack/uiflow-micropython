# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
import widgets
import M5
import esp32
import machine
import sys
import os
import time

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class RunApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()
        self._enter_handler = self._handle_run_once

    def on_install(self):
        pass

    def on_launch(self):
        self._mtime_text, self._account_text, self._ver_text = self._get_file_info("main.py")

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)
        M5.Lcd.drawImage(res.RUN_INFO_IMG, 6, 22)

        self._name_label = widgets.Label(
            "name",
            16,
            23,
            w=208,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCDCDCD,
            font=res.MontserratMedium16_VLW,
        )
        self._name_label.set_text("main.py")

        self._mtime_label = widgets.Label(
            "Time: 2023/5/14 12:23:43",
            16,
            46,
            w=208,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._mtime_label.set_text(self._mtime_text)

        self._account_label = widgets.Label(
            "Account: XXABC",
            16,
            60,
            w=208,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._account_label.set_text(self._account_text)

        self._ver_label = widgets.Label(
            "Ver: UIFLOW2.0 a18",
            16,
            74,
            w=208,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._ver_label.set_text(self._ver_text)

        M5.Lcd.drawImage(res.RUN_ONCE_SELECT_IMG, 6, 100)
        M5.Lcd.drawImage(res.RUN_ALWAYS_UNSELECT_IMG, 123, 100)

    def on_ready(self):
        pass

    def on_hide(self):
        self._enter_handler = self._handle_run_once
        M5.Lcd.fillRect(32, 26, 206, 103, 0xEEEEEF)

    def on_exit(self):
        del (
            self._name_label,
            self._mtime_label,
            self._account_label,
            self._ver_label,
        )

    def _handle_run_once(self, fw):
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    def _handle_run_always(self, fw):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 2)
        nvs.commit()
        machine.reset()

    @staticmethod
    def _get_file_info(path) -> tuple(str, str, str):
        mtime = None
        account = None
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
                if line.find("Account") != -1:
                    account = line.split(":")[1].strip()
                if line.find("Ver") != -1:
                    ver = line.split(":")[1].strip()
                if account is not None and ver is not None:
                    break

        if account is None and _HAS_SERVER and M5Things.status() == 2:
            infos = M5Things.info()
            account = "Account: None" if len(infos[1]) == 0 else "Account: {:s}".format(infos[1])
        else:
            account = "Account: None"

        return (mtime, account, ver)

    async def _kb_event_handler(self, event, fw):
        if event.key == 183:  # Right key
            M5.Lcd.drawImage(res.RUN_ONCE_UNSELECT_IMG, 6, 100)
            M5.Lcd.drawImage(res.RUN_ALWAYS_SELECT_IMG, 123, 100)
            self._enter_handler = self._handle_run_always
        elif event.key == 180:  # Left key
            M5.Lcd.drawImage(res.RUN_ONCE_SELECT_IMG, 6, 100)
            M5.Lcd.drawImage(res.RUN_ALWAYS_UNSELECT_IMG, 123, 100)
            self._enter_handler = self._handle_run_once
        elif event.key == 0x0D:  # Enter key
            self._enter_handler(fw)
