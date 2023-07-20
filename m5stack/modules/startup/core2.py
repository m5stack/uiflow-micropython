# -*- encoding: utf-8 -*-
# CoreS3 startup script
import M5
from M5 import *
import time
import network
from . import Startup
from collections import namedtuple
import os
import micropython
import machine

# from machine import I2C, Pin
import esp32
import sys
import binascii

# from unit import CardKB, KeyCode
import gc
from widgets.label import Label
from widgets.button import Button
from widgets.image import Image
from tiny_gui.app import AppManage, AppBase, KeyEvent

try:
    import urequests as requests
except ImportError:
    import requests

from common.font import MontserratMedium10

# from common.font import MontserratMedium14
from common.font import MontserratMedium16
from common.font import MontserratMedium18

micropython.alloc_emergency_exception_buf(100)

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = False


_permissions = {0: "Private", 1: "ToKen Required", 2: "Public"}


class KeyCode:
    KEYCODE_UNKNOWN = 0x00
    KEYCODE_BACKSPACE = 0x08
    KEYCODE_TAB = 0x09
    KEYCODE_ENTER = 0x0D
    KEYCODE_ESC = 0x1B
    KEYCODE_SPACE = 0x20
    KEYCODE_DEL = 0x7F

    KEYCODE_LEFT = 180
    KEYCODE_UP = 181
    KEYCODE_DOWN = 182
    KEYCODE_RIGHT = 183


class _ServerStatus:
    INIT = 0
    CONNECTED = 1
    DISCONNECTED = 2


_m5things_status = {
    -2: "SNTP_ERROR",
    -1: "CNCT_ERROR",
    0: "STANDBY",
    1: "CONNECTING",
    2: "CONNECTED",
    3: "DISCONNECT",
}


class _WiFiStatus:
    INIT = 0
    RSSI_GOOD = 1
    RSSI_MID = 2
    RSSI_WORSE = 3
    DISCONNECTED = 4


ImageDesc = namedtuple("ImageDesc", ["src", "x", "y", "w", "h"])


_setting_icos = {
    True: ImageDesc(src="/system/core2/Selection/setting_selected.png", x=5, y=20 + 4, w=62, h=56),
    False: ImageDesc(
        src="/system/core2/Selection/setting_unselected.png", x=5, y=20 + 4, w=62, h=56
    ),
}


_develop_icos = {
    True: ImageDesc(
        src="/system/core2/Selection/develop_selected.png", x=5 + 62, y=20 + 4, w=62, h=56
    ),
    False: ImageDesc(
        src="/system/core2/Selection/develop_unselected.png", x=5 + 62, y=20 + 4, w=62, h=56
    ),
}


_apprun_icos = {
    True: ImageDesc(
        src="/system/core2/Selection/appRun_selected.png", x=5 + 62 + 62, y=20 + 4, w=62, h=56
    ),
    False: ImageDesc(
        src="/system/core2/Selection/appRun_unselected.png", x=5 + 62 + 62, y=20 + 4, w=62, h=56
    ),
}

_applist_icos = {
    True: ImageDesc(
        src="/system/core2/Selection/appList_selected.png",
        x=5 + 62 + 62 + 62,
        y=20 + 4,
        w=62,
        h=56,
    ),
    False: ImageDesc(
        src="/system/core2/Selection/appList_unselected.png",
        x=5 + 62 + 62 + 62,
        y=20 + 4,
        w=62,
        h=56,
    ),
}


_ezdata_icos = {
    True: ImageDesc(
        src="/system/core2/Selection/ezdata_selected.png",
        x=5 + 62 + 62 + 62 + 62,
        y=20 + 4,
        w=62,
        h=56,
    ),
    False: ImageDesc(
        src="/system/core2/Selection/ezdata_unselected.png",
        x=5 + 62 + 62 + 62 + 62,
        y=20 + 4,
        w=62,
        h=56,
    ),
}


_binary_data = None
_wav_path = None


def _play_wav(wav: str):
    global _binary_data, _wav_path
    if _binary_data is None or _wav_path is not wav:
        with open(wav, "rb") as f:
            _binary_data = f.read()
        _wav_path = wav
        if wav is "/system/common/wav/click.wav":
            M5.Speaker.setVolume(64)
        else:
            M5.Speaker.setVolume(127)
    M5.Speaker.playWav(_binary_data)


Rect = namedtuple("Rect", ["x", "y", "w", "h"])


def _charge_ico(icos):
    try:
        len(icos)
    except TypeError:
        cache = []
        for i in icos:
            yield i
            cache.append(i)
        icos = cache
    while icos:
        yield from icos


_ssid_img_desc = ImageDesc(
    src="/system/core2/Setting/ssid.png", x=4, y=20 + 4 + 56 + 4, w=312, h=108
)

_pwd_img_desc = ImageDesc(
    src="/system/core2/Setting/pass.png", x=4, y=20 + 4 + 56 + 4, w=312, h=108
)

_wifiserver_img_desc = ImageDesc(
    src="/system/core2/Setting/wifiServer.png", x=4, y=20 + 4 + 56 + 4, w=312, h=108
)

