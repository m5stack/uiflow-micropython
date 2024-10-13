# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
import M5
import widgets
import esp32
from unit import KeyCode


class WiFiSetting(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._wifi = data
        super().__init__()

    def on_launch(self):
        self.get_data()
        self.focus = True

    def on_view(self):
        origin_x = 4
        origin_y = 4

        self._bg_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._bg_img.set_pos(origin_x, origin_y)
        self._bg_img.set_size(312, 108)
        self._bg_img.set_src("/system/cores3/Setting/wifiServer.png")

        self._ssid_label = widgets.Label(
            "ssid",
            origin_x + 56 + 2,
            origin_y + 12,
            w=180,
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
            origin_x + 56 + 2,
            origin_y + 12 + 35,
            w=180,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-16.vlw",
            parent=self._lcd,
        )
        self._psk_label.set_long_mode(widgets.Label.LONG_DOT)
        if len(self.ssid):
            self._psk_label.set_text("*" * 20)
        else:
            self._psk_label.set_text("")

        self._server_label = widgets.Label(
            "server",
            origin_x + 56 + 2,
            origin_y + 12 + 35 + 34,
            w=190,
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

        self._option_button = widgets.Button(None)
        self._option_button.set_pos(4, 20 + 4 + 56 + 4)
        self._option_button.set_size(244, 108)
        self._option_button.add_event(self._handle_option_button)

        self._confirm_button = widgets.Button(None)
        self._confirm_button.set_pos(4 + 249, 20 + 4 + 56 + 4)
        self._confirm_button.set_size(63, 64)
        self._confirm_button.add_event(self._handle_confirm_button)

        self._option1_button = widgets.Button(None)
        self._option1_button.set_pos(4 + 249, 20 + 4 + 56 + 4 + 64)
        self._option1_button.set_size(63, 64)
        self._option1_button.add_event(self._handle_option_button)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass

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

        if self.focus is False:
            return

        if event.key == KeyCode.KEYCODE_ESC:
            self.ssid_tmp = self.ssid
            self.psk_tmp = self.psk
            self.server_tmp = self.server
            self._select_default_option()
            self.focus = False
            event.status = True

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
        self._bg_img.set_src("/system/cores3/Setting/wifiServer.png")
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
        self._bg_img.set_src("/system/cores3/Setting/ssid.png")
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
        self._bg_img.set_src("/system/cores3/Setting/pass.png")
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
        self._bg_img.set_src("/system/cores3/Setting/server.png")
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
            # print("set new ssid: ", self.ssid)
            is_save = True
        if self.psk != self.psk_tmp:
            self.psk = self.psk_tmp
            self.nvs.set_str("pswd0", self.psk)
            # print("set new ssid: ", self.ssid)
            is_save = True
        if self.server != self.server_tmp:
            self.server = self.server_tmp
            self.nvs.set_str("server", self.server)
            # print("set new server: ", self.server)
            is_save = True

        if is_save is True:
            self.nvs.commit()
            self._wifi.wlan.disconnect()
            self._wifi.wlan.active(False)
            self._wifi.wlan.active(True)
            self._wifi.connect_network(self.ssid, self.psk)


_current_options = {
    100: "/system/cores3/Setting/charge100.png",
    500: "/system/cores3/Setting/charge500.png",
    900: "/system/cores3/Setting/charge900.png",
    1000: "/system/cores3/Setting/charge1000.png",
}


class BatteryChargeSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos
        super().__init__()

    def install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._current = self._get_charge_current()
        self._options = app_base.generator(_current_options)
        while True:
            t = next(self._options)
            if t == self._current:
                break

    def on_view(self):
        self._origin_x = 4
        self._origin_y = 4 + 108 + 4

        if hasattr(self, "_option_img") is False:
            self._option_img = widgets.Image(use_sprite=False, parent=self._lcd)
            self._option_img.set_pos(self._origin_x, self._origin_y)
            self._option_img.set_size(60, 44)
            self._option_img.set_src(_current_options.get(self._current))

        self._button = widgets.Button(None)
        self._button.set_pos(4, 20 + 4 + 56 + 4 + 108 + 4)
        self._button.set_size(60, 44)
        self._button.add_event(self._handle_charge_current)

    def on_ready(self):
        self._option_img._draw(True)

    def on_hide(self):
        self._option_img._draw(True)

    def on_exit(self):
        del self._option_img

    async def _click_event_handler(self, x, y, fw):
        self._button.handle(x, y)

    def _handle_charge_current(self, fw):
        self._current = next(self._options)
        self._set_charge_current(self._current)
        self._option_img.set_src(_current_options.get(self._current))
        self._lcd.push(0, 80)

    def _get_charge_current(self):
        self.nvs = esp32.NVS("uiflow")
        try:
            return self.nvs.get_i32("charge_current")
        except OSError:
            return 500

    def _set_charge_current(self, current):
        M5.Power.setBatteryCharge(True)
        M5.Power.setChargeCurrent(current)
        self.nvs.set_i32("charge_current", current)
        self.nvs.commit()


_boot_options = {
    1: "/system/cores3/Setting/bootYes.png",
    2: "/system/cores3/Setting/bootNo.png",
}


class BootScreenSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos
        super().__init__()

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
        self._origin_x = 4 + 60 + 3
        self._origin_y = 4 + 108 + 4

        self._boot_option_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._boot_option_img.set_pos(self._origin_x, self._origin_y)
        self._boot_option_img.set_size(60, 44)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))
        self._boot_option_img.add_event(self._handle_boot_option)

        self._button = widgets.Button(None)
        self._button.set_pos(4 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4)
        self._button.set_size(60, 44)
        self._button.add_event(self._handle_boot_option)

    def on_ready(self):
        self._boot_option_img._draw(True)

    def on_hide(self):
        self._boot_option_img._draw(True)

    def on_exit(self):
        del self._boot_option_img

    async def _click_event_handler(self, x, y, fw):
        self._button.handle(x, y)

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
        self._lcd.push(0, 80)


