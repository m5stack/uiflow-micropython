# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app
from .. import res
import widgets
import M5
import esp32


class WiFiSettingApp(app.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wifi = data
        super().__init__()

    def on_launch(self):
        self.get_data()
        self._option = 0

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

        self._ssid_label = widgets.Label(
            "ssid",
            70,
            32,
            w=152,
            h=16,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._ssid_label.set_long_mode(widgets.Label.LONG_DOT)
        self._ssid_label.set_text(self.ssid)

        self._psk_label = widgets.Label(
            "psk",
            70,
            54,
            w=152,
            h=16,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._psk_label.set_long_mode(widgets.Label.LONG_DOT)
        if len(self.psk):
            self._psk_label.set_text("*" * 20)
        else:
            self._psk_label.set_text("")

        self._server_label = widgets.Label(
            "server",
            70,
            76,
            w=152,
            h=16,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)
        self._server_label.set_text(self.server)

        self._submit_button = widgets.Image(use_sprite=False)
        self._submit_button.set_pos(6, 105)
        self._submit_button.set_size(228, 24)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

        self._menu_selector = app.AppSelector(
            (
                (0, self._select_default_option),
                (1, self._select_ssid_option),
                (2, self._select_psk_option),
                (3, self._select_server_option),
                (4, self._select_submit_button_option),
            )
        )
        self._option, view_fn = self._menu_selector.index(0)
        view_fn()

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        del (
            self._ssid_label,
            self._psk_label,
            self._server_label,
            self.nvs,
            self.ssid,
            self.psk,
            self.server,
            self.ssid_tmp,
            self.psk_tmp,
            self.server_tmp,
            self._option,
        )

    async def _kb_event_handler(self, event, fw):
        if event.key == 182:  # down key
            self._option, view_fn = self._menu_selector.next()
            view_fn()
            event.status = True
        elif event.key == 181:  # up key
            self._option, view_fn = self._menu_selector.prev()
            view_fn()
            event.status = True

        if event.key == 0x0D and self._option == 4:  # Enter key
            self._option, view_fn = self._menu_selector.current()
            view_fn()
            event.status = True

        if event.key == 0x1B:  # ESC key
            self.ssid_tmp = self.ssid
            self.psk_tmp = self.psk
            self.server_tmp = self.server
            self._option, view_fn = self._menu_selector.index(0)
            view_fn()
            event.status = True

        if event.key == 0x08 and self._option in (1, 2, 3):
            print("backspace")
            if self._option == 1:
                self.ssid_tmp = self.ssid_tmp[:-1]
                self._ssid_label.set_text(self.ssid_tmp)
            elif self._option == 2:
                self.psk_tmp = self.psk_tmp[:-1]
                self._psk_label.set_text(self.psk_tmp)
            elif self._option == 3:
                self.server_tmp = self.server_tmp[:-1]
                self._server_label.set_text(self.server_tmp)
            event.status = True
        elif event.key >= 0x20 and event.key <= 126:
            if self._option == 1:
                self.ssid_tmp += chr(event.key)
                self._ssid_label.set_text(self.ssid_tmp)
            elif self._option == 2:
                self.psk_tmp += chr(event.key)
                self._psk_label.set_text(self.psk_tmp)
            elif self._option == 3:
                self.server_tmp += chr(event.key)
                self._server_label.set_text(self.server_tmp)
            event.status = True

    def _select_default_option(self):
        M5.Lcd.drawImage(res.WIFI_DEFAULT_IMG, 6, 22)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_ssid_option(self):
        M5.Lcd.drawImage(res.WIFI_SSID_IMG, 6, 22)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_psk_option(self):
        M5.Lcd.drawImage(res.WIFI_PSK_IMG, 6, 22)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_server_option(self):
        M5.Lcd.drawImage(res.WIFI_SERVER_IMG, 6, 22)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_submit_button_option(self):
        M5.Lcd.drawImage(res.WIFI_DEFAULT_IMG, 6, 22)
        self._ssid_label.set_text(self.ssid_tmp)
        if len(self.psk_tmp) == 0:
            self._psk_label.set_text("")
        else:
            self._psk_label.set_text("*" * 20)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_SELECT_BUTTON_IMG)

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


class BootScreenSetting(app.AppBase):
    _boot_options = {
        1: res.ENABLE_IMG,
        2: res.DISABLE_IMG,
    }

    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._option = self._get_boot_option()
        self._option = 1 if self._option == 1 else 2
        self._options = app.generator(self._boot_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._menu_label = widgets.Label(
            "Boot Screen",
            14,
            65,
            w=155,
            h=22,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )

        self._option_img = widgets.Image(use_sprite=False)
        self._option_img.set_pos(193, 69)
        self._option_img.set_size(30, 14)
        self._option_img.set_src(self._boot_options.get(self._option))

    def on_ready(self):
        M5.Lcd.drawImage(res.CARD_228x32_SELECT_IMG, 6, 60)
        self._menu_label.set_text("Boot Screen")
        self._option_img.set_src(self._boot_options.get(self._option))

    def on_hide(self):
        M5.Lcd.drawImage(res.CARD_228x32_UNSELECT_IMG, 6, 60)
        self._menu_label.set_text("Boot Screen")
        self._option_img.set_src(self._boot_options.get(self._option))

    def on_exit(self):
        del (self._menu_label, self._option_img)

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
        self._option = next(self._options)
        self._set_boot_option(self._option)
        self._option_img.set_src(self._boot_options.get(self._option))

    async def _kb_event_handler(self, event, fw):
        if event.key == 0x0D:  # Enter key
            self._handle_boot_option(fw)
            event.status = True


class ComLinkSetting(app.AppBase):
    _comlink_options = {
        False: res.DISABLE_IMG,
        True: res.ENABLE_IMG,
    }

    def __init__(self, icos: dict) -> None:
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._option = False
        self._options = app.generator(self._comlink_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._menu_label = widgets.Label(
            "COM.X Link",
            14,
            103,
            w=155,
            h=22,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )

        self._option_img = widgets.Image(use_sprite=False)
        self._option_img.set_pos(193, 106)
        self._option_img.set_size(30, 14)
        self._option_img.set_src(self._comlink_options.get(self._option))

    def on_ready(self):
        M5.Lcd.drawImage(res.CARD_228x32_SELECT_IMG, 6, 98)
        self._menu_label.set_text("COM.X Link")
        self._option_img.set_src(self._comlink_options.get(self._option))

    def on_hide(self):
        M5.Lcd.drawImage(res.CARD_228x32_UNSELECT_IMG, 6, 98)
        self._menu_label.set_text("COM.X Link")
        self._option_img.set_src(self._comlink_options.get(self._option))

    def on_exit(self):
        del self._option_img

    async def _btnb_event_handler(self, fw):
        pass

    def _handle_option(self, fw):
        self._option = next(self._options)
        self._option_img.set_src(self._comlink_options.get(self._option))

    async def _kb_event_handler(self, event, fw):
        if event.key == 0x0D:  # Enter key
            self._handle_option(fw)
            event.status = True


class BrightnessSettingApp(app.AppBase):
    _brightness_options = {64: "25%", 128: "50%", 192: "75%", 255: "100%"}

    def __init__(self, icos: dict) -> None:
        super().__init__()

    def on_install(self):
        self.on_launch()
        self.on_view()
        self.on_hide()

    def on_launch(self):
        self._brightness = M5.Lcd.getBrightness()
        self._brightness = self.approximate(self._brightness)
        self._options = app.generator(self._brightness_options)
        while True:
            t = next(self._options)
            if t == self._brightness:
                break

    def on_view(self):
        self._menu_label = widgets.Label(
            "Brightness",
            14,
            27,
            w=155,
            h=22,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )

        self._brightness_label = widgets.Label(
            "server",
            223,
            30,
            w=40,
            h=15,
            font_align=widgets.Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium12_VLW,
        )

    def on_ready(self):
        M5.Lcd.drawImage(res.CARD_228x32_SELECT_IMG, 6, 22)
        self._menu_label.set_text("Brightness")
        self._brightness_label.set_text(self._brightness_options.get(self._brightness))

    def on_hide(self):
        M5.Lcd.drawImage(res.CARD_228x32_UNSELECT_IMG, 6, 22)
        self._menu_label.set_text("Brightness")
        self._brightness_label.set_text(self._brightness_options.get(self._brightness))

    def on_exit(self):
        del (self._menu_label, self._brightness_label)

    def _handle_brightness(self, fw):
        self._brightness = next(self._options)
        M5.Lcd.setBrightness(self._brightness)
        self._brightness_label.set_text(self._brightness_options.get(self._brightness))

    @staticmethod
    def approximate(number):
        tolerance = 32
        for v in (64, 128, 192, 255):
            if number < 64:
                return 64
            if abs(number - v) < tolerance:
                return v

    async def _kb_event_handler(self, event, fw):
        if event.key == 0x0D:  # Enter key
            self._handle_brightness(fw)
            event.status = True


class GeneralSettingApp(app.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._menus = (
            BrightnessSettingApp(None),
            BootScreenSetting(None),
            ComLinkSetting(None),
        )
        self._menu_selector = app.AppSelector(self._menus)
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        pass

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def start(self):
        super().start()
        for menu in self._menus:
            menu.install()
        self._menu_selector.current().resume()

    def stop(self):
        for menu in self._menus:
            menu.uninstall()
        super().stop()

    async def _kb_event_handler(self, event, fw):
        if event.key == 182:  # down key
            self._menu_selector.current().pause()
            app = self._menu_selector.next().resume()
            event.status = True
        elif event.key == 181:  # up key
            self._menu_selector.current().pause()
            self._menu_selector.prev().resume()
            event.status = True
        elif event.key == 0x0D:  # Enter key
            app = self._menu_selector.current()
            await app._kb_event_handler(event, fw)


class SettingsApp(app.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan = data
        self._menus = (
            WiFiSettingApp(None, data=self._wlan),
            GeneralSettingApp(None),
        )
        self._menu_selector = app.AppSelector(self._menus)
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._imgs = []
        self._icos = []
        self._labels = []
        self._app = None

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

        self._img0 = widgets.Image(use_sprite=False)
        self._img0.set_pos(6, 22)
        self._img0.set_size(228, 32)
        self._img0.set_src(res.CARD_228x32_SELECT_IMG)
        self._imgs.append(self._img0)

        self._ico0 = widgets.Image(use_sprite=False)
        self._ico0.set_pos(9, 25)
        self._ico0.set_size(26, 26)
        self._ico0.set_src(res.WLAN_ICO_IMG)
        self._icos.append(self._ico0)

        self._label0 = widgets.Label(
            "",
            40,
            27,
            w=182,
            h=22,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )
        self._label0.set_text("WLAN")
        self._labels.append(self._label0)

        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 25)

        self._img1 = widgets.Image(use_sprite=False)
        self._img1.set_pos(6, 60)
        self._img1.set_size(228, 32)
        self._img1.set_src(res.CARD_228x32_UNSELECT_IMG)
        self._imgs.append(self._img1)

        self._ico1 = widgets.Image(use_sprite=False)
        self._ico1.set_pos(9, 63)
        self._ico1.set_size(26, 26)
        self._ico1.set_src(res.GENERAL_ICO_IMG)
        self._icos.append(self._ico1)

        self._label1 = widgets.Label(
            "",
            40,
            65,
            w=182,
            h=22,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )
        self._label1.set_text("General")
        self._labels.append(self._label1)

        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 63)

    def on_ready(self):
        pass

    def on_hide(self):
        self._app = None

    async def _kb_event_handler(self, event, fw):
        if self._app:
            await self._app._kb_event_handler(event, fw)
            return

        if event.key == 0x0D:  # Enter key
            self._app = self._menu_selector.current()
            print("current app:", self._app)
            await fw.load(self._app)
            event.status = True
        elif event.key == 182:  # down key
            self._menu_selector.index(1)
            self._imgs[0].set_src(res.CARD_228x32_UNSELECT_IMG)
            self._icos[0].refresh()
            # self._labels[0].refresh()
            self._labels[0].set_text("WLAN")
            M5.Lcd.drawImage(res.CARET_RIGHT, 213, 25)

            self._imgs[1].set_src(res.CARD_228x32_SELECT_IMG)
            self._icos[1].refresh()
            # self._labels[1].refresh()
            self._labels[1].set_text("General")
            M5.Lcd.drawImage(res.CARET_RIGHT, 213, 63)

            event.status = True
        elif event.key == 181:  # up key
            self._menu_selector.index(0)
            self._imgs[0].set_src(res.CARD_228x32_SELECT_IMG)
            self._icos[0].refresh()
            # self._labels[0].refresh()
            self._labels[0].set_text("WLAN")
            M5.Lcd.drawImage(res.CARET_RIGHT, 213, 25)

            self._imgs[1].set_src(res.CARD_228x32_UNSELECT_IMG)
            self._icos[1].refresh()
            # self._labels[1].refresh()
            self._labels[1].set_text("General")
            M5.Lcd.drawImage(res.CARET_RIGHT, 213, 63)
            event.status = True

    async def _btna_event_handler(self, fw):
        self._menu_selector.index(0)
        self._app = None