_server_img_desc = ImageDesc(
    src="/system/core2/Setting/server.png", x=4, y=20 + 4 + 56 + 4, w=312, h=108
)


class WiFiSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self.x = 4
        self.y = 20 + 4 + 56 + 4
        self.w = 312
        self.h = 108
        self._ssid_label = Label(
            "ssid",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12,
            w=180,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)
        self._pwd_label = Label(
            "pwd",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12 + 35,
            w=180,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._pwd_label.setLongMode(Label.LONG_DOT)
        self._server_label = Label(
            "server",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12 + 35 + 34,
            w=190,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._server_label.setLongMode(Label.LONG_DOT)
        self._apps = [
            Rect(4, 20 + 4 + 56 + 4, 244, 108),  # option select
            Rect(4 + 249, 20 + 4 + 56 + 4, 63, 64),  # save & link
            Rect(4 + 249, 20 + 4 + 56 + 4 + 64, 63, 44),  # option select
        ]
        self._option_views = _charge_ico(
            (
                (0, self._select_ssid_option),
                (1, self._select_psd_option),
                (2, self._select_server_option),
            )
        )
        self._app_layout = (
            (self._apps[0],),
            (self._apps[1],),
        )
        self._cursor_row = 0
        self._cursor_col = 0
        self._option = -1
        self._wifi = data
        self.focus = False

    def mount(self):
        self.get_data()
        self._select_default_option()

    def _select_default_option(self):
        M5.Lcd.drawImage(_wifiserver_img_desc.src, _wifiserver_img_desc.x, _wifiserver_img_desc.y)
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def _select_ssid_option(self):
        M5.Lcd.drawImage(_ssid_img_desc.src, _ssid_img_desc.x, _ssid_img_desc.y)
        self._ssid_label.setTextColor(0x000000, 0xDCDDDD)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def _select_psd_option(self):
        M5.Lcd.drawImage(_pwd_img_desc.src, _pwd_img_desc.x, _pwd_img_desc.y)
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xDCDDDD)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def _select_server_option(self):
        M5.Lcd.drawImage(_server_img_desc.src, _server_img_desc.x, _server_img_desc.y)
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xDCDDDD)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        self.ssid = self.nvs.get_str("ssid0")
        self.pswd = self.nvs.get_str("pswd0")
        self.server = self.nvs.get_str("server")
        self.ssid_tmp = self.ssid
        self.pswd_tmp = self.pswd
        self.server_tmp = self.server

    def set_data(self):
        is_save = False
        if self.ssid != self.ssid_tmp:
            self.ssid = self.ssid_tmp
            self.nvs.set_str("ssid0", self.ssid)
            DEBUG and print("set new ssid: ", self.ssid)
            is_save = True
        if self.pswd != self.pswd_tmp:
            self.pswd = self.pswd_tmp
            self.nvs.set_str("pswd0", self.pswd)
            DEBUG and print("set new ssid: ", self.ssid)
            is_save = True
        if self.server != self.server_tmp:
            self.server = self.server_tmp
            self.nvs.set_str("server", self.server)
            DEBUG and print("set new server: ", self.server)
            is_save = True

        if is_save is True:
            self.nvs.commit()
            self._wifi.wlan.disconnect()
            self._wifi.wlan.active(False)
            self._wifi.wlan.active(True)
            self._wifi.connect_network(self.ssid, self.pswd)

    def handle(self, x, y):
        if self.is_select_option(self._apps[0], x, y):
            self._option, view_fn = next(self._option_views)
            view_fn()
        elif self.is_select_option(self._apps[1], x, y):
            self._select_default_option()
            self.set_data()
        if self.is_select_option(self._apps[2], x, y):
            self._option, view_fn = next(self._option_views)
            view_fn()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            event.status = True
            self.focus = True
            self._option, view_fn = next(self._option_views)
            view_fn()

        if self.focus is False:
            return

        if event.key == KeyCode.KEYCODE_ESC:
            self.ssid_tmp = self.ssid
            self.pswd_tmp = self.pswd
            self.server_tmp = self.server
            self._select_default_option()
            self.focus = False
            event.status = True

        if event.key == KeyCode.KEYCODE_BACKSPACE and self._option in (0, 1, 2):
            if self._option == 0:
                self.ssid_tmp = self.ssid_tmp[:-1]
                self._ssid_label.setText(self.ssid_tmp)
            elif self._option == 1:
                if self.pswd_tmp == self.pswd:
                    self.pswd_tmp = ""
                else:
                    self.pswd_tmp = self.pswd_tmp[:-1]
                self._pwd_label.setText(self.pswd_tmp)
            elif self._option == 2:
                self.server_tmp = self.server_tmp[:-1]
                self._server_label.setText(self.server_tmp)
            event.status = True

        if event.key in (
            KeyCode.KEYCODE_DOWN,
            KeyCode.KEYCODE_RIGHT,
            KeyCode.KEYCODE_LEFT,
            KeyCode.KEYCODE_UP,
        ):
            if event.key == KeyCode.KEYCODE_DOWN:
                self._cursor_row += 1
                self._cursor_col = 0
            if event.key == KeyCode.KEYCODE_RIGHT:
                self._cursor_col += 1
            if event.key == KeyCode.KEYCODE_LEFT:
                self._cursor_col -= 1
            if event.key == KeyCode.KEYCODE_UP:
                self._cursor_row -= 1
                self._cursor_col = 0
            if event.key == KeyCode.KEYCODE_ESC:
                self._cursor_row = 0
                self._cursor_col = 0

            if self._cursor_row >= len(self._app_layout):
                self._cursor_row = len(self._app_layout) - 1
            if self._cursor_row < 0:
                self._cursor_row = 0

            if self._cursor_col >= 0:
                self._cursor_col = self._cursor_col % len(self._app_layout[self._cursor_row])
            if self._cursor_col < 0:
                self._cursor_col = len(self._app_layout[self._cursor_row]) - 1

            if self._cursor_col == 1:
                self._select_default_option()
                self.set_data()
            event.status = True
        elif event.key >= 0x20 and event.key <= 126:
            if self._option == 0:
                self.ssid_tmp += chr(event.key)
                self._ssid_label.setText(self.ssid_tmp)
            elif self._option == 1:
                if self.pswd_tmp == self.pswd:
                    self.pswd_tmp = ""
                else:
                    self.pswd_tmp += chr(event.key)
                self._pwd_label.setText(self.pswd_tmp)
            elif self._option == 2:
                self.server_tmp += chr(event.key)
                self._server_label.setText(self.server_tmp)
            event.status = True

    def umount(self) -> None:
        self._select_default_option()

    @staticmethod
    def is_select_option(rect: Rect, x, y):
        if x < rect.x:
            return False
        if x > (rect.x + rect.w):
            return False
        if y < rect.y:
            return False
        if y > (rect.y + rect.h):
            return False
        return True


