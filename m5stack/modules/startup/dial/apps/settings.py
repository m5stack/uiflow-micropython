# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase, generator, AppSelector
import M5
from widgets.image import Image
from widgets.label import Label
from widgets.button import Button
import esp32
from .status_bar import StatusBarApp
from unit import KeyCode
from ..res import (
    SETTING_WIFI_IMG,
    WIFI_DEFAULT_IMG,
    WIFI_SSID_IMG,
    WIFI_PSK_IMG,
    WIFI_SERVER_IMG,
    SETTING_COMMON_IMG,
    BOOT_IMG,
    BOOT_NO_IMG,
    BOOT_YES_IMG,
    COMX_IMG,
    COMX_DISABLE_IMG,
    COMX_ENABLE_IMG,
    SCREEN_IMG,
    SCREEN25_IMG,
    SCREEN50_IMG,
    SCREEN75_IMG,
    SCREEN100_IMG,
)


class WiFiSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wifi = data
        super().__init__()

    def on_launch(self):
        self.get_data()
        self._option = 0
        self.focus = True

    def on_view(self):
        M5.Lcd.drawImage(SETTING_WIFI_IMG, 0, 0)
        M5.Lcd.drawImage(WIFI_DEFAULT_IMG, 9, 83)

        self._ssid_label = Label(
            "ssid",
            58,
            92,
            w=164,
            h=23,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._ssid_label.set_long_mode(Label.LONG_DOT)
        self._ssid_label.set_text(self.ssid)

        self._psk_label = Label(
            "psk",
            58,
            92 + 33,
            w=164,
            h=23,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._psk_label.set_long_mode(Label.LONG_DOT)
        if len(self.psk):
            self._psk_label.set_text("*" * 20)
        else:
            self._psk_label.set_text("")

        self._server_label = Label(
            "server",
            58,
            92 + 33 + 30,
            w=164,
            h=23,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
        )
        self._server_label.set_long_mode(Label.LONG_DOT)
        self._server_label.set_text(self.server)

        self._option_views = generator(
            (
                (0, self._select_ssid_option),
                (1, self._select_psk_option),
                (2, self._select_server_option),
            )
        )

        self._option_button = Button(None)
        self._option_button.set_pos(145, 49)
        self._option_button.set_size(127, 34)
        self._option_button.add_event(self._handle_option_button)

        self._confirm_button = Button(None)
        self._confirm_button.set_pos(0, 49)
        self._confirm_button.set_size(145, 34)
        self._confirm_button.add_event(self._handle_confirm_button)

        self._option1_button = Button(None)
        self._option1_button.set_pos(9, 83)
        self._option1_button.set_size(219, 95)
        self._option1_button.add_event(self._handle_option_button)

    def on_ready(self):
        self._status_bar = StatusBarApp(None, self._wifi)
        self._status_bar.start()

    def on_hide(self):
        self._status_bar.stop()

    def on_exit(self):
        del (
            self._ssid_label,
            self._psk_label,
            self._server_label,
            self._option_views,
            self.nvs,
            self.ssid,
            self.psk,
            self.server,
            self.ssid_tmp,
            self.psk_tmp,
            self.server_tmp,
            self._option,
            self.focus,
        )

    async def _click_event_handler(self, x, y, fw):
        self._option_button.handle(x, y)
        self._confirm_button.handle(x, y)
        self._option1_button.handle(x, y)

    async def _kb_event_handler(self, event, fw):
        if event.key == KeyCode.KEYCODE_ENTER:
            event.status = True
            self.focus = True
            self._option, view_fn = next(self._option_views)
            view_fn()
            self.set_data()

        if self.focus is False:
            return

        if event.key == KeyCode.KEYCODE_ESC:
            self.ssid_tmp = self.ssid
            self.psk_tmp = self.psk
            self.server_tmp = self.server
            self._select_default_option()
            self.focus = False
            event.status = True
            self.set_data()

        if event.key == KeyCode.KEYCODE_BACKSPACE and self._option in (0, 1, 2):
            if self._option == 0:
                self.ssid_tmp = self.ssid_tmp[:-1]
                self._ssid_label.set_text(self.ssid_tmp)
            elif self._option == 1:
                if self.psk_tmp == self.psk and len(self.psk):
                    self.psk_tmp = ""
                else:
                    self.psk_tmp = self.psk_tmp[:-1]
                self._psk_label.set_text(self.psk_tmp)
            elif self._option == 2:
                self.server_tmp = self.server_tmp[:-1]
                self._server_label.set_text(self.server_tmp)
            event.status = True
        elif event.key >= 0x20 and event.key <= 126:
            if self._option == 0:
                self.ssid_tmp += chr(event.key)
                self._ssid_label.set_text(self.ssid_tmp)
            elif self._option == 1:
                if self.psk_tmp == self.psk and len(self.psk):
                    self.psk_tmp = ""
                else:
                    self.psk_tmp += chr(event.key)
                self._psk_label.set_text(self.psk_tmp)
            elif self._option == 2:
                self.server_tmp += chr(event.key)
                self._server_label.set_text(self.server_tmp)
            event.status = True

    def _select_default_option(self):
        M5.Lcd.drawImage(WIFI_DEFAULT_IMG, 9, 83)
        self._ssid_label.set_text_color(0x000000, 0xFEFEFE)
        self._psk_label.set_text_color(0x000000, 0xFEFEFE)
        self._server_label.set_text_color(0x000000, 0xFEFEFE)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)

    def _select_ssid_option(self):
        M5.Lcd.drawImage(WIFI_SSID_IMG, 9, 83)
        self._ssid_label.set_text_color(0x000000, 0xDCDDDD)
        self._psk_label.set_text_color(0x000000, 0xFEFEFE)
        self._server_label.set_text_color(0x000000, 0xFEFEFE)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)

    def _select_psk_option(self):
        M5.Lcd.drawImage(WIFI_PSK_IMG, 9, 83)
        self._ssid_label.set_text_color(0x000000, 0xFEFEFE)
        self._psk_label.set_text_color(0x000000, 0xDCDDDD)
        self._server_label.set_text_color(0x000000, 0xFEFEFE)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)

    def _select_server_option(self):
        M5.Lcd.drawImage(WIFI_SERVER_IMG, 9, 83)
        self._ssid_label.set_text_color(0x000000, 0xFEFEFE)
        self._psk_label.set_text_color(0x000000, 0xFEFEFE)
        self._server_label.set_text_color(0x000000, 0xDCDDDD)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)

    def _handle_option_button(self, fw):
        self._option, view_fn = next(self._option_views)
        view_fn()

    def _handle_confirm_button(self, fw):
        self._select_default_option()
        self.set_data()

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        self.ssid = self.nvs.get_str("ssid0")
        self.psk = self.nvs.get_str("pswd0")
        self.server = self.nvs.get_str("server")
        self.ssid_tmp = self.ssid
        self.psk_tmp = self.psk
        self.server_tmp = self.server

    def set_data(self):
        is_save = False
        if self.ssid != self.ssid_tmp:
            self.ssid = self.ssid_tmp
            self.nvs.set_str("ssid0", self.ssid)
            print("set new ssid: ", self.ssid)
            is_save = True
        if self.psk != self.psk_tmp:
            self.psk = self.psk_tmp
            self.nvs.set_str("pswd0", self.psk)
            print("set new psk: ", self.psk)
            is_save = True
        if self.server != self.server_tmp:
            self.server = self.server_tmp
            self.nvs.set_str("server", self.server)
            print("set new server: ", self.server)
            is_save = True

        if is_save is True:
            self.nvs.commit()
            self._wifi.wlan.disconnect()
            self._wifi.wlan.active(False)
            self._wifi.wlan.active(True)
            self._wifi.connect_network(self.ssid, self.psk)


