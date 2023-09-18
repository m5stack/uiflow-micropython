from ..app import AppBase
import M5
from widgets.label import Label
from common.font import MontserratMedium16
from common.font import MontserratMedium18
import esp32
import sys
import machine
import os
import time

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class RunApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage("/system/fire/appRun_unselected.png", 5 + 62 * 2, 0)

    def on_launch(self):
        self._mtime_text, self._account_text, self._ver_text = self._get_file_info("main.py")

    def on_view(self):
        # M5.Lcd.clear()
        # M5.Lcd.drawImage("/system/fire/setting_unselected.png", 5 + 62 * 0, 0)
        # M5.Lcd.drawImage("/system/fire/develop_unselected.png", 5 + 62 * 1, 0)
        M5.Lcd.drawImage("/system/fire/appRun_selected.png", 5 + 62 * 2, 0)
        # M5.Lcd.drawImage("/system/fire/appList_unselected.png", 5 + 62 * 3, 0)
        # M5.Lcd.drawImage("/system/fire/ezdata_unselected.png", 5 + 62 * 4, 0)

        M5.Lcd.drawImage("/system/fire/run.png", 4, 56 + 4)
        M5.Lcd.drawImage("/system/fire/bar4.png", 0, 220)

        self._name_label = Label(
            "name",
            4 + 10,
            (56 + 4) + 4,
            w=312,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )
        self._name_label.setText("main.py")

        self._mtime_label = Label(
            "Time: 2023/5/14 12:23:43",
            4 + 10 + 8,
            (56 + 4) + 4 + 20 + 6,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium16.FONT,
        )
        self._mtime_label.setText(self._mtime_text)

        self._account_label = Label(
            "Account: XXABC",
            4 + 10 + 8,
            (56 + 4) + 4 + 20 + 6 + 18,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium16.FONT,
        )
        self._account_label.setText(self._account_text)

        self._ver_label = Label(
            "Ver: UIFLOW2.0 a18",
            4 + 10 + 8,
            (56 + 4) + 4 + 20 + 6 + 18 + 18,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium16.FONT,
        )
        self._ver_label.setText(self._ver_text)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage("/system/fire/appRun_unselected.png", 5 + 62 * 2, 0)
        del self._name_label, self._mtime_label, self._account_label, self._ver_label

    async def _btna_event_handler(self, fw):
        # print("_btna_event_handler")
        pass

    async def _btnb_event_handler(self, fw):
        # print("_btnb_event_handler")
        execfile("main.py")
        sys.exit(0)

    async def _btnc_event_handler(self, fw):
        # print("_btnc_event_handler")
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

        if mtime == None or mtime[0] < 2023 and mtime[1] < 9:
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
                if account != None and ver != None:
                    break

        if account == None and _HAS_SERVER and M5Things.status() is 2:
            infos = M5Things.info()
            account = "Account: None" if len(infos[1]) is 0 else "Account: {:s}".format(infos[1])
        else:
            account = "Account: None"

        if ver == None:
            ver = "Ver: None"

        return (mtime, account, ver)
