# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase
import M5
from widgets.label import Label
from widgets.button import Button
import esp32
import sys
import machine
import os
import time
from ..res import RUN_IMG
from .status_bar import StatusBarApp

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class RunApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._mtime_text, self._account_text, self._ver_text = self._get_file_info("main.py")

    def on_view(self):
        M5.Lcd.drawImage(RUN_IMG, 0, 0)

        self._name_label = Label(
            "name",
            10,
            105,
            w=220,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font="/system/common/font/Montserrat-Medium-18.vlw",
        )
        self._name_label.set_text("main.py")

        self._mtime_label = Label(
            "Time: 2023/5/14 12:23:43",
            120,
            137,
            w=200,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._mtime_label.set_text(self._mtime_text)

        self._account_label = Label(
            "Account: XXABC",
            120,
            162,
            w=180,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._account_label.set_text(self._account_text)

        self._ver_label = Label(
            "Ver: UIFLOW2.0 a18",
            120,
            187,
            w=160,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._ver_label.set_text(self._ver_text)

        _button_run_once = Button(None)
        _button_run_once.set_pos(0, 50)
        _button_run_once.set_size(120, 51)
        _button_run_once.add_event(self._handle_run_once)

        _button_run_always = Button(None)
        _button_run_always.set_pos(120, 50)
        _button_run_always.set_size(120, 51)
        _button_run_always.add_event(self._handle_run_always)
        self._buttons = (_button_run_once, _button_run_always)

    def on_ready(self):
        self._status_bar = StatusBarApp(None, self._wlan)
        self._status_bar.start()

    def on_hide(self):
        self._status_bar.stop()

    def on_exit(self):
        del (
            self._name_label,
            self._mtime_label,
            self._account_label,
            self._ver_label,
        )

    async def _click_event_handler(self, x, y, fw):
        for button in self._buttons:
            if button.handle(x, y):
                break

    def _handle_run_once(self, fw):
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        sys.exit(0)

    def _handle_run_always(self, fw):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 2)
        nvs.commit()
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

        if ver is None:
            ver = "Ver: None"

        return (mtime, account, ver)