_comlink_options = {
    False: "/system/cores3/Setting/comxDisable.png",
    True: "/system/cores3/Setting/comxEnable.png",
}


class ComLinkSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._option = False
        self._options = app_base.generator(_comlink_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._origin_x = 4 + 60 + 3 + 60 + 3
        self._origin_y = 4 + 108 + 4

        self._option_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._option_img.set_pos(self._origin_x, self._origin_y)
        self._option_img.set_size(60, 44)
        self._option_img.set_src(_comlink_options.get(self._option))

        self._button = widgets.Button(None)
        self._button.set_pos(4 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4)
        self._button.set_size(60, 44)
        self._button.add_event(self._handle_option)

    def on_ready(self):
        self._option_img._draw(True)

    def on_hide(self):
        self._option_img._draw(True)

    def on_exit(self):
        del self._option_img

    async def _click_event_handler(self, x, y, fw):
        self._button.handle(x, y)

    async def _btnb_event_handler(self, fw):
        pass

    def _handle_option(self, fw):
        self._option = next(self._options)
        self._option_img.set_src(_comlink_options.get(self._option))
        self._lcd.push(0, 80)


_usbpower_options = {
    False: "/system/cores3/Setting/usbInput.png",
    True: "/system/cores3/Setting/usbOutput.png",
}


class USBPowerSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._option = M5.Power.getUsbOutput()
        self._options = app_base.generator(_usbpower_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._origin_x = 4 + 60 + 3 + 60 + 3 + 60 + 3
        self._origin_y = 4 + 108 + 4

        self._option_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._option_img.set_pos(self._origin_x, self._origin_y)
        self._option_img.set_size(60, 44)
        self._option_img.set_src(_usbpower_options.get(self._option))

        self._button = widgets.Button(None)
        self._button.set_pos(4 + 60 + 3 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4)
        self._button.set_size(60, 44)
        self._button.add_event(self._handle_option)

    def on_ready(self):
        self._option_img._draw(True)

    def on_hide(self):
        self._option_img._draw(True)

    def on_exit(self):
        del self._option_img

    async def _click_event_handler(self, x, y, fw):
        self._button.handle(x, y)

    async def _btnb_event_handler(self, fw):
        pass

    def _handle_option(self, fw):
        self._option = next(self._options)
        M5.Power.setUsbOutput(self._option)
        self._option_img.set_src(_usbpower_options.get(self._option))
        self._lcd.push(0, 80)


_buspower_options = {
    False: "/system/cores3/Setting/busInput.png",
    True: "/system/cores3/Setting/busOutput.png",
}


class BUSPowerSetting(app_base.AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._option = M5.Power.getExtOutput()
        self._options = app_base.generator(_buspower_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._origin_x = 4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3
        self._origin_y = 4 + 108 + 4

        self._option_img = widgets.Image(use_sprite=False, parent=self._lcd)
        self._option_img.set_pos(self._origin_x, self._origin_y)
        self._option_img.set_size(60, 44)
        self._option_img.set_src(_buspower_options.get(self._option))
        self._button = widgets.Button(None)
        self._button.set_pos(4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3, 20 + 4 + 56 + 4 + 108 + 4)
        self._button.set_size(60, 44)
        self._button.add_event(self._handle_power_setting)

    def on_ready(self):
        self._button._draw(False)

    def on_hide(self):
        pass

    def on_exit(self):
        del self._option_img

    async def _click_event_handler(self, x, y, fw):
        self._button.handle(x, y)

    def _handle_power_setting(self, fw):
        self._option = next(self._options)
        M5.Power.setExtOutput(self._option)
        self._option_img.set_src(_buspower_options.get(self._option))
        self._lcd.push(0, 80)


class SettingsApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos
        self._menus = (
            WiFiSetting(self._lcd, data=data),
            BatteryChargeSetting(self._lcd),
            BootScreenSetting(self._lcd),
            ComLinkSetting(self._lcd),
            USBPowerSetting(self._lcd),
            BUSPowerSetting(self._lcd),
        )
        self._menu_selector = app_base.AppSelector(self._menus)
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage("/system/cores3/Selection/setting_unselected.png", 5 + 62 * 0, 20 + 4)
        self.descriptor = app_base.Descriptor(x=5, y=20 + 4, w=62, h=56)

    def on_launch(self):
        pass

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 80
        M5.Lcd.drawImage("/system/cores3/Selection/setting_selected.png", 5 + 62 * 0, 20 + 4)
        self._lcd.clear()

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage("/system/cores3/Selection/setting_unselected.png", 5 + 62 * 0, 20 + 4)

    async def _click_event_handler(self, x, y, fw):
        for menu in self._menus:
            if hasattr(menu, "_click_event_handler"):
                await menu._click_event_handler(x, y, fw)
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

    async def _kb_event_handler(self, event, fw):
        for menu in self._menus:
            if hasattr(menu, "_kb_event_handler"):
                await menu._kb_event_handler(event, fw)
                self._lcd.push(self._origin_x, self._origin_y)

    def start(self):
        super().start()
        for menu in self._menus:
            menu.install()
        self._menus[0].start()
        self._lcd.push(self._origin_x, self._origin_y)

    def stop(self):
        for menu in self._menus:
            menu.stop()
        super().stop()
        self._lcd.push(self._origin_x, self._origin_y)
