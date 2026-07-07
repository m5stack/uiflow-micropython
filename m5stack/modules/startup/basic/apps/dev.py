# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
import M5
from M5 import Widgets
import widgets
import asyncio
import binascii
from startup import print_access_info
import machine
import network


try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

NETWORK_STATUS_INIT = 0
NETWORK_STATUS_RSSI_GOOD = 1
NETWORK_STATUS_RSSI_MID = 2
NETWORK_STATUS_RSSI_WORSE = 3
NETWORK_STATUS_DISCONNECTED = 4

CLOUD_STATUS_INIT = 0
CLOUD_STATUS_CONNECTED = 1
CLOUD_STATUS_DISCONNECTED = 2


_NETWORK_STATUS_ICOS = {
    NETWORK_STATUS_INIT: res.WIFI_EMPTY_IMG,
    NETWORK_STATUS_RSSI_GOOD: res.WIFI_GOOD_IMG,
    NETWORK_STATUS_RSSI_MID: res.WIFI_MID_IMG,
    NETWORK_STATUS_RSSI_WORSE: res.WIFI_WORSE_IMG,
    NETWORK_STATUS_DISCONNECTED: res.WIFI_DISCONNECTED_IMG,
}

_CLOUD_STATUS_ICOS = {
    CLOUD_STATUS_INIT: res.SERVER_EMPTY_IMG,
    CLOUD_STATUS_CONNECTED: res.SERVER_GREEN_IMG,
    CLOUD_STATUS_DISCONNECTED: res.SERVER_ERROR_IMG,
}

_BG_COLOR = 0xEEEEEF
_LABEL_COLOR = 0x008FD7
_VALUE_COLOR = 0x000000
_TEXT_PANEL_W = 181


class DevApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wifi = data
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage(res.DEVELOP_UNSELECTED_IMG, 5 + 62 * 1, 0)

    def on_launch(self):
        self._state = self._collect_state()
        self._status_bar_src = self._get_bar_src()
        self._network_status = self._get_network_status()
        self._cloud_status = self._get_cloud_status()
        self._battery_src = self._get_battery_src(
            M5.Power.getBatteryLevel(), M5.Power.isCharging()
        )
        self._battery_text = self._get_battery_text(M5.Power.getBatteryLevel())

    def on_view(self):
        M5.Lcd.drawImage(res.DEVELOP_SELECTED_IMG, 5 + 62 * 1, 0)
        self._origin_x = 0
        self._origin_y = 56

        M5.Lcd.fillRect(self._origin_x, self._origin_y, 320, 184, 0x000000)

        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(self._origin_x + 4, self._origin_y + 4)
        self._bg_img.set_size(312, 156)
        self._bg_img.set_src(res.DEVELOP_BG_IMG)
        M5.Lcd.fillRect(4, self._origin_y + 4, _TEXT_PANEL_W, 156, _BG_COLOR)

        self._mac_label, self._mac_value = self._create_row("Device MAC:", 8)
        self._code_label, self._code_value = self._create_row("Access Code:", 59)
        self._nick_label, self._nick_value = self._create_row("Nickname:", 110)

        self._set_value(self._mac_value, self._state.get("mac", "-"))
        self._set_value(self._code_value, self._state.get("access_code", ""), fallback="")
        self._set_value(self._nick_value, self._state.get("nick_name", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

        self._bar_img = widgets.Image(use_sprite=False)
        self._bar_img.set_pos(0, self._origin_y + 164)
        self._bar_img.set_size(320, 20)
        self._bar_img.set_src(self._status_bar_src)

        self._network_img = widgets.Image(use_sprite=False)
        self._network_img.set_pos(320 - 56 - 20 - 5 - 20 - 5, self._origin_y + 164)
        self._network_img.set_size(20, 20)
        self._network_img.set_src(_NETWORK_STATUS_ICOS[self._network_status])

        self._cloud_img = widgets.Image(use_sprite=False)
        self._cloud_img.set_pos(320 - 56 - 20 - 5, self._origin_y + 164)
        self._cloud_img.set_size(20, 20)
        self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])

        self._battery_img = widgets.Image(use_sprite=False)
        self._battery_img.set_pos(320 - 56, self._origin_y + 164)
        self._battery_img.set_size(56, 20)
        self._battery_img.set_src(self._battery_src)

        self._battery_label = widgets.Label(
            "0%",
            320 - 56 + 22,
            220 + 6,
            w=22,
            h=10,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.Montserrat12,
        )
        self._battery_label.set_text(self._battery_text)

    async def on_run(self):
        refresh_bar = False
        while True:
            new_state = self._collect_state()

            if new_state["access_code"] != self._state.get("access_code"):
                self._state["access_code"] = new_state["access_code"]
                self._set_value(self._code_value, new_state["access_code"], fallback="")
                print_access_info(self._state.get("nick_name", ""), new_state["access_code"])

            if new_state["nick_name"] != self._state.get("nick_name"):
                self._state["nick_name"] = new_state["nick_name"]
                self._set_value(self._nick_value, new_state["nick_name"], fallback="")
                print_access_info(new_state["nick_name"], self._state.get("access_code", ""))

            t = self._get_bar_src()
            if t != self._status_bar_src:
                self._status_bar_src = t
                self._bar_img.set_src(self._status_bar_src)
                refresh_bar = True

            t = self._get_network_status()
            if t != self._network_status:
                self._network_status = t
                self._network_img.set_src(_NETWORK_STATUS_ICOS[self._network_status])
            elif refresh_bar:
                self._network_img._draw(False)

            t = self._get_cloud_status()
            if t != self._cloud_status:
                self._cloud_status = t
                self._cloud_img.set_src(_CLOUD_STATUS_ICOS[self._cloud_status])
            elif refresh_bar:
                self._cloud_img._draw(False)

            t = self._get_battery_src(M5.Power.getBatteryLevel(), M5.Power.isCharging())
            if t != self._battery_src:
                self._battery_src = t
                self._battery_img.set_src(self._battery_src)
            elif refresh_bar:
                self._battery_img._draw(False)

            t = self._get_battery_text(M5.Power.getBatteryLevel())
            if t != self._battery_text or refresh_bar:
                self._battery_text = t
                self._battery_label.set_text(self._battery_text)

            refresh_bar = False
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        # if hasattr(self, "_dl_task"):
        #     self._dl_task.cancel()
        self._task.cancel()

    def on_exit(self):
        M5.Lcd.drawImage(res.DEVELOP_UNSELECTED_IMG, 5 + 62 * 1, 0)
        del (self._bg_img,)
        del (self._mac_label,)
        del (self._mac_value,)
        del (self._code_label,)
        del (self._code_value,)
        del (self._nick_label,)
        del (self._nick_value,)
        del (self._bar_img,)
        del (self._network_img,)
        del (self._cloud_img,)
        del (self._battery_img,)
        del (self._battery_label,)
        del (self._origin_x,)
        del (self._origin_y,)
        del (self._status_bar_src,)
        del (self._network_status,)
        del (self._cloud_status,)
        del (self._battery_src,)
        del (self._battery_text,)

    async def _btna_event_handler(self, fw):
        # print("_btna_event_handler")
        pass

    async def _btnb_event_handler(self, fw):
        # print("_btnb_event_handler")
        pass

    async def _btnc_event_handler(self, fw):
        # print("_btnc_event_handler")
        pass

    def _create_row(self, label_text, y):
        label = widgets.Label(
            label_text,
            12,
            self._origin_y + y,
            w=_TEXT_PANEL_W - 18,
            h=20,
            fg_color=_LABEL_COLOR,
            bg_color=_BG_COLOR,
            font=Widgets.FONTS.Montserrat14,
        )
        label.set_text(label_text)

        value = widgets.Label(
            "",
            12,
            self._origin_y + y + 22,
            w=_TEXT_PANEL_W - 18,
            h=26,
            fg_color=_VALUE_COLOR,
            bg_color=_BG_COLOR,
            font=Widgets.FONTS.Montserrat18,
        )
        value.set_long_mode(widgets.Label.LONG_DOT)
        return label, value

    @staticmethod
    def _set_value(label, text, fallback="-"):
        text = fallback if text is None or text == "" else str(text)
        label.set_text(text)

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).decode("utf-8").upper()

    @staticmethod
    def _get_access_code():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_nick_name():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""

    def _collect_state(self):
        return {
            "mac": self._get_mac(),
            "access_code": self._get_access_code(),
            "nick_name": self._get_nick_name(),
        }

    def _get_bar_src(self):
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if infos[0] == 0:
                return res.BAR2_IMG
            elif infos[0] in (1, 2):
                return res.BAR3_IMG
        else:
            return res.BAR2_IMG

    def _get_network_status(self):
        status = self._wifi.connect_status()
        if status is network.STAT_GOT_IP:
            rssi = self._wifi.get_rssi()
            if rssi <= -80:
                return NETWORK_STATUS_RSSI_WORSE
            elif rssi <= -60:
                return NETWORK_STATUS_RSSI_MID
            else:
                return NETWORK_STATUS_RSSI_GOOD
        else:
            return NETWORK_STATUS_DISCONNECTED

    def _get_cloud_status(self):
        if _HAS_SERVER is True:
            status = M5Things.status()
            return {
                -2: CLOUD_STATUS_DISCONNECTED,
                -1: CLOUD_STATUS_DISCONNECTED,
                0: CLOUD_STATUS_INIT,
                1: CLOUD_STATUS_INIT,
                2: CLOUD_STATUS_CONNECTED,
                3: CLOUD_STATUS_DISCONNECTED,
            }[status]
        else:
            return CLOUD_STATUS_DISCONNECTED

    @staticmethod
    def _get_battery_src(battery, charging):
        src = ""
        if battery > 0 and battery <= 100:
            if battery < 20:
                src = res.BATTERY_RED_CHARGE_IMG if charging else res.BATTERY_RED_IMG
            elif battery <= 100:
                src = res.BATTERY_GREEN_CHARGE_IMG if charging else res.BATTERY_GREEN_IMG
        else:
            src = res.BATTERY_BLACK_CHARGE_IMG if charging else res.BATTERY_BLACK_IMG
        return src

    @staticmethod
    def _get_battery_text(battery):
        if battery > 0 and battery <= 100:
            return "{:d}%".format(battery)
        else:
            return ""