_current_options = (
    (
        100,
        ImageDesc(
            src="/system/core2/Setting/charge100.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        500,
        ImageDesc(
            src="/system/core2/Setting/charge500.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        900,
        ImageDesc(
            src="/system/core2/Setting/charge900.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        1000,
        ImageDesc(
            src="/system/core2/Setting/charge1000.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    # (1500, ImageDesc(src="/system/core2/Setting/charge1500.png", x=4, y=20 + 4 + 56 + 4 + 108 + 4, w=60, h=44)),
    # (2000, ImageDesc(src="/system/core2/Setting/charge2000.png", x=4, y=20 + 4 + 56 + 4 + 108 + 4, w=60, h=44)),
)


class BatteryChargeSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = _charge_ico(_current_options)
        self._current, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            current, self.descriptor = next(self.icos)
            if current == self._current:
                break
        M5.Lcd.drawImage(self.descriptor.src, self.descriptor.x, self.descriptor.y)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._current, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._current, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        try:
            self._current = self.nvs.get_i32("charge_current")
        except OSError:
            self._current = 500

    def set_data(self):
        M5.Power.setBatteryCharge(True)
        M5.Power.setChargeCurrent(self._current)
        self.nvs.set_i32("charge_current", self._current)
        self.nvs.commit()

    def umount(self) -> None:
        pass


_boot_options = (
    (
        0,
        ImageDesc(
            src="/system/core2/Setting/bootNo.png",
            x=4 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        1,
        ImageDesc(
            src="/system/core2/Setting/bootYes.png",
            x=4 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class BootScreenSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = _charge_ico(_boot_options)
        self.boot_option, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            boot_option, self.descriptor = next(self.icos)
            if boot_option == self.boot_option:
                break
        self._load_view()

    def _load_view(self):
        M5.Lcd.drawImage(self.descriptor.src, self.descriptor.x, self.descriptor.y)

    def handle(self, x, y):
        if self.is_select(x, y):
            self.boot_option, self.descriptor = next(self.icos)
            self._load_view()
            self.set_data()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self.boot_option, self.descriptor = next(self.icos)
            self._load_view()
            self.set_data()

    def get_data(self):
        nvs = esp32.NVS("uiflow")
        self.boot_option = nvs.get_u8("boot_option")

    def set_data(self):
        nvs = esp32.NVS("uiflow")
        boot_option = nvs.set_u8("boot_option", self.boot_option)
        nvs.commit()
        return boot_option

    def umount(self) -> None:
        pass


_comlink_options = (
    (
        False,
        ImageDesc(
            src="/system/core2/Setting/comxDisable.png",
            x=4 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        True,
        ImageDesc(
            src="/system/core2/Setting/comxEnable.png",
            x=4 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class ComLinkSetting(AppBase):
    # TODO

    def __init__(self, icos: dict) -> None:
        self.icos = _charge_ico(_comlink_options)
        self._data, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        M5.Lcd.drawImage(self.descriptor.src, self.descriptor.x, self.descriptor.y)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.descriptor = next(self.icos)
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.descriptor = next(self.icos)
            self.mount()

    def umount(self) -> None:
        pass


_brightness_options = (
    (
        64,
        ImageDesc(
            src="/system/core2/Setting/screen25.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        127,
        ImageDesc(
            src="/system/core2/Setting/screen50.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        192,
        ImageDesc(
            src="/system/core2/Setting/screen75.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        255,
        ImageDesc(
            src="/system/core2/Setting/screen100.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class BrightnessSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = _charge_ico(_brightness_options)
        self._data, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            data, self.descriptor = next(self.icos)
            if data == self._data:
                break
        M5.Lcd.drawImage(self.descriptor.src, self.descriptor.x, self.descriptor.y)

    def get_data(self):
        self._data = M5.Lcd.getBrightness()

    def set_data(self):
        M5.Lcd.setBrightness(self._data)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def umount(self) -> None:
        pass


_buspower_options = (
    (
        False,
        ImageDesc(
            src="/system/core2/Setting/busInput.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        True,
        ImageDesc(
            src="/system/core2/Setting/busOutput.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class BUSPowerSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = _charge_ico(_buspower_options)
        self._data, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            data, self.descriptor = next(self.icos)
            if data == self._data:
                break
        M5.Lcd.drawImage(self.descriptor.src, self.descriptor.x, self.descriptor.y)

    def get_data(self):
        self._data = M5.Power.getExtOutput()

    def set_data(self):
        M5.Power.setExtOutput(self._data)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def umount(self) -> None:
        pass


class SettingsApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self.icos = icos
        self.descriptor = self.icos.get(False)
        self._apps = [
            WiFiSetting(None, data=data),
            BatteryChargeSetting(None),
            BootScreenSetting(None),
            ComLinkSetting(None),
            BrightnessSetting(None),
            BUSPowerSetting(None),
        ]

        self._app_layout = (
            (self._apps[0],),
            (
                self._apps[1],
                self._apps[2],
                self._apps[3],
                self._apps[4],
                self._apps[5],
            ),
        )
        self._cursor_row = 0
        self._cursor_col = 0
        self._focus = True

    def mount(self):
        desc = self.icos.get(True)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        for app in self._apps:
            app.mount()

    def handle(self, x, y):
        app = None
        for app in self._apps:
            if app.is_select(x, y):
                break

        if app is not None:
            app.handle(x, y)

    def handle_input(self, event: KeyEvent):
        self._app_layout[self._cursor_row][self._cursor_col].handle_input(event)

        if event.status is True:
            return

        if event.key == KeyCode.KEYCODE_DOWN:
            self._cursor_row += 1
            self._cursor_col = 0
            event.status = True
        if event.key == KeyCode.KEYCODE_RIGHT:
            self._cursor_col += 1
            event.status = True
        if event.key == KeyCode.KEYCODE_LEFT:
            self._cursor_col -= 1
            event.status = True
        if event.key == KeyCode.KEYCODE_UP:
            self._cursor_row -= 1
            self._cursor_col = 0
            event.status = True
        if event.key == KeyCode.KEYCODE_ESC:
            self._cursor_row = 0
            self._cursor_col = 0

        if self._cursor_row >= len(self._app_layout):
            self._cursor_row = len(self._app_layout) - 1
        if self._cursor_row < 0:
            self._cursor_row = 0

        if self._cursor_col >= 0:
            self._cursor_col = self._cursor_col % len(self._app_layout[self._cursor_row])
        if self._cursor_col < 0:
            self._cursor_col = len(self._app_layout[self._cursor_row]) - 1

    def umount(self) -> None:
        for app in self._apps:
            app.umount()
        desc = self.icos.get(False)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)


_dev_private_desc = ImageDesc(
    src="/system/core2/Develop/private.png", x=4, y=20 + 4 + 56 + 4, w=312, h=156
)
_dev_pulic_desc = ImageDesc(
    src="/system/core2/Develop/public.png", x=4, y=20 + 4 + 56 + 4, w=312, h=156
)


class DevApp(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = icos
        self.descriptor = self.icos.get(False)
        self._mac_label = Label(
            "aabbcc112233",
            4 + 6,
            (20 + 4 + 56 + 4) + 57,
            w=177,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )

        self._account_label = Label(
            "XXABC",
            4 + 6,
            (20 + 4 + 56 + 4) + 57 + 40,
            w=110,
            h=60,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )
        self._account_label.setLongMode(Label.LONG_WARP)

        self.avatar = "/system/common/img/avatar.jpg"

        super().__init__(icos)

    def mount(self):
        data = self.load_data()
        desc = self.icos.get(True)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        M5.Lcd.drawImage(self.src.src, self.src.x, self.src.y)
        self._mac_label.setText(data[0])
        self._account_label.setText(str(data[1]))

        if self.avatar == "/system/common/img/avatar.jpg":
            M5.Lcd.drawJpg(self.avatar, 130, 180, 60, 60)
        else:
            M5.Lcd.drawJpg(self.avatar, 130, 180, 56, 56, 0, 0, 0.28, 0.28)

    def load_data(self):
        mac = binascii.hexlify(machine.unique_id()).upper()
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if infos[0] is 0 or infos[0] is 1:
                self.src = _dev_private_desc
            elif infos[0] is 2:
                self.src = _dev_pulic_desc
            DEBUG and print("Develop info:")
            DEBUG and print("  Device mac:", mac)
            DEBUG and print("  Permissions:", _permissions.get(infos[0]))
            DEBUG and print("  Account:", infos[1])
            DEBUG and print("  Avatar:", infos[4])
            if len(infos[4]) is 0:
                self.avatar = "/system/common/img/avatar.jpg"
            else:
                # FIXME: avatar.jpg path is not right
                self.avatar = "/system/common/" + str(infos[4]).split("/")[-1]

            try:
                os.stat(self.avatar)
            except OSError:
                rsp = requests.get("https://community.m5stack.com" + str(infos[4]))
                f = open(self.avatar, "wb")
                f.write(rsp.content)
                f.close()
                rsp.close()
            return (mac, None if len(infos[1]) is 0 else infos[1])
        else:
            self.src = _dev_private_desc
            return (mac, None, None)

    def handle(self, x, y):
        pass

    def umount(self) -> None:
        desc = self.icos.get(False)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)


class RunApp(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = icos
        self.descriptor = self.icos.get(False)
        self._name_label = Label(
            "name",
            4 + 10,
            (20 + 4 + 56 + 4) + 4,
            w=312,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )

        self._mtime_label = Label(
            "Time: 2023/5/14 12:23:43",
            4 + 10 + 8,
            (20 + 4 + 56 + 4) + 4 + 20 + 6,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium16.FONT,
        )

        self._account_label = Label(
            "Account: XXABC",
            4 + 10 + 8,
            (20 + 4 + 56 + 4) + 4 + 20 + 6 + 18,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium16.FONT,
        )

        self._ver_label = Label(
            "Ver: UIFLOW2.0 a18",
            4 + 10 + 8,
            (20 + 4 + 56 + 4) + 4 + 20 + 6 + 18 + 18,
            w=312,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium16.FONT,
        )

        self._main_canvas = M5.Lcd.newCanvas(312, 156, 16, True)
        self._main_canvas.drawImage("/system/core2/Run/run.png", 0, 0)

        self._apps = [
            Rect(4, 20 + 4 + 56 + 4 + 84, 156, 72),
            Rect(4 + 156, 20 + 4 + 56 + 4 + 84, 156, 72),
        ]
        self._path = None

    def mount(self):
        desc = self.icos.get(True)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        # M5.Lcd.drawImage("/system/core2/Run/run.png", 4, 20 + 4 + 56 + 4)
        self._main_canvas.push(4, 20 + 4 + 56 + 4)
        self.update_file_info("main.py")

    def update_file_info(self, filename):
        try:
            self._path = filename
            infos = self._get_file_info(self._path)
            self._name_label.setText(filename)
            self._mtime_label.setText(
                "Time: {:04d}/{:d}/{:d} {:02d}:{:02d}:{:02d}".format(
                    infos[0][0], infos[0][1], infos[0][2], infos[0][3], infos[0][4], infos[0][5]
                )
            )
            self._account_label.setText("Account: {:s}".format(str(infos[1])))
            self._ver_label.setText("Ver: {:s}".format(str(infos[2])))
        except OSError:
            self._name_label.setText("None")
            self._mtime_label.setText("Time: None")
            self._account_label.setText("Account: None")
            self._ver_label.setText("Ver: None")

    def handle(self, x, y):
        if self.is_select(self._apps[0], x, y):
            self._handle_run_once()
        elif self.is_select(self._apps[1], x, y):
            self._handle_run_always()

    def _handle_run_once(self):
        execfile(self._path)
        sys.exit(0)

    def _handle_run_always(self):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 0)
        nvs.commit()
        machine.reset()

    @staticmethod
    def is_select(rect: Rect, x, y):
        if x < rect.x:
            return False
        if x > (rect.x + rect.w):
            return False
        if y < rect.y:
            return False
        if y > (rect.y + rect.h):
            return False
        return True

    @staticmethod
    def _get_file_info(path):
        stat = os.stat(path)
        account = None
        ver = None

        with open(path, "r") as f:
            for line in f:
                if line.find("Account") != -1:
                    account = line.split(":")[1].strip()
                if line.find("Ver") != -1:
                    ver = line.split(":")[1].strip()
                if account != None and ver != None:
                    break

        return (time.localtime(stat[8]), account, ver)

    def umount(self) -> None:
        desc = self.icos.get(False)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)


_list_main_desc = ImageDesc(
    src="/system/core2/List/main.png", x=4, y=20 + 4 + 56 + 4, w=312, h=156
)


class ListApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self.icos = icos
        self.data = None
        self.descriptor = self.icos.get(False)

        self._btn_up = None
        self._btn_down = None
        self._btn_once = None
        self._btn_always = None
        self._buttons = []

        self._left_img = None
        self._right_img = None

        self._labels = []
        self._label0 = None
        self._label1 = None
        self._label2 = None
        self._label3 = None

    def create(self):
        pass

    def mount(self):
        self.load_data()
        desc = self.icos.get(True)
        M5.Lcd.drawImage(desc.src, desc.x, desc.y)
        M5.Lcd.drawImage(_list_main_desc.src, _list_main_desc.x, _list_main_desc.y)

        # button up
        # x 4 + 2
        # y (20 + 4 + 56 + 4) + 2
        # w 30
        # h 75
        if self._btn_up is None:
            self._btn_up = Button(None)
            self._btn_up.set_pos(4 + 2, (20 + 4 + 56 + 4) + 2)
            self._btn_up.set_size(60, 75)
            self._btn_up.add_event(self._btn_up_event_handler)

        # button down
        # x 4 + 2
        # y (20 + 4 + 56 + 4) + 2 + 75 + 2
        # w 30
        # h 75
        if self._btn_down is None:
            self._btn_down = Button(None)
            self._btn_down.set_pos(4 + 2, (20 + 4 + 56 + 4) + 2 + 75 + 2)
            self._btn_down.set_size(60, 75)
            self._btn_down.add_event(self._btn_down_event_handler)

        # run once
        # x 4 + (312 - 60)
        # y (20 + 4 + 56 + 4) + 30
        # w 60
        # h 63
        if self._btn_once is None:
            self._btn_once = Button(None)
            self._btn_once.set_pos(4 + (312 - 100), (20 + 4 + 56 + 4) + 30)
            self._btn_once.set_size(100, 63)
            self._btn_once.add_event(self._btn_once_event_handler)

        # run always
        # x 4 + (312 - 60)
        # y (20 + 4 + 56 + 4) + 30 + 63
        # w 60
        # h 63
        if self._btn_always is None:
            self._btn_always = Button(None)
            self._btn_always.set_pos(4 + (312 - 100), (20 + 4 + 56 + 4) + 30 + 63)
            self._btn_always.set_size(100, 63)
            self._btn_always.add_event(self._btn_always_event_handler)

        if len(self._buttons) is not 0:
            self._buttons.clear()
            self._buttons.append(self._btn_up)
            self._buttons.append(self._btn_down)
            self._buttons.append(self._btn_once)
            self._buttons.append(self._btn_always)

        self._line_spacing = 36 + 2 + 2
        self._left_cursor_x = 4 + 2 + 30
        self._left_cursor_y = (20 + 4 + 56 + 4) + 2
        if self._left_img is None:
            self._left_img = Image()
        self._left_img.set_pos(self._left_cursor_x, self._left_cursor_y)
        self._left_img.set_size(10, 36)
        self._left_img.set_src("/system/core2/List/left_cursor.png")

        self._right_cursor_x = 320 - 4 - 60 - 10
        self._right_cursor_y = (20 + 4 + 56 + 4) + 2
        if self._right_img is None:
            self._right_img = Image()
        self._right_img.set_pos(self._right_cursor_x, self._right_cursor_y)
        self._right_img.set_size(10, 36)
        self._right_img.set_src("/system/core2/List/right_cursor.png")

        if self._label0 is None:
            self._label0 = Label(
                "",
                self._left_cursor_x + 10,
                self._left_cursor_y + 8,
                w=200,
                h=36,
                fg_color=0x000000,
                bg_color=0xFEFEFE,
                font=MontserratMedium18.FONT,
            )
        if self._label1 is None:
            self._label1 = Label(
                "",
                self._left_cursor_x + 10,
                self._left_cursor_y + 8 + self._line_spacing,
                w=200,
                h=36,
                fg_color=0x000000,
                bg_color=0xFEFEFE,
                font=MontserratMedium18.FONT,
            )
        if self._label2 is None:
            self._label2 = Label(
                "",
                self._left_cursor_x + 10,
                self._left_cursor_y + 8 + self._line_spacing + self._line_spacing,
                w=200,
                h=36,
                fg_color=0x000000,
                bg_color=0xFEFEFE,
                font=MontserratMedium18.FONT,
            )
        if self._label3 is None:
            self._label3 = Label(
                "",
                self._left_cursor_x + 10,
                self._left_cursor_y
                + 8
                + self._line_spacing
                + self._line_spacing
                + self._line_spacing,
                w=200,
                h=36,
                fg_color=0x000000,
                bg_color=0xFEFEFE,
                font=MontserratMedium18.FONT,
            )

        if len(self._labels) is not 4:
            self._labels.clear()
            self._labels.append(self._label0)
            self._labels.append(self._label1)
            self._labels.append(self._label2)
            self._labels.append(self._label3)

        for label, file in zip(self._labels, self._files):
            if file is None or label is None:
                break
            label.setText(file)

    def load_data(self):
        self._files = []
        for file in os.listdir("apps"):
            if file.endswith(".py"):
                self._files.append(file)
        self._files_number = len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def handle(self, x, y):
        for btn in self._buttons:
            if btn.handle(x, y):
                break

    def handle_input(self, event: KeyEvent):
        return super().handle_input(event)

    def umount(self) -> None:
        super().umount()
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)

    def _btn_up_event_handler(self, event):
        if self._file_pos is 0 and self._cursor_pos == 0:
            _play_wav("/system/common/wav/bg.wav")
            return

        self._file_pos -= 1
        if self._cursor_pos < 0:
            self._cursor_pos = 0

        self._cursor_pos -= 1
        if self._file_pos < 0:
            self._file_pos = 0

        DEBUG and print("cursor:", self._cursor_pos)
        DEBUG and print("file:", self._file_pos)

        M5.Lcd.drawImage(_list_main_desc.src, _list_main_desc.x, _list_main_desc.y)
        if self._file_pos < self._cursor_pos:
            for label, file in zip(self._labels, self._files):
                if file is None or label is None:
                    break
                label.setText(file)
        else:
            for label, file in zip(
                self._labels,
                self._files[
                    self._file_pos - self._cursor_pos : self._file_pos + (4 - self._cursor_pos)
                ],
            ):
                if file is None or label is None:
                    break
                label.setText(file)

        self._left_img.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._line_spacing * self._cursor_pos
        )
        self._right_img.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._line_spacing * self._cursor_pos
        )

    def _btn_down_event_handler(self, event):
        # FIXME
        self._file_pos += 1
        self._cursor_pos += 1

        max_cursor_pos = len(self._files) - 1 if len(self._files) < 4 else 3
        if self._cursor_pos > max_cursor_pos:
            self._cursor_pos = max_cursor_pos
        if self._file_pos >= len(self._files):
            self._file_pos = len(self._files) - 1
            _play_wav("/system/common/wav/bg.wav")
            return

        DEBUG and print("cursor:", self._cursor_pos)
        DEBUG and print("file:", self._file_pos)

        M5.Lcd.drawImage(_list_main_desc.src, _list_main_desc.x, _list_main_desc.y)
        if self._file_pos < 4:
            for label, file in zip(self._labels, self._files):
                if file is None or label is None:
                    break
                label.setText(file)
        else:
            for label, file in zip(
                self._labels, self._files[self._file_pos - 3 : self._file_pos + 1]
            ):
                if file is None or label is None:
                    break
                label.setText(file)

        # cursor img
        self._left_img.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing
        )
        self._right_img.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing
        )

    def _btn_once_event_handler(self, event):
        DEBUG and print("run once")
        execfile("apps/" + self._files[self._file_pos])
        sys.exit(0)

    def _btn_always_event_handler(self, event):
        DEBUG and print("run always")
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 0)
        nvs.commit()
        with open("apps/" + self._files[self._file_pos], "rb") as f_src, open(
            "main.py", "wb"
        ) as f_dst:
            while True:
                chunk = f_src.read(1024)
                if not chunk:
                    break
                f_dst.write(chunk)
        time.sleep(0.1)
        machine.reset()


_WIFI_STATUS_ICO = {
    _WiFiStatus.INIT: ImageDesc(
        src="/system/core2/WiFi/wifi_empty.png", x=320 - 56 - 20 - 5 - 20 - 5, y=0, w=20, h=20
    ),
    _WiFiStatus.RSSI_GOOD: ImageDesc(
        src="/system/core2/WiFi/wifi_good.png", x=320 - 56 - 20 - 5 - 20 - 5, y=0, w=20, h=20
    ),
    _WiFiStatus.RSSI_MID: ImageDesc(
        src="/system/core2/WiFi/wifi_mid.png", x=320 - 56 - 20 - 5 - 20 - 5, y=0, w=20, h=20
    ),
    _WiFiStatus.RSSI_WORSE: ImageDesc(
        src="/system/core2/WiFi/wifi_worse.png", x=320 - 56 - 20 - 5 - 20 - 5, y=0, w=20, h=20
    ),
    _WiFiStatus.DISCONNECTED: ImageDesc(
        src="/system/core2/WiFi/wifi_disconnected.png",
        x=320 - 56 - 20 - 5 - 20 - 5,
        y=0,
        w=20,
        h=20,
    ),
}


_SERVER_STATUS_ICO = {
    _ServerStatus.INIT: ImageDesc(
        src="/system/core2/Server/server_empty.png", x=320 - 56 - 20 - 5, y=0, w=20, h=20
    ),
    _ServerStatus.CONNECTED: ImageDesc(
        src="/system/core2/Server/Server_Green.png", x=320 - 56 - 20 - 5, y=0, w=20, h=20
    ),
    _ServerStatus.DISCONNECTED: ImageDesc(
        src="/system/core2/Server/server_error.png", x=320 - 56 - 20 - 5, y=0, w=20, h=20
    ),
}


class StatusBarApp:
    def __init__(self, icos: dict, wifi) -> None:
        self.id = 0
        self.x = 0
        self.y = 0
        self.w = 320
        self.h = 20

        self._wifi = wifi
        self._time_label = Label(
            "12:23",
            160,
            2,
            w=312,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xEEEEEF,
            font=MontserratMedium16.FONT,
        )
        self._battery_label = Label(
            "78%",
            320 - 56 + 22,
            4,
            w=312,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xFEFEFE,
            font=MontserratMedium10.FONT,
        )
        self._wifi_status = _WiFiStatus.INIT
        if _HAS_SERVER is False:
            self._server_status = _ServerStatus.DISCONNECTED

    def registered(self):
        pass

    def mount(self):
        self._load_view()

    def _load_view(self):
        M5.Lcd.drawImage("/system/core2/Title/title_blue.png", 0, 0)
        self.handle(None, None)

    def _update_time(self, struct_time):
        self._time_label.setText("{:02d}:{:02d}".format(struct_time[3], struct_time[4]))

    def _update_wifi(self, status):
        self._wifi_status = status
        src = _WIFI_STATUS_ICO.get(self._wifi_status)
        M5.Lcd.drawImage(src.src, src.x, src.y)

    def _update_server(self, status):
        self._server_status = status
        src = _SERVER_STATUS_ICO.get(self._server_status)
        M5.Lcd.drawImage(src.src, src.x, src.y)

    def _update_battery(self, battery, charging):
        src = ""
        if battery > 0 and battery <= 100:
            if battery < 20:
                src = (
                    "/system/core2/Battery/battery_Red_Charge.png"
                    if charging
                    else "/system/core2/Battery/battery_Red.png"
                )
            elif battery <= 100:
                src = (
                    "/system/core2/Battery/battery_Green_Charge.png"
                    if charging
                    else "/system/core2/Battery/battery_Green.png"
                )
            M5.Lcd.drawImage(src, 320 - 56, 0)
            self._battery_label.setText("{:d}%".format(battery))
        else:
            src = (
                "/system/core2/Battery/battery_Black_Charge.png"
                if charging
                else "/system/core2/Battery/battery_Black.png"
            )
            M5.Lcd.drawImage(src, 320 - 56, 0)

    @staticmethod
    def get_local_time():
        return time.localtime()

    def get_wifi_status(self):
        status = self._wifi.connect_status()
        if status is network.STAT_GOT_IP:
            rssi = self._wifi.get_rssi()
            if rssi <= -80:
                return _WiFiStatus.RSSI_WORSE
            elif rssi <= -60:
                return _WiFiStatus.RSSI_MID
            else:
                return _WiFiStatus.RSSI_GOOD
        else:
            return _WiFiStatus.DISCONNECTED

    @staticmethod
    def get_server_status():
        if _HAS_SERVER is True:
            status = M5Things.status()
            DEBUG and print(
                "Server connect status: %d(%s)" % (status, _m5things_status.get(status))
            )
            if status in (0, 1):
                return _ServerStatus.INIT
            elif status == 2:
                return _ServerStatus.CONNECTED
            elif status in (-2, -1, 3):
                return _ServerStatus.DISCONNECTED
        else:
            return _ServerStatus.DISCONNECTED

    def handle(self, x, y):
        self._update_time(self.get_local_time())
        self._update_wifi(self.get_wifi_status())
        self._update_server(self.get_server_status())
        self._update_battery(M5.Power.getBatteryLevel(), M5.Power.isCharging())

    def umount(self):
        pass

    def _disappear_view(self):
        pass


class BootView:
    def __init__(self) -> None:
        pass

    @classmethod
    def load(self) -> None:
        M5.Lcd.drawImage("/system/core2/boot.png", 0, 0)
        time.sleep(0.2)


class Core2_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()
        self._status_bar = StatusBarApp(None, self._wifi)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        gc.enable()
        self._wifi.connect_network(ssid, pswd)
        BootView.load()
        M5.Lcd.clear(0x000000)
        self._apps = AppManage(5)
        self._apps.register_app(SettingsApp(_setting_icos, data=self._wifi))
        self._apps.register_app(DevApp(_develop_icos))
        self._apps.register_app(RunApp(_apprun_icos))
        self._apps.register_app(ListApp(_applist_icos))
        self._apps.register_app(AppBase(_ezdata_icos))
        self._status_bar.mount()
        self._apps.mount()
        self._apps.select_app(1)

        DEBUG and print("Run startup menu")
        last_touch_time = time.ticks_ms()
        last_update_status_time = last_touch_time

        # self.i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
        # self._kb = CardKB(self.i2c0)
        # self._event = KeyEvent()
        # self._kb_status = False

        # try:
        while True:
            M5.update()
            if M5.Touch.getCount() > 0:
                detail = M5.Touch.getDetail(0)
                cur_time = time.ticks_ms()
                if cur_time - last_touch_time > 150:
                    if detail[9]:  # isHolding
                        pass
                    # elif detail[5] and detail[4]:  # wasPressed and isPressed
                    #     pass
                    # elif detail[8] and detail[4]:  # wasReleased and isPressed
                    #     pass
                    else:
                        _play_wav("/system/common/wav/click.wav")
                        self._apps.load_app(M5.Touch.getX(), M5.Touch.getY())
                    last_touch_time = time.ticks_ms()

            # try:
            #     if self._kb.is_pressed():
            #         _play_wav("/system/common/wav/click.wav")
            #         self._event.key = self._kb.get_key()
            #         self._event.status = False
            #         self._apps.handle_input(self._event)
            #     if self._kb_status is False:
            #         _play_wav("/system/common/wav/insert.wav")
            #         self._kb_status = True
            # except OSError:
            #     if self._kb_status is True:
            #         _play_wav("/system/common/wav/remove.wav")
            #         self._kb_status = False

            # if self._kb.is_pressed():
            #     _play_wav("/system/common/wav/click.wav")
            #     self._event.key = self._kb.get_key()
            #     self._event.status = False
            #     self._apps.handle_input(self._event)

            if time.ticks_ms() - last_update_status_time > 5000:
                # 会影响触摸发处理速度
                self._status_bar.handle(None, None)
                last_update_status_time = time.ticks_ms()
                gc.collect()
                # print("alloc:", gc.mem_alloc())
                # print("free:", gc.mem_free())
        # except KeyboardInterrupt:
        #     gc.collect()
