from ..app import AppBase, AppSelector
from M5 import Lcd, Widgets

# from widgets.image import Image
from widgets.label import Label
import esp32
from ..res import (
    SETTING_WIFI_IMG,
    SCREEN25_IMG,
    SCREEN50_IMG,
    SCREEN75_IMG,
    SCREEN100_IMG,
    SETTING_SELECT_IMG,
    # SETTING_UNSELECT_IMG,
    BOOT_YES_IMG,
    BOOT_NO_IMG,
    SETTING_UNSELECTED_IMG,
    SETTING_SELECTED_IMG,
    BAR1_IMG,
)
from unit import KeyCode
from .app_list import Rectangle
import boot_option


class WiFiSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wifi = data
        super().__init__()

    def on_launch(self):
        self.get_data()
        self._option = 0
        self.focus = True

    def on_view(self):
        self._origin_x = 4
        self._origin_y = 56 + 4

        Lcd.drawImage(SETTING_WIFI_IMG, self._origin_x, self._origin_y)

        self._rect0 = Rectangle(
            self._origin_x + 96, self._origin_y + 7, 144, 26, 0xFEFEFE, 0xFEFEFE
        )

        self._ssid_label = Label(
            "ssid",
            self._origin_x + 98,
            self._origin_y + 12,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu12,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)
        self._ssid_label.setText(self.ssid)

        self._psk_label = Label(
            "pwd",
            self._origin_x + 98,
            self._origin_y + 12 + 35,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu12,
        )
        self._psk_label.setLongMode(Label.LONG_DOT)
        if len(self.psk):
            self._psk_label.setText("*" * 20)
        else:
            self._psk_label.setText("")

        self._server_label = Label(
            "server",
            self._origin_x + 98,
            self._origin_y + 12 + 35 + 34,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu12,
        )
        self._server_label.setLongMode(Label.LONG_DOT)
        self._server_label.setText(self.server)

        # self._option_views = AppSelector(
        #     (
        #         (0, self._select_ssid_option),
        #         (1, self._select_psk_option),
        #         (2, self._select_server_option),
        #     )
        # )

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        del (
            self._rect0,
            self._ssid_label,
            self._psk_label,
            self._server_label,
            # self._option_views,
            self._origin_x,
            self._origin_y,
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

    # async def _kb_event_handler(self, event, fw):
    #     if event.key == KeyCode.KEYCODE_ENTER:
    #         event.status = True
    #         self.focus = True
    #         self._option, view_fn = self._option_views.next()
    #         view_fn()
    #         self.set_data()

    #     if self.focus is False:
    #         return

    #     if event.key == KeyCode.KEYCODE_ESC:
    #         self.ssid_tmp = self.ssid
    #         self.psk_tmp = self.psk
    #         self.server_tmp = self.server
    #         self._select_default_option()
    #         self.focus = False
    #         event.status = True
    #         self.set_data()

    #     if event.key == KeyCode.KEYCODE_BACKSPACE and self._option in (0, 1, 2):
    #         if self._option == 0:
    #             self.ssid_tmp = self.ssid_tmp[:-1]
    #             self._ssid_label.setText(self.ssid_tmp)
    #         elif self._option == 1:
    #             if self.psk_tmp == self.psk and len(self.psk):
    #                 self.psk_tmp = ""
    #             else:
    #                 self.psk_tmp = self.psk_tmp[:-1]
    #             self._psk_label.setText(self.psk_tmp)
    #         elif self._option == 2:
    #             self.server_tmp = self.server_tmp[:-1]
    #             self._server_label.setText(self.server_tmp)
    #         event.status = True
    #     elif event.key >= 0x20 and event.key <= 126:
    #         if self._option == 0:
    #             self.ssid_tmp += chr(event.key)
    #             self._ssid_label.setText(self.ssid_tmp)
    #         elif self._option == 1:
    #             if self.psk_tmp == self.psk and len(self.psk):
    #                 self.psk_tmp = ""
    #             else:
    #                 self.psk_tmp += chr(event.key)
    #             self._psk_label.setText(self.psk_tmp)
    #         elif self._option == 2:
    #             self.server_tmp += chr(event.key)
    #             self._server_label.setText(self.server_tmp)
    #         event.status = True

    # def _select_default_option(self):
    #     Lcd.drawImage(SETTING_WIFI_IMG, self._origin_x, self._origin_y)
    #     self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._psk_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._server_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._ssid_label.setText(self.ssid_tmp)
    #     if len(self.psk_tmp) is 0:
    #         self._psk_label.setText("")
    #     else:
    #         self._psk_label.setText("*" * 20)
    #     self._server_label.setText(self.server_tmp)

    # def _select_ssid_option(self):
    #     self._rect0.set_color(0xFEFEFE, 0xFEFEFE)
    #     self._rect0.set_pos(self._origin_x + 98, self._origin_y + 7)
    #     self._rect0.set_color(0xDCDDDD, 0xDCDDDD)
    #     self._ssid_label.setTextColor(0x000000, 0xDCDDDD)
    #     self._psk_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._server_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._ssid_label.setText(self.ssid_tmp)
    #     if len(self.psk_tmp) is 0:
    #         self._psk_label.setText("")
    #     else:
    #         self._psk_label.setText("*" * 20)
    #     self._server_label.setText(self.server_tmp)

    # def _select_psk_option(self):
    #     self._rect0.set_color(0xFEFEFE, 0xFEFEFE)
    #     self._rect0.set_pos(self._origin_x + 98, self._origin_y + 7 + 36)
    #     self._rect0.set_color(0xDCDDDD, 0xDCDDDD)
    #     self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._psk_label.setTextColor(0x000000, 0xDCDDDD)
    #     self._server_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._ssid_label.setText(self.ssid_tmp)
    #     if len(self.psk_tmp) is 0:
    #         self._psk_label.setText("")
    #     else:
    #         self._psk_label.setText("*" * 20)
    #     self._server_label.setText(self.server_tmp)

    # def _select_server_option(self):
    #     self._rect0.set_color(0xFEFEFE, 0xFEFEFE)
    #     self._rect0.set_pos(self._origin_x + 98, self._origin_y + 7 + 36 + 36)
    #     self._rect0.set_color(0xDCDDDD, 0xDCDDDD)
    #     self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._psk_label.setTextColor(0x000000, 0xFEFEFE)
    #     self._server_label.setTextColor(0x000000, 0xDCDDDD)
    #     self._ssid_label.setText(self.ssid_tmp)
    #     if len(self.psk_tmp) is 0:
    #         self._psk_label.setText("")
    #     else:
    #         self._psk_label.setText("*" * 20)
    #     self._server_label.setText(self.server_tmp)

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        self.ssid = self.nvs.get_str("ssid0")
        self.psk = self.nvs.get_str("pswd0")
        self.server = self.nvs.get_str("server")
        self.ssid_tmp = self.ssid
        self.psk_tmp = self.psk
        self.server_tmp = self.server

    # def set_data(self):
    #     is_save = False
    #     if self.ssid != self.ssid_tmp:
    #         self.ssid = self.ssid_tmp
    #         self.nvs.set_str("ssid0", self.ssid)
    #         print("set new ssid: ", self.ssid)
    #         is_save = True
    #     if self.psk != self.psk_tmp:
    #         self.psk = self.psk_tmp
    #         self.nvs.set_str("pswd0", self.psk)
    #         print("set new psk: ", self.psk)
    #         is_save = True
    #     if self.server != self.server_tmp:
    #         self.server = self.server_tmp
    #         self.nvs.set_str("server", self.server)
    #         print("set new server: ", self.server)
    #         is_save = True

    #     if is_save is True:
    #         self.nvs.commit()
    #         self._wifi.wlan.disconnect()
    #         self._wifi.wlan.active(False)
    #         self._wifi.wlan.active(True)
    #         self._wifi.connect_network(self.ssid, self.psk)


_brightness_options = {
    64: SCREEN25_IMG,
    128: SCREEN50_IMG,
    192: SCREEN75_IMG,
    255: SCREEN100_IMG,
}


# class BrightnessSetting(AppBase):
#     def __init__(self, icos: dict) -> None:
#         super().__init__()

#     def on_install(self):
#         self.on_launch()
#         self.on_view()
#         self.on_hide()

#     def on_launch(self):
#         self._brightness = Lcd.getBrightness()
#         self._brightness = self.approximate(self._brightness)
#         self._options = AppSelector(list(_brightness_options))
#         self._options.select(self._brightness)

#     def on_view(self):
#         self._origin_x = 4
#         self._origin_y = 56 + 4 + 108 + 4

#         Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
#         Lcd.drawImage(SETTING_SELECT_IMG, self._origin_x + 0, self._origin_y + 6)
#         Lcd.drawImage(
#             _brightness_options.get(self._brightness), self._origin_x + 6, self._origin_y + 0
#         )

#     def on_ready(self):
#         Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
#         Lcd.drawImage(SETTING_SELECT_IMG, self._origin_x + 0, self._origin_y + 6)
#         Lcd.drawImage(
#             _brightness_options.get(self._brightness), self._origin_x + 6, self._origin_y + 0
#         )

#     def on_hide(self):
#         Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
#         Lcd.drawImage(
#             _brightness_options.get(self._brightness), self._origin_x + 6, self._origin_y + 0
#         )

#     def on_exit(self):
#         del self._origin_x, self._origin_y
#         del self._brightness, self._options

#     # async def _btna_event_handler(self, fw):
#     #     pass

#     # async def _btnb_event_handler(self, fw):
#     #     pass

#     async def _btnc_event_handler(self, fw):
#         self._brightness = self._options.next()
#         Lcd.setBrightness(self._brightness)
#         Lcd.drawImage(
#             _brightness_options.get(self._brightness), self._origin_x + 6, self._origin_y + 0
#         )

#     @staticmethod
#     def approximate(number):
#         tolerance = 32
#         for v in (64, 128, 192, 255):
#             if number < 64:
#                 return 64
#             if abs(number - v) < tolerance:
#                 return v


_boot_options = {
    1: BOOT_YES_IMG,
    2: BOOT_NO_IMG,
}


# class BootScreenSetting(AppBase):
#     def __init__(self, icos: dict) -> None:
#         super().__init__()

#     def on_install(self):
#         self.on_launch()
#         self.on_view()
#         self.on_hide()

#     def on_launch(self):
#         self._boot_option = boot_option.get_boot_option()
#         self._boot_option = 1 if self._boot_option == 1 else 2
#         self._options = AppSelector(list(_boot_options))
#         self._options.select(self._boot_option)

#     def on_view(self):
#         self._origin_x = 4 + 72 + 8
#         self._origin_y = 56 + 4 + 108 + 4

#         Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
#         Lcd.drawImage(SETTING_SELECT_IMG, self._origin_x + 0, self._origin_y + 6)
#         Lcd.drawImage(_boot_options.get(self._boot_option), self._origin_x + 6, self._origin_y + 0)

#     def on_ready(self):
#         Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
#         Lcd.drawImage(SETTING_SELECT_IMG, self._origin_x + 0, self._origin_y + 6)
#         Lcd.drawImage(_boot_options.get(self._boot_option), self._origin_x + 6, self._origin_y + 0)

#     def on_hide(self):
#         Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
#         Lcd.drawImage(_boot_options.get(self._boot_option), self._origin_x + 6, self._origin_y + 0)

#     def on_exit(self):
#         del self._origin_x, self._origin_y
#         del self._boot_option, self._options

#     # async def _btna_event_handler(self, fw):
#     #     pass

#     # async def _btnb_event_handler(self, fw):
#     #     pass

#     async def _btnc_event_handler(self, fw):
#         self._boot_option = self._options.next()
#         boot_option.set_boot_option(self._boot_option)
#         Lcd.drawImage(_boot_options.get(self._boot_option), self._origin_x + 6, self._origin_y + 0)


class SettingsApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan_app = WiFiSetting(None, data=data)
        # self._menus = (
        #     BrightnessSetting(None),
        #     BootScreenSetting(None),
        # )
        # self._menu_selector = AppSelector(self._menus)

    def on_install(self):
        Lcd.drawImage(SETTING_UNSELECTED_IMG, 5 + 62 * 0, 0)

    def on_launch(self):
        self._brightness = Lcd.getBrightness()
        self._brightness = self.approximate(self._brightness)
        self._brightness_options = AppSelector(list(_brightness_options))
        self._brightness_options.select(self._brightness)

        self._boot_option = boot_option.get_boot_option()
        self._boot_option = 1 if self._boot_option == 1 else 2
        self._boot_options = AppSelector(list(_boot_options))
        self._boot_options.select(self._boot_option)

        self._pos = 0

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 56

        Lcd.drawImage(SETTING_SELECTED_IMG, 5 + 62 * 0, 0)
        Lcd.fillRect(self._origin_x, self._origin_y, 320, 184, 0x000000)
        Lcd.fillRect(4 + 72 + 8 + 72 + 8, self._origin_y + 4 + 108 + 4, 72, 44, 0x404040)
        Lcd.fillRect(4 + 72 + 8 + 72 + 8 + 72 + 8, self._origin_y + 4 + 108 + 4, 72, 44, 0x404040)
        Lcd.drawImage(BAR1_IMG, 0, 220)

        self._origin_x = 4
        self._origin_y = 56 + 4 + 108 + 4

        Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        Lcd.drawImage(SETTING_SELECT_IMG, self._origin_x + 0, self._origin_y + 6)
        Lcd.drawImage(
            _brightness_options.get(self._brightness), self._origin_x + 6, self._origin_y + 0
        )

        self._origin_x = 4 + 72 + 8
        self._origin_y = 56 + 4 + 108 + 4

        Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        # Lcd.drawImage(SETTING_SELECT_IMG, self._origin_x + 0, self._origin_y + 6)
        Lcd.drawImage(_boot_options.get(self._boot_option), self._origin_x + 6, self._origin_y + 0)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        Lcd.drawImage(SETTING_UNSELECTED_IMG, 5 + 62 * 0, 0)

    # async def _kb_event_handler(self, event, fw):
    #     await self._wlan_app._kb_event_handler(event, fw)

    # async def _btna_event_handler(self, fw):
    #     pass

    async def _btnb_event_handler(self, fw):
        # self._menu_selector.current().pause()
        # self._menu_selector.next().resume()
        self._pos += 1
        if self._pos % 2 == 0:
            Lcd.fillRect(4 + 72 + 8, 56 + 4 + 108 + 4, 72, 44, 0x000000)
            Lcd.drawImage(
                _boot_options.get(self._boot_option), 4 + 72 + 8 + 6, 56 + 4 + 108 + 4 + 0
            )
            Lcd.fillRect(4, 56 + 4 + 108 + 4, 72, 44, 0x000000)
            Lcd.drawImage(SETTING_SELECT_IMG, 4 + 0, 56 + 4 + 108 + 4 + 6)
            Lcd.drawImage(_brightness_options.get(self._brightness), 4 + 6, 56 + 4 + 108 + 4 + 0)
        else:
            Lcd.fillRect(4, 56 + 4 + 108 + 4, 72, 44, 0x000000)
            Lcd.drawImage(_brightness_options.get(self._brightness), 4 + 6, 56 + 4 + 108 + 4 + 0)
            Lcd.fillRect(4 + 72 + 8, 56 + 4 + 108 + 4, 72, 44, 0x000000)
            Lcd.drawImage(SETTING_SELECT_IMG, 4 + 72 + 8 + 0, 56 + 4 + 108 + 4 + 6)
            Lcd.drawImage(
                _boot_options.get(self._boot_option), 4 + 72 + 8 + 6, 56 + 4 + 108 + 4 + 0
            )

    async def _btnc_event_handler(self, fw):
        if self._pos % 2 == 0:
            self._brightness = self._brightness_options.next()
            Lcd.setBrightness(self._brightness)
            Lcd.drawImage(_brightness_options.get(self._brightness), 4 + 6, 56 + 4 + 108 + 4 + 0)
        else:
            self._boot_option = self._boot_options.next()
            boot_option.set_boot_option(self._boot_option)
            Lcd.drawImage(
                _boot_options.get(self._boot_option), 4 + 72 + 8 + 6, 56 + 4 + 108 + 4 + 0
            )

    def start(self):
        super().start()
        self._wlan_app.start()
        # for menu in self._menus:
        #     menu.install()
        # self._menus[0].start()

    def stop(self):
        super().stop()
        self._wlan_app.stop()
        # for menu in self._menus:
        #     menu.stop()

    @staticmethod
    def approximate(number):
        tolerance = 32
        for v in (64, 128, 192, 255):
            if number < 64:
                return 64
            if abs(number - v) < tolerance:
                return v
