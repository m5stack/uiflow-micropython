# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import res
import widgets
import M5
import esp32


class WiFiSettingApp(app_base.AppBase):
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

        self._menu_selector = app_base.AppSelector(
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

    async def _btnb_enter_event_handler(self, fw):
        self._option, view_fn = self._menu_selector.current()
        view_fn()

    async def _btnb_back_event_handler(self, fw):
        self.ssid_tmp = self.ssid
        self.psk_tmp = self.psk
        self.server_tmp = self.server
        self._option, view_fn = self._menu_selector.index(0)
        view_fn()

    async def _btna_next_event_handler(self, fw):
        self._option, view_fn = self._menu_selector.prev()
        view_fn()

    async def _btnc_next_event_handler(self, fw):
        self._option, view_fn = self._menu_selector.next()
        view_fn()

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


class EthernetSettingApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._net_if = data
        super().__init__()

    def on_launch(self):
        self.get_data()
        self._option = 0

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

        self._ip_label = widgets.Label(
            "ip",
            70,
            32,
            w=152,
            h=16,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._ip_label.set_long_mode(widgets.Label.LONG_DOT)
        self._ip_label.set_text(self.ip)

        self._mask_label = widgets.Label(
            "mask",
            70,
            54,
            w=152,
            h=16,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium10_VLW,
        )
        self._mask_label.set_long_mode(widgets.Label.LONG_DOT)
        self._mask_label.set_text(self.mask)

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

        self._menu_selector = app_base.AppSelector(
            (
                (0, self._select_default_option),
                (1, self._select_ip_option),
                (2, self._select_mask_option),
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
            self._ip_label,
            self._mask_label,
            self._server_label,
            self.nvs,
            self.ip,
            self.mask,
            self.server,
            self.ip_tmp,
            self.mask_tmp,
            self.server_tmp,
            self._option,
        )

    async def _btnb_enter_event_handler(self, fw):
        self._option, view_fn = self._menu_selector.current()
        view_fn()

    async def _btnb_back_event_handler(self, fw):
        self.ip_tmp = self.ip
        self.mask_tmp = self.mask
        self.server_tmp = self.server
        self._option, view_fn = self._menu_selector.index(0)
        view_fn()

    async def _btna_next_event_handler(self, fw):
        self._option, view_fn = self._menu_selector.prev()
        view_fn()

    async def _btnc_next_event_handler(self, fw):
        self._option, view_fn = self._menu_selector.next()
        view_fn()

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
            self.ip_tmp = self.ip
            self.mask_tmp = self.mask
            self.server_tmp = self.server
            self._option, view_fn = self._menu_selector.index(0)
            view_fn()
            event.status = True

        if event.key == 0x08 and self._option in (1, 2, 3):
            print("backspace")
            if self._option == 1:
                self.ip_tmp = self.ip_tmp[:-1]
                self._ip_label.set_text(self.ip_tmp)
            elif self._option == 2:
                self.mask_tmp = self.mask_tmp[:-1]
                self._mask_label.set_text(self.mask_tmp)
            elif self._option == 3:
                self.server_tmp = self.server_tmp[:-1]
                self._server_label.set_text(self.server_tmp)
            event.status = True
        elif event.key >= 0x20 and event.key <= 126:
            if self._option == 1:
                self.ip_tmp += chr(event.key)
                self._ip_label.set_text(self.ip_tmp)
            elif self._option == 2:
                self.mask_tmp += chr(event.key)
                self._mask_label.set_text(self.mask_tmp)
            elif self._option == 3:
                self.server_tmp += chr(event.key)
                self._server_label.set_text(self.server_tmp)
            event.status = True

    def _select_default_option(self):
        M5.Lcd.drawImage(res.ETHERNET_DEFAULT_IMG, 6, 22)
        self._ip_label.set_text(self.ip_tmp)
        self._mask_label.set_text(self.mask_tmp)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_ip_option(self):
        M5.Lcd.drawImage(res.ETHERNET_IP_IMG, 6, 22)
        self._ip_label.set_text(self.ip_tmp)
        self._mask_label.set_text(self.mask_tmp)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_mask_option(self):
        M5.Lcd.drawImage(res.ETHERNET_MASK_IMG, 6, 22)
        self._ip_label.set_text(self.ip_tmp)
        self._mask_label.set_text(self.mask_tmp)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_server_option(self):
        M5.Lcd.drawImage(res.ETHERNET_SERVER_IMG, 6, 22)
        self._ip_label.set_text(self.ip_tmp)
        self._mask_label.set_text(self.mask_tmp)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_UNSELECT_BUTTON_IMG)

    def _select_submit_button_option(self):
        M5.Lcd.drawImage(res.ETHERNET_DEFAULT_IMG, 6, 22)
        self._ip_label.set_text(self.ip_tmp)
        self._mask_label.set_text(self.mask_tmp)
        self._server_label.set_text(self.server_tmp)
        self._submit_button.set_src(res.SUBMIT_SELECT_BUTTON_IMG)

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        self.ip = self._net_if.local_ip()
        self.mask = self.nvs.get_str("netmask")
        self.server = self.nvs.get_str("server")
        self.ip_tmp = self.ip
        self.mask_tmp = self.mask
        self.server_tmp = self.server

    def set_data(self):
        is_save = False
        if self.ip != self.ip_tmp:
            self.ip = self.ip_tmp
            self.nvs.set_str("ssid0", self.ip)
            print("set new ip: ", self.ip)
            is_save = True
        if self.mask != self.mask_tmp:
            self.mask = self.mask_tmp
            self.nvs.set_str("mask0", self.mask)
            print("set new mask: ", self.mask)
            is_save = True
        if self.server != self.server_tmp:
            self.server = self.server_tmp
            self.nvs.set_str("server", self.server)
            print("set new server: ", self.server)
            is_save = True

        if is_save is True:
            self.nvs.commit()
            self._net_if.wlan.disconnect()
            self._net_if.wlan.active(False)
            self._net_if.wlan.active(True)
            self._net_if.connect_network(self.ip, self.mask)


class BootScreenSetting(app_base.AppBase):
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
        self._options = app_base.generator(self._boot_options)
        while True:
            t = next(self._options)
            if t == self._option:
                break

    def on_view(self):
        self._menu_label = widgets.Label(
            "Boot Screen",
            14,
            27,
            w=155,
            h=22,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )

        self._option_img = widgets.Image(use_sprite=False)
        self._option_img.set_pos(193, 30)
        self._option_img.set_size(30, 14)
        self._option_img.set_src(self._boot_options.get(self._option))

    def on_ready(self):
        M5.Lcd.drawImage(res.CARD_228x32_SELECT_IMG, 6, 22)
        self._menu_label.set_text("Boot Screen")
        self._option_img.set_src(self._boot_options.get(self._option))

    def on_hide(self):
        M5.Lcd.drawImage(res.CARD_228x32_UNSELECT_IMG, 6, 22)
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

    async def _btnb_enter_event_handler(self, fw):
        self._handle_boot_option(fw)

    async def _kb_event_handler(self, event, fw):
        if event.key == 0x0D:  # Enter key
            self._handle_boot_option(fw)
            event.status = True


class GeneralSettingApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._menus = (
            # BrightnessSettingApp(None),
            # BatteryChargeSetting(None),
            BootScreenSetting(None),
        )
        self._menu_selector = app_base.AppSelector(self._menus)
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
        for app in self._menus:
            app.install()
        self._menu_selector.current().resume()

    def stop(self):
        for app in self._menus:
            app.uninstall()
        super().stop()

    async def _btnb_enter_event_handler(self, fw):
        app = self._menu_selector.current()
        await app._btnb_enter_event_handler(fw)

    async def _btnb_back_event_handler(self, fw):
        pass

    async def _btna_next_event_handler(self, fw):
        self._menu_selector.current().pause()
        self._menu_selector.prev().resume()

    async def _btnc_next_event_handler(self, fw):
        self._menu_selector.current().pause()
        self._menu_selector.next().resume()

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


class SettingsApp(app_base.AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._net_if = data
        self._menus = (
            WiFiSettingApp(None, data=self._net_if),
            EthernetSettingApp(None, data=self._net_if),
            GeneralSettingApp(None),
        )
        self._menu_selector = app_base.AppSelector(self._menus)
        self._current_index = 0
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

        # WLAN
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

        # Ethernet
        self._img1 = widgets.Image(use_sprite=False)
        self._img1.set_pos(6, 60)
        self._img1.set_size(228, 32)
        self._img1.set_src(res.CARD_228x32_UNSELECT_IMG)
        self._imgs.append(self._img1)

        self._ico1 = widgets.Image(use_sprite=False)
        self._ico1.set_pos(9, 63)
        self._ico1.set_size(26, 26)
        self._ico1.set_src(res.ETHERNET_ICO_IMG)
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
        self._label1.set_text("Ethernet")
        self._labels.append(self._label1)

        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 63)

        # General
        self._img2 = widgets.Image(use_sprite=False)
        self._img2.set_pos(6, 100)
        self._img2.set_size(228, 32)
        self._img2.set_src(res.CARD_228x32_UNSELECT_IMG)
        self._imgs.append(self._img2)

        self._ico2 = widgets.Image(use_sprite=False)
        self._ico2.set_pos(9, 101)
        self._ico2.set_size(26, 26)
        self._ico2.set_src(res.GENERAL_ICO_IMG)
        self._icos.append(self._ico2)

        self._label2 = widgets.Label(
            "",
            40,
            103,
            w=182,
            h=22,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=res.MontserratMedium18_VLW,
        )
        self._label2.set_text("General")
        self._labels.append(self._label2)

        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 101)

    def on_ready(self):
        pass

    def on_hide(self):
        self._app = None

    def _update_menu_display(self):
        """更新菜单显示状态"""
        current_index = self._menu_selector._id

        # 先将所有选项设置为未选中状态
        for i in range(3):
            self._imgs[i].set_src(res.CARD_228x32_UNSELECT_IMG)
            self._icos[i].refresh()

        # 设置当前选中的选项
        self._imgs[current_index].set_src(res.CARD_228x32_SELECT_IMG)
        self._icos[current_index].refresh()

        # 更新标签文本
        self._labels[0].set_text("WLAN")
        self._labels[1].set_text("Ethernet")
        self._labels[2].set_text("General")

        # 绘制箭头
        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 25)
        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 63)
        M5.Lcd.drawImage(res.CARET_RIGHT, 213, 101)

    async def _btnb_enter_event_handler(self, fw):
        if self._app:
            await self._app._btnb_enter_event_handler(fw)
            return

        self._app = self._menu_selector.current()
        print("current app:", self._app)
        await fw.load(self._app)

    async def _btnb_back_event_handler(self, fw):
        self._menu_selector.index(0)
        self._app = None

    async def _btna_next_event_handler(self, fw):
        if self._app:
            await self._app._btna_next_event_handler(fw)
            return

        self._menu_selector.prev()
        self._update_menu_display()

    async def _btnc_next_event_handler(self, fw):
        if self._app:
            await self._app._btnc_next_event_handler(fw)
            return

        self._menu_selector.next()
        self._update_menu_display()

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
            self._menu_selector.next()
            self._update_menu_display()
            event.status = True
        elif event.key == 181:  # up key
            self._menu_selector.prev()
            self._update_menu_display()
            event.status = True

    async def _btna_event_handler(self, fw):
        self._menu_selector.index(0)
        self._app = None
