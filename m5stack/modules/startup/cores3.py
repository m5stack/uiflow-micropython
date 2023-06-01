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
from machine import I2C, Pin
import esp32
import sys
import binascii
from unit import CardKB
import gc

from res.font import MontserratMedium10
from res.font import MontserratMedium14
from res.font import MontserratMedium16
from res.font import MontserratMedium18

micropython.alloc_emergency_exception_buf(100)

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = False


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


Permissions = {0: "Private", 1: "ToKen Required", 2: "Public"}


class KeyEvent:
    key = 0
    status = False


class ServerStatus:
    INIT = 0
    CONNECTED = 1
    DISCONNECTED = 2


M5THINGS_STATUS = {
    -2: "SNTP_ERROR",
    -1: "CNCT_ERROR",
    0: "STANDBY",
    1: "CONNECTING",
    2: "CONNECTED",
    3: "DISCONNECT",
}


class WiFiStatus:
    INIT = 0
    RSSI_GOOD = 1
    RSSI_MID = 2
    RSSI_WORSE = 3
    DISCONNECTED = 4


ImageDescriptor = namedtuple("ImageDescriptor", ["x", "y", "width", "height"])

_IMAGE_LIST = {
    "res/sys/cores3/Battery/battery_Gray.png": ImageDescriptor(320 - 44, 0, 44, 20),
    "res/sys/cores3/Battery/battery_Green.png": ImageDescriptor(320 - 44, 0, 44, 20),
    "res/sys/cores3/Battery/battery_Red.png": ImageDescriptor(320 - 44, 0, 44, 20),
    "res/sys/cores3/Battery/battery_Yellow.png": ImageDescriptor(320 - 44, 0, 44, 20),
    "res/sys/cores3/Selection/appList_selected.png": ImageDescriptor(5 + 62 + 62 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/appList_unselected.png": ImageDescriptor(5 + 62 + 62 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/appRun_selected.png": ImageDescriptor(5 + 62 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/appRun_unselected.png": ImageDescriptor(5 + 62 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/develop_selected.png": ImageDescriptor(5 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/develop_unselected.png": ImageDescriptor(5 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/ezdata_selected.png": ImageDescriptor(5 + 62 + 62 + 62 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/ezdata_unselected.png": ImageDescriptor(5 + 62 + 62 + 62 + 62, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/setting_selected.png": ImageDescriptor(5, 20 + 4, 62, 56),
    "res/sys/cores3/Selection/setting_unselected.png": ImageDescriptor(5, 20 + 4, 62, 56),
    "res/sys/cores3/Server/server_blue.png": ImageDescriptor(320 - 44 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/Server/server_empty.png": ImageDescriptor(320 - 44 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/Server/server_error.png": ImageDescriptor(320 - 44 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/Server/Server_Green.png": ImageDescriptor(320 - 44 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/Server/server_red.png": ImageDescriptor(320 - 44 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/Title/title_blue.png": ImageDescriptor(0, 0, 320, 20),
    "res/sys/cores3/Title/title_gray.png": ImageDescriptor(0, 0, 320, 20),
    "res/sys/cores3/Title/title_green.png": ImageDescriptor(0, 0, 320, 20),
    "res/sys/cores3/Title/title_red.png": ImageDescriptor(0, 0, 320, 20),
    "res/sys/cores3/WiFi/wifi_disconnected.png": ImageDescriptor(320 - 44 - 20 - 5 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/WiFi/wifi_empty.png": ImageDescriptor(320 - 44 - 20 - 5 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/WiFi/wifi_good.png": ImageDescriptor(320 - 44 - 20 - 5 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/WiFi/wifi_mid.png": ImageDescriptor(320 - 44 - 20 - 5 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/WiFi/wifi_worse.png": ImageDescriptor(320 - 44 - 20 - 5 - 20 - 5, 0, 20, 20),
    "res/sys/cores3/boot.png": ImageDescriptor(0, 0, 320, 240),
    "res/sys/cores3/boot/boot0.png": ImageDescriptor(60, 45, 320, 240),
    "res/sys/cores3/boot/boot1.png": ImageDescriptor(60, 45, 320, 240),
    "res/sys/cores3/boot/boot2.png": ImageDescriptor(60, 45, 320, 240),
    "res/sys/cores3/boot/boot3.png": ImageDescriptor(60, 45, 320, 240),
    "res/sys/cores3/Setting/wifiServer.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/pass.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/server.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/ssid.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/charge100.png": ImageDescriptor(4, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/charge500.png": ImageDescriptor(4, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/charge900.png": ImageDescriptor(4, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/charge1000.png": ImageDescriptor(4, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/charge1500.png": ImageDescriptor(4, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/charge2000.png": ImageDescriptor(4, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/bootNo.png": ImageDescriptor(4 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/bootYes.png": ImageDescriptor(4 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44),
    "res/sys/cores3/Setting/comxDisable.png": ImageDescriptor(
        4 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44
    ),
    "res/sys/cores3/Setting/comxEnable.png": ImageDescriptor(
        4 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44
    ),
    "res/sys/cores3/Setting/usbInput.png": ImageDescriptor(
        4 + 60 + 3 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44
    ),
    "res/sys/cores3/Setting/usbOutput.png": ImageDescriptor(
        4 + 60 + 3 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44
    ),
    "res/sys/cores3/Setting/busInput.png": ImageDescriptor(
        4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44
    ),
    "res/sys/cores3/Setting/busOutput.png": ImageDescriptor(
        4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4, 60, 44
    ),
    "res/sys/cores3/Develop/public.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 156),
    "res/sys/cores3/Develop/private.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 156),
    "res/sys/cores3/Run/run.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 156),
}

_APPLIST_ICO = {
    True: "res/sys/cores3/Selection/appList_selected.png",
    False: "res/sys/cores3/Selection/appList_unselected.png",
}

_APPRUN_ICO = {
    True: "res/sys/cores3/Selection/appRun_selected.png",
    False: "res/sys/cores3/Selection/appRun_unselected.png",
}

_DEVELOP_ICO = {
    True: "res/sys/cores3/Selection/develop_selected.png",
    False: "res/sys/cores3/Selection/develop_unselected.png",
}

_SETTING_ICO = {
    True: "res/sys/cores3/Selection/setting_selected.png",
    False: "res/sys/cores3/Selection/setting_unselected.png",
}


_EZDATA_ICO = {
    True: "res/sys/cores3/Selection/ezdata_selected.png",
    False: "res/sys/cores3/Selection/ezdata_unselected.png",
}


_WIFI_SETTINGS_ICO = {
    "res/sys/cores3/Setting/wifiServer.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/wifi_area_pass.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/wifi_area_server.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
    "res/sys/cores3/Setting/wifi_area_ssid.png": ImageDescriptor(4, 20 + 4 + 56 + 4, 312, 108),
}


def _draw_png(src: str):
    descriptor = _IMAGE_LIST.get(src)
    M5.Lcd.drawPng(src, descriptor.x, descriptor.y)


binary_data = None


def _playWav(wav: str):
    global binary_data
    if binary_data is None:
        with open(wav, "rb") as f:
            binary_data = f.read()
    M5.Speaker.playWav(binary_data)


class Label:

    LEFT_ALIGNED = 0
    CENTER_ALIGNED = 1

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        size: float = 1.0,
        font_align: int = LEFT_ALIGNED,
        fg_color: int = 0xFFFFFF,
        bg_color: int = 0x000000,
        font=M5.Lcd.FONTS.DejaVu12,
    ) -> None:
        self._text = text
        self._x = x
        self._y = y
        self._size = size
        self._font_align = font_align
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._font = font

    def _erase_helper(self):
        width = M5.Lcd.textWidth(self._text)
        height = M5.Lcd.fontHeight()
        if self._font_align == self.LEFT_ALIGNED:
            M5.Lcd.fillRect(self._x, self._y, width, height, self._bg_color)
        elif self._font_align == self.CENTER_ALIGNED:
            M5.Lcd.fillRect(self._x - int(width / 2), self._y, width, height, self._bg_color)

    def setText(self, text=None) -> None:
        self._load_font()
        self._erase_helper()
        if text is not None:
            self._text = text
        M5.Lcd.setTextColor(self._fg_color, self._bg_color)
        if self._font_align == self.LEFT_ALIGNED:
            M5.Lcd.drawString(self._text, self._x, self._y)
        elif self._font_align == self.CENTER_ALIGNED:
            M5.Lcd.drawCenterString(self._text, self._x, self._y)
        else:
            print("Warning: unknown alignment")

    def setTextColor(self, fg_color, bg_color):
        self._fg_color = fg_color
        self._bg_color = bg_color

    def _load_font(self):
        if type(self._font) == bytes:
            M5.Lcd.unloadFont()
            M5.Lcd.loadFont(self._font)
        else:
            M5.Lcd.setFont(self._font)


class AppBase:
    def __init__(self, ico, data=None) -> None:
        self.id = 0
        self.ico = ico
        self.src = ico.get(False)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = 0
        self.y = 80
        self.width = 320
        self.height = 160

    def registered(self):
        """
        注册到 AppManage 之后，由 AppManage 调用
        """
        _draw_png(self.ico.get(False))

    def mount(self):
        """
        应用加载，由 AppManage 调用
        """
        self._load_view()

    def _load_view(self):
        _draw_png(self.ico.get(True))
        M5.Lcd.fillRect(self.x, self.y, self.width, self.height, 0x000000)

    def ready(self):
        pass

    def handle(self, x, y):
        DEBUG and print("Touch X: ", x)
        DEBUG and print("Touch Y: ", y)

    def handle_input(self, event: KeyEvent):
        DEBUG and print("keyboard value: %d" % event.key)

    def umount(self) -> None:
        """
        应用退出的方法，由 AppManage 调用
        """
        self._disappear_view()

    def _disappear_view(self):
        _draw_png(self.ico.get(False))
        # M5.Lcd.fillRect(self.x, self.y, self.width, self.height, 0x000000)

    def is_select(self, x, y):
        if x < self.x:
            return False
        if x > (self.x + self.width):
            return False
        if y < self.y:
            return False
        if y > (self.y + self.height):
            return False
        return True


Rect = namedtuple("Rect", ["x", "y", "width", "height"])


def charge_ico(icos):
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


class WiFiSetting(AppBase):
    def __init__(self, ico, data=None) -> None:
        self.x = 4
        self.y = 20 + 4 + 56 + 4
        self.width = 312
        self.height = 108
        self._ssid_label = Label(
            "ssid",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._pwd_label = Label(
            "pwd",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12 + 35,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._server_label = Label(
            "server",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12 + 35 + 34,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._apps = [
            Rect(4, 20 + 4 + 56 + 4, 244, 108),  # option select
            Rect(4 + 249, 20 + 4 + 56 + 4, 63, 64),  # save & link
            Rect(4 + 249, 20 + 4 + 56 + 4 + 64, 63, 44),  # option select
        ]
        self._option_views = charge_ico(
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
        _draw_png("res/sys/cores3/Setting/wifiServer.png")
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * len(self.pswd_tmp))
        self._server_label.setText(self.server_tmp)

    def _select_ssid_option(self):
        _draw_png("res/sys/cores3/Setting/ssid.png")
        self._ssid_label.setTextColor(0x000000, 0xDCDDDD)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * len(self.pswd_tmp))
        self._server_label.setText(self.server_tmp)

    def _select_psd_option(self):
        _draw_png("res/sys/cores3/Setting/pass.png")
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xDCDDDD)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * len(self.pswd_tmp))
        self._server_label.setText(self.server_tmp)

    def _select_server_option(self):
        _draw_png("res/sys/cores3/Setting/server.png")
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xDCDDDD)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * len(self.pswd_tmp))
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
        if x > (rect.x + rect.width):
            return False
        if y < rect.y:
            return False
        if y > (rect.y + rect.height):
            return False
        return True


CURRENT_OPTION = (
    (100, "res/sys/cores3/Setting/charge100.png"),
    (500, "res/sys/cores3/Setting/charge500.png"),
    (900, "res/sys/cores3/Setting/charge900.png"),
    (1000, "res/sys/cores3/Setting/charge1000.png"),
    # (1500, "res/sys/cores3/Setting/charge1500.png"),
    # (2000, "res/sys/cores3/Setting/charge2000.png"),
)


class BatteryChargeSetting(AppBase):
    def __init__(self, ico) -> None:
        self.icos = charge_ico(CURRENT_OPTION)
        self._current, self.src = next(self.icos)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.width = self.descriptor.width
        self.height = self.descriptor.height

    def mount(self):
        self.get_data()
        while True:
            current, self.src = next(self.icos)
            if current == self._current:
                break
        _draw_png(self.src)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._current, self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.set_data()

            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._current, self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
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


BOOT_OPTION = (
    (0, "res/sys/cores3/Setting/bootNo.png"),
    (1, "res/sys/cores3/Setting/bootYes.png"),
)


class BootScreenSetting(AppBase):
    def __init__(self, ico) -> None:
        self.icos = charge_ico(BOOT_OPTION)
        self.boot_option, self.src = next(self.icos)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.width = self.descriptor.width
        self.height = self.descriptor.height

    def mount(self):
        self.get_data()
        while True:
            boot_option, self.src = next(self.icos)
            if boot_option == self.boot_option:
                break
        self._load_view()

    def _load_view(self):
        _draw_png(self.src)

    def handle(self, x, y):
        if self.is_select(x, y):
            self.boot_option, self.src = next(self.icos)
            self._load_view()
            self.set_data()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self.boot_option, self.src = next(self.icos)
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


class ComLinkSetting(AppBase):
    # TODO

    def __init__(self, ico) -> None:
        self.icos = charge_ico(
            (
                "res/sys/cores3/Setting/comxEnable.png",
                "res/sys/cores3/Setting/comxDisable.png",
            )
        )
        self.src = next(self.icos)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.width = self.descriptor.width
        self.height = self.descriptor.height

    def mount(self):
        _draw_png(self.src)

    def handle(self, x, y):
        if self.is_select(x, y):
            self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.mount()

    def umount(self) -> None:
        pass


USBPOWER_OPTION = (
    (False, "res/sys/cores3/Setting/usbInput.png"),
    (True, "res/sys/cores3/Setting/usbOutput.png"),
)


class USBPowerSetting(AppBase):
    def __init__(self, ico) -> None:
        self.icos = charge_ico(USBPOWER_OPTION)
        self._data, self.src = next(self.icos)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.width = self.descriptor.width
        self.height = self.descriptor.height

    def mount(self):
        self.get_data()
        while True:
            data, self.src = next(self.icos)
            if data == self._data:
                break
        _draw_png(self.src)

    def get_data(self):
        self._data = M5.Power.getUsbOutput()

    def set_data(self):
        M5.Power.setUsbOutput(self._data)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.set_data()
            self.mount()

    def umount(self) -> None:
        pass


BUSPOWER_OPTION = (
    (False, "res/sys/cores3/Setting/busInput.png"),
    (True, "res/sys/cores3/Setting/busOutput.png"),
)


class BUSPowerSetting(AppBase):
    def __init__(self, ico) -> None:
        self.icos = charge_ico(BUSPOWER_OPTION)
        self._data, self.src = next(self.icos)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.width = self.descriptor.width
        self.height = self.descriptor.height

    def mount(self):
        self.get_data()
        while True:
            data, self.src = next(self.icos)
            if data == self._data:
                break
        _draw_png(self.src)

    def get_data(self):
        self._data = M5.Power.getExtOutput()

    def set_data(self):
        M5.Power.setExtOutput(self._data)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.set_data()
            self.mount()

    def umount(self) -> None:
        pass


class SettingsApp(AppBase):
    def __init__(self, ico, data=None) -> None:
        self.ico = ico
        self.src = ico.get(False)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self._apps = [
            WiFiSetting(None, data=data),
            BatteryChargeSetting(None),
            BootScreenSetting(None),
            ComLinkSetting(None),
            USBPowerSetting(None),
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
        _draw_png(self.ico.get(True))
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
        _draw_png(self.ico.get(False))
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)


class DevApp(AppBase):
    def __init__(self, ico) -> None:
        self.ico = ico
        self.src = ico.get(False)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y

        self._mac_label = Label(
            "aabbcc112233",
            4 + 6,
            (20 + 4 + 56 + 4) + 57,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )

        self._account_label = Label(
            "XXABC",
            4 + 6,
            (20 + 4 + 56 + 4) + 57 + 40,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )

        self._account1_label = Label(
            "",
            4 + 6,
            (20 + 4 + 56 + 4) + 57 + 40 + 16,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )

        # self._token_label = Label(
        #     "AABBCCDDEEFF",
        #     4 + 6,
        #     (20 + 4 + 56 + 4) + 57 + 40 + 40,
        #     fg_color = 0x000000,
        #     bg_color = 0xeeeeef,
        #     font=MontserratMedium18.FONT
        # )

        super().__init__(ico)

    def mount(self):
        data = self.load_data()
        _draw_png(self.ico.get(True))
        _draw_png(self.src)
        self._mac_label.setText(data[0])
        if data[1] is None:
            self._account_label.setText(str(data[1]))
            self._account1_label.setText("")
            return

        if len(data[1]) > 14:
            self._account_label.setText(data[1][:14])
            self._account1_label.setText(data[1][14:])
        else:
            self._account_label.setText(data[1])
            self._account1_label.setText("")
        # self._token_label.setText(data[2])

    def load_data(self):
        mac = binascii.hexlify(machine.unique_id()).upper()
        if _HAS_SERVER is True and M5Things.status() is 2:
            infos = M5Things.info()
            if infos[0] is 0 or infos[0] is 1:
                self.src = "res/sys/cores3/Develop/private.png"
            elif infos[0] is 2:
                self.src = "res/sys/cores3/Develop/public.png"
            DEBUG and print("Develop info:")
            DEBUG and print("  Device mac: ", mac)
            DEBUG and print("  Permissions: ", Permissions.get(infos[0]))
            DEBUG and print("  Account: ", infos[1])
            return (mac, infos[1])
        else:
            self.src = "res/sys/cores3/Develop/private.png"
            return (mac, None, None)

    def handle(self, x, y):
        pass

    def umount(self) -> None:
        _draw_png(self.ico.get(False))
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)


class RunApp(AppBase):
    def __init__(self, ico) -> None:
        self.ico = ico
        self.src = ico.get(False)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y

        self._name_label = Label(
            "name",
            4 + 10,
            (20 + 4 + 56 + 4) + 4,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium18.FONT,
        )

        self._mtime_label = Label(
            "Time: 2023/5/14 12:23:43",
            4 + 10,
            (20 + 4 + 56 + 4) + 32,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium14.FONT,
        )

        self._account_label = Label(
            "Account: XXABC",
            4 + 10,
            (20 + 4 + 56 + 4) + 32 + 18,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium14.FONT,
        )

        self._ver_label = Label(
            "Ver: UIFLOW2.0 a18",
            4 + 10,
            (20 + 4 + 56 + 4) + 32 + 18 + 18,
            fg_color=0x000000,
            bg_color=0xDCDDDD,
            font=MontserratMedium14.FONT,
        )

        self._apps = [
            Rect(4, 20 + 4 + 56 + 4 + 84, 156, 72),
            Rect(4 + 156, 20 + 4 + 56 + 4 + 84, 156, 72),
        ]
        self._path = None

    def mount(self):
        _draw_png(self.ico.get(True))
        _draw_png("res/sys/cores3/Run/run.png")
        self.update_file_info("main.py")

    def update_file_info(self, filename):
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
        if x > (rect.x + rect.width):
            return False
        if y < rect.y:
            return False
        if y > (rect.y + rect.height):
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
        _draw_png(self.ico.get(False))
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)


def app_id_generator(n):
    for i in range(n):
        yield i


class AppManage:
    def __init__(self, app_num) -> None:
        self._apps = []
        self._last_app = None
        self._id_generator = app_id_generator(app_num)
        self._id = 0
        self.app = self
        self.focus = True

    def register_app(self, app: AppBase):
        self._apps.append(app)
        app.id = next(self._id_generator)

    def select_app(self, id):
        for app in self._apps:
            if id is app.id:
                self._load_app(app)
                break

    def mount(self):
        for app in self._apps:
            app.registered()

    def load_app(self, x, y):
        select_app = None
        for app in self._apps:
            if self._is_select(app, x, y):
                select_app = app
                break

        if select_app is not None:
            # Handle app switching
            if self._last_app is not select_app and self._last_app is not None:
                # destroy old app
                self._last_app.umount()

            if self._last_app is not select_app:
                # load app
                select_app.mount()
                self._last_app = select_app
                self._id = select_app.id
        else:
            # Handle the functionality of the app
            if self._last_app is not None:
                self._last_app.handle(x, y)

    def _load_app(self, new_app: AppBase):
        if new_app is not None:
            # Handle app switching
            if self._last_app is not new_app and self._last_app is not None:
                # destroy old app
                self._last_app.umount()

            if self._last_app is not new_app:
                # load app
                new_app.mount()
                self._last_app = new_app
                self._id = new_app.id

    def handle_input(self, event: KeyEvent):
        # if self.focus == True:
        #     if key == KeyCode.KEYCODE_DOWN or key == KeyCode.KEYCODE_ENTER:
        #         self.focus = False
        # else:
        #     self.app.handle_input(key)

        if self.app == self:
            if event.key in (KeyCode.KEYCODE_DOWN, KeyCode.KEYCODE_ENTER):
                self.app = self._last_app
                event.status = True
            if event.key is KeyCode.KEYCODE_RIGHT:
                id = (self._id + 1) % len(self._apps)
                self.select_app(id)
                event.status = True
            if KeyCode.KEYCODE_LEFT == event.key:
                id = len(self._apps) - 1 if (self._id - 1 < 0) else (self._id - 1)
                self.select_app(id)
                event.status = True
        else:
            self.app.handle_input(event)

        if event.status is False and event.key is KeyCode.KEYCODE_ESC:
            event.status = True
            self.app = self
            self._last_app.umount()
            self._last_app.mount()
            return

    @staticmethod
    def _is_select(app: AppBase, x, y):
        descriptor = app.descriptor
        if x < descriptor.x:
            return False
        if x > (descriptor.x + descriptor.width):
            return False
        if y < descriptor.y:
            return False
        if y > (descriptor.y + descriptor.height):
            return False
        return True


class Theme:
    Gray = 0
    Green = 1
    Red = 2
    Yellow = 3


_WIFI_STATUS_ICO = {
    WiFiStatus.INIT: "res/sys/cores3/WiFi/wifi_empty.png",
    WiFiStatus.RSSI_GOOD: "res/sys/cores3/WiFi/wifi_good.png",
    WiFiStatus.RSSI_MID: "res/sys/cores3/WiFi/wifi_mid.png",
    WiFiStatus.RSSI_WORSE: "res/sys/cores3/WiFi/wifi_worse.png",
    WiFiStatus.DISCONNECTED: "res/sys/cores3/WiFi/wifi_disconnected.png",
}


_SERVER_STATUS_ICO = {
    ServerStatus.INIT: "res/sys/cores3/Server/server_empty.png",
    ServerStatus.CONNECTED: "res/sys/cores3/Server/Server_Green.png",
    ServerStatus.DISCONNECTED: "res/sys/cores3/Server/server_error.png",
}


_BATTERY_THEME_ICO = {
    Theme.Gray: "res/sys/cores3/Battery/battery_Gray.png",
    Theme.Green: "res/sys/cores3/Battery/battery_Green.png",
    Theme.Red: "res/sys/cores3/Battery/battery_Red.png",
    Theme.Yellow: "res/sys/cores3/Battery/battery_Yellow.png",
}


class StatusBarApp:
    def __init__(self, ico, wifi) -> None:
        self.id = 0
        self.x = 0
        self.y = 0
        self.width = 320
        self.height = 20

        self._wifi = wifi
        self._time_label = Label(
            "12:23",
            160,
            2,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xEEEEEF,
            font=MontserratMedium16.FONT,
        )
        self._battery_label = Label(
            "78%",
            320 - 44 + 22 + 1,
            4,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xFEFEFE,
            font=MontserratMedium10.FONT,
        )
        self._wifi_status = WiFiStatus.INIT
        if _HAS_SERVER is False:
            self._server_status = ServerStatus.DISCONNECTED

    def registered(self):
        pass

    def mount(self):
        self._load_view()

    def _load_view(self):
        _draw_png("res/sys/cores3/Title/title_blue.png")
        self.handle(None, None)

    def _update_time(self, struct_time):
        self._time_label.setText("{:02d}:{:02d}".format(struct_time[3], struct_time[4]))

    def _update_wifi(self, status):
        self._wifi_status = status
        src = _WIFI_STATUS_ICO.get(self._wifi_status, "res/sys/cores3/WiFi/wifi_empty.png")
        _draw_png(src)

    def _update_server(self, status):
        self._server_status = status
        src = _SERVER_STATUS_ICO.get(self._server_status, "res/sys/cores3/Server/server_error.png")
        _draw_png(src)

    def _update_battery(self, battery):
        if battery >= 0 and battery <= 100:
            if battery < 20:
                src = _BATTERY_THEME_ICO.get(Theme.Red, "res/sys/cores3/Battery/battery_Green.png")
                _draw_png(src)
            elif battery < 40:
                src = _BATTERY_THEME_ICO.get(Theme.Yellow, "res/sys/cores3/Battery/battery_Green.png")
                _draw_png(src)
            elif battery <= 100:
                src = _BATTERY_THEME_ICO.get(Theme.Green, "res/sys/cores3/Battery/battery_Green.png")
                _draw_png(src)
            self._battery_label.setText("{:d}%".format(battery))
        else:
            src = _BATTERY_THEME_ICO.get(Theme.Gray, "res/sys/cores3/Battery/battery_Green.png")
            _draw_png(src)
            self._battery_label.setText("null")

    @staticmethod
    def get_local_time():
        return time.localtime()

    def get_wifi_status(self):
        status = self._wifi.connect_status()
        if status is network.STAT_GOT_IP:
            rssi = self._wifi.get_rssi()
            if rssi <= -80:
                return WiFiStatus.RSSI_WORSE
            elif rssi <= -60:
                return WiFiStatus.RSSI_MID
            else:
                return WiFiStatus.RSSI_GOOD
        else:
            return WiFiStatus.DISCONNECTED

    @staticmethod
    def get_server_status():
        if _HAS_SERVER is True:
            status = M5Things.status()
            DEBUG and print(
                "Server connect status: %d(%s)" % (status, M5THINGS_STATUS.get(status))
            )
            if status in (0, 1):
                return ServerStatus.INIT
            elif status == 2:
                return ServerStatus.CONNECTED
            elif status in (-2, -1, 3):
                return ServerStatus.DISCONNECTED
        else:
            return ServerStatus.DISCONNECTED

    def get_battery_percentage(self):
        return M5.Power.getBatteryLevel()

    def handle(self, x, y):
        self._update_time(self.get_local_time())
        self._update_wifi(self.get_wifi_status())
        self._update_server(self.get_server_status())
        self._update_battery(self.get_battery_percentage())

    def umount(self):
        pass

    def _disappear_view(self):
        pass


class BootView:
    def __init__(self) -> None:
        pass

    @classmethod
    def load(self) -> None:
        _draw_png("res/sys/cores3/boot.png")
        time.sleep(0.2)


class CoreS3_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()
        self._status_bar = StatusBarApp(None, self._wifi)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        gc.enable()
        self._wifi.connect_network(ssid, pswd)
        BootView.load()
        M5.Lcd.clear(0x000000)
        self._apps = AppManage(5)
        self._apps.register_app(SettingsApp(_SETTING_ICO, data=self._wifi))
        self._apps.register_app(DevApp(_DEVELOP_ICO))
        self._apps.register_app(RunApp(_APPRUN_ICO))
        self._apps.register_app(AppBase(_APPLIST_ICO))
        self._apps.register_app(AppBase(_EZDATA_ICO))
        self._status_bar.mount()
        self._apps.mount()
        self._apps.select_app(1)

        DEBUG and print("Run startup menu")
        last_touch_time = time.ticks_ms()
        last_update_status_time = last_touch_time

        self.i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        self._kb = CardKB(self.i2c0)
        self._event = KeyEvent()

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
                        _playWav("res/sys/cores3/click.wav")
                        self._apps.load_app(M5.Touch.getX(), M5.Touch.getY())
                    last_touch_time = time.ticks_ms()

            try:
                if self._kb.is_pressed():
                    _playWav("res/sys/cores3/click.wav")
                    self._event.key = self._kb.get_key()
                    self._event.status = False
                    self._apps.handle_input(self._event)
            except OSError:
                pass

            if time.ticks_ms() - last_update_status_time > 5000:
                # 会影响触摸发处理速度
                self._status_bar.handle(None, None)
                last_update_status_time = time.ticks_ms()
                gc.collect()