_boot_options = {
    1: BOOT_YES_IMG,
    2: BOOT_NO_IMG,
}


class BootScreenSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._boot_option = self._get_boot_option()
        self._boot_option = 1 if self._boot_option == 1 else 2
        self._options = generator(_boot_options)
        while True:
            t = next(self._options)
            if t == self._boot_option:
                break

    def on_view(self):
        self._boot_label_img = Image(use_sprite=False)
        self._boot_label_img.set_pos(0, 49)
        self._boot_label_img.set_size(120, 50)
        self._boot_label_img.set_src(BOOT_IMG)
        self._boot_label_img.add_event(self._handle_boot_option)

        self._boot_option_img = Image(use_sprite=False)
        self._boot_option_img.set_pos(120, 49)
        self._boot_option_img.set_size(120, 50)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))
        self._boot_option_img.add_event(self._handle_boot_option)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        del (self._boot_label_img, self._boot_option_img)

    async def _click_event_handler(self, x, y, fw):
        self._boot_option_img.handle(x, y)

    @staticmethod
    def _get_boot_option():
        nvs = esp32.NVS("uiflow")
        return nvs.get_u8("boot_option")

    @staticmethod
    def _set_boot_option(boot_option):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", boot_option)
        nvs.commit()

    def _handle_boot_option(self, fw):
        self._boot_option = next(self._options)
        self._set_boot_option(self._boot_option)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))


