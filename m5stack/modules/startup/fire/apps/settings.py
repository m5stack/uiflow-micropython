# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import M5
import widgets
import esp32
from .. import res
from unit import KeyCode
from . import app_list


class WiFiSetting(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wifi = data
        self._lcd = icos

    def on_launch(self):
        self.get_data()
        self._option = 0
        self.focus = True

    def on_view(self):
        self._origin_x = 4
        self._origin_y = 4

        self._bg_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._bg_img.set_pos(self._origin_x, self._origin_y)
        self._bg_img.set_size(312, 108)
        self._bg_img.set_src(res.SETTING_WIFI_IMG)

        self._rect0 = app_list.Rectangle(
            self._origin_x + 96, self._origin_y + 7, 144, 26, 0xFEFEFE, 0xFEFEFE, self._lcd
        )

        self._ssid_label = widgets.Label(
            "ssid",
            self._origin_x + 98,
            self._origin_y + 12,
            w=144,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
            parent=self._lcd,
        )
        self._ssid_label.set_long_mode(widgets.Label.LONG_DOT)
        self._ssid_label.set_text(self.ssid)

        self._psk_label = widgets.Label(
            "pwd",
            self._origin_x + 98,
            self._origin_y + 12 + 35,
            w=144,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
            parent=self._lcd,
        )
        self._psk_label.set_long_mode(widgets.Label.LONG_DOT)
        if len(self.psk):
            self._psk_label.set_text("*" * 20)
        else:
            self._psk_label.set_text("")

        self._server_label = widgets.Label(
            "server",
            self._origin_x + 98,
            self._origin_y + 12 + 35 + 34,
            w=144,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
            parent=self._lcd,
        )
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)
        self._server_label.set_text(self.server)

        self._option_views = app_base.generator(
            (
                (0, self._select_ssid_option),
                (1, self._select_psk_option),
                (2, self._select_server_option),
            )
        )

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass

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
        self._bg_img.refresh()
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
        # self._bg_img.set_src(res.SETTING_WIFI_IMG)
        self._rect0.set_color(0xFEFEFE, 0xFEFEFE)
        self._rect0.set_pos(self._origin_x + 98, self._origin_y + 7)
        self._rect0.set_color(0xDCDDDD, 0xDCDDDD)
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
        # self._bg_img.set_src(res.SETTING_WIFI_IMG)
        self._rect0.set_color(0xFEFEFE, 0xFEFEFE)
        self._rect0.set_pos(self._origin_x + 98, self._origin_y + 7 + 36)
        self._rect0.set_color(0xDCDDDD, 0xDCDDDD)
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
        # self._bg_img.set_src(res.SETTING_WIFI_IMG)
        self._rect0.set_color(0xFEFEFE, 0xFEFEFE)
        self._rect0.set_pos(self._origin_x + 98, self._origin_y + 7 + 36 + 36)
        self._rect0.set_color(0xDCDDDD, 0xDCDDDD)
        self._ssid_label.set_text_color(0x000000, 0xFEFEFE)
        self._psk_label.set_text_color(0x000000, 0xFEFEFE)
        self._server_label.set_text_color(0x000000, 0xDCDDDD)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)

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


_brightness_options = {
    64: res.SCREEN25_IMG,
    128: res.SCREEN50_IMG,
    192: res.SCREEN75_IMG,
    255: res.SCREEN100_IMG,
}


class BrightnessSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._brightness = M5.Lcd.getBrightness()
        self._brightness = self.approximate(self._brightness)
        self._options = app_base.generator(_brightness_options)
        while True:
            t = next(self._options)
            if t == self._brightness:
                break

    def on_view(self):
        self._origin_x = 4
        self._origin_y = 4 + 108 + 4

        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._select_img.set_pos(self._origin_x + 0, self._origin_y + 6)
        self._select_img.set_size(72, 32)
        self._select_img.set_src(res.SETTING_SELECT_IMG)

        self._brightness_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._brightness_img.set_pos(self._origin_x + 6, self._origin_y + 0)
        self._brightness_img.set_size(60, 44)
        self._brightness_img.set_src(_brightness_options.get(self._brightness))

    def on_ready(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src(res.SETTING_SELECT_IMG)
        self._brightness_img._draw(False)

    def on_hide(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src(res.SETTING_UNSELECT_IMG)
        self._brightness_img._draw(False)

    def on_exit(self):
        del self._select_img, self._brightness_img

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        self._brightness = next(self._options)
        M5.Lcd.setBrightness(self._brightness)
        self._brightness_img.set_src(_brightness_options.get(self._brightness))

    @staticmethod
    def approximate(number):
        tolerance = 32
        for v in (64, 128, 192, 255):
            if number < 64:
                return 64
            if abs(number - v) < tolerance:
                return v


_boot_options = {
    1: res.BOOT_YES_IMG,
    2: res.BOOT_NO_IMG,
}


class BootScreenSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._boot_option = self._get_boot_option()
        self._boot_option = 1 if self._boot_option == 1 else 2
        self._options = app_base.generator(_boot_options)
        while True:
            t = next(self._options)
            if t == self._boot_option:
                break

    def on_view(self):
        self._origin_x = 4 + 72 + 8
        self._origin_y = 4 + 108 + 4

        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._select_img.set_pos(self._origin_x + 0, self._origin_y + 6)
        self._select_img.set_size(72, 32)
        self._select_img.set_src(res.SETTING_SELECT_IMG)

        self._boot_option_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._boot_option_img.set_pos(self._origin_x + 6, self._origin_y + 0)
        self._boot_option_img.set_size(60, 44)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))

    def on_ready(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src(res.SETTING_SELECT_IMG)
        self._boot_option_img._draw(True)

    def on_hide(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src(res.SETTING_UNSELECT_IMG)
        self._boot_option_img._draw(True)

    def on_exit(self):
        del self._select_img, self._boot_option_img

    @staticmethod
    def _get_boot_option():
        nvs = esp32.NVS("uiflow")
        return nvs.get_u8("boot_option")

    @staticmethod
    def _set_boot_option(boot_option):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", boot_option)
        nvs.commit()

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        self._boot_option = next(self._options)
        self._set_boot_option(self._boot_option)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))


class SettingsApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wlan_app = WiFiSetting(self._lcd, data=data)
        self._menus = (
            BrightnessSetting(self._lcd),
            BootScreenSetting(self._lcd),
        )
        self._menu_selector = app_base.AppSelector(self._menus)

    def on_install(self):
        M5.Lcd.drawImage(res.SETTING_UNSELECTED_IMG, 5 + 62 * 0, 0)

    def on_launch(self):
        pass

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 56

        M5.Lcd.drawImage(res.SETTING_SELECTED_IMG, 5 + 62 * 0, 0)

        self._lcd.clear()
        self._lcd.fillRect(4 + 72 + 8 + 72 + 8, 4 + 108 + 4, 72, 44, 0x404040)
        self._lcd.fillRect(4 + 72 + 8 + 72 + 8 + 72 + 8, 4 + 108 + 4, 72, 44, 0x404040)
        self._lcd.drawImage(res.BAR1_IMG, 0, 220 - 56)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage(res.SETTING_UNSELECTED_IMG, 5 + 62 * 0, 0)

    async def _kb_event_handler(self, event, fw):
        await self._wlan_app._kb_event_handler(event, fw)
        self._lcd.push(self._origin_x, self._origin_y)

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        await self._menus[0]._btnb_event_handler(fw)
        self._menu_selector.current().pause()
        self._menu_selector.next().resume()
        self._lcd.push(self._origin_x, self._origin_y)

    async def _btnc_event_handler(self, fw):
        await self._menu_selector.current()._btnc_event_handler(fw)
        self._lcd.push(self._origin_x, self._origin_y)

    def start(self):
        super().start()
        self._wlan_app.start()
        for menu in self._menus:
            menu.install()
        self._menus[0].start()
        self._lcd.push(self._origin_x, self._origin_y)

    def stop(self):
        super().stop()
        self._wlan_app.stop()
        for menu in self._menus:
            menu.stop()
        self._lcd.push(self._origin_x, self._origin_y)