_comlink_options = {
    False: COMX_DISABLE_IMG,
    True: COMX_ENABLE_IMG,
}


class ComLinkSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._option = False
        self._options = generator(_comlink_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._label_img = Image(use_sprite=False)
        self._label_img.set_pos(0, 155)
        self._label_img.set_size(120, 53)
        self._label_img.set_src(COMX_IMG)
        self._label_img.add_event(self._handle_option)

        self._option_img = Image(use_sprite=False)
        self._option_img.set_pos(120, 155)
        self._option_img.set_size(120, 53)
        self._option_img.set_src(_comlink_options.get(self._option))
        self._option_img.add_event(self._handle_option)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        del self._option_img

    async def _click_event_handler(self, x, y, fw):
        self._option_img.handle(x, y)

    async def _btnb_event_handler(self, fw):
        pass

    def _handle_option(self, fw):
        self._option = next(self._options)
        self._option_img.set_src(_comlink_options.get(self._option))


_brightness_options = {
    64: SCREEN25_IMG,
    128: SCREEN50_IMG,
    192: SCREEN75_IMG,
    255: SCREEN100_IMG,
}


class BrightnessSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._brightness = M5.Lcd.getBrightness()
        self._brightness = self.approximate(self._brightness)
        self._options = generator(_brightness_options)
        while True:
            t = next(self._options)
            if t == self._brightness:
                break

    def on_view(self):
        self._brightness_label_img = Image(use_sprite=False)
        self._brightness_label_img.set_pos(0, 101)
        self._brightness_label_img.set_size(120, 52)
        self._brightness_label_img.set_src(SCREEN_IMG)
        self._brightness_label_img.add_event(self._handle_brightness)

        self._brightness_option_img = Image(use_sprite=False)
        self._brightness_option_img.set_pos(120, 101)
        self._brightness_option_img.set_size(120, 52)
        self._brightness_option_img.set_src(_brightness_options.get(self._brightness))
        self._brightness_option_img.add_event(self._handle_brightness)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        del (self._brightness_label_img, self._brightness_option_img)

    async def _click_event_handler(self, x, y, fw):
        self._brightness_option_img.handle(x, y)

    def _handle_brightness(self, fw):
        self._brightness = next(self._options)
        M5.Lcd.setBrightness(self._brightness)
        self._brightness_option_img.set_src(_brightness_options.get(self._brightness))

    @staticmethod
    def approximate(number):
        tolerance = 32
        for v in (64, 128, 192, 255):
            if number < 64:
                return 64
            if abs(number - v) < tolerance:
                return v


class SettingsApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan = data
        self._menus = (
            BootScreenSetting(None),
            ComLinkSetting(None),
            BrightnessSetting(None),
        )
        self._menu_selector = AppSelector(self._menus)
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        pass

    def on_view(self):
        M5.Lcd.drawImage(SETTING_COMMON_IMG, 0, 0)

    def on_ready(self):
        self._status_bar = StatusBarApp(None, self._wlan)
        self._status_bar.start()

    def on_hide(self):
        self._status_bar.stop()

    async def _click_event_handler(self, x, y, fw):
        for menu in self._menus:
            if hasattr(menu, "_click_event_handler"):
                await menu._click_event_handler(x, y, fw)

    def start(self):
        super().start()
        for menu in self._menus:
            menu.install()
        self._menus[0].start()

    def stop(self):
        for menu in self._menus:
            menu.stop()
        super().stop()
