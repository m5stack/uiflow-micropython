from ..app import AppBase, generator, AppSelector
import M5
from M5 import Widgets
from widgets.image import Image
from widgets.label import Label
import esp32


from ..res import (
    SETTING_WIFI_IMG,
    SCREEN25_IMG,
    SCREEN50_IMG,
    SCREEN75_IMG,
    SCREEN100_IMG,
    SETTING_SELECT_IMG,
    SETTING_UNSELECT_IMG,
    BOOT_YES_IMG,
    BOOT_NO_IMG,
    SETTING_UNSELECTED_IMG,
    SETTING_SELECTED_IMG,
    BAR1_IMG,
)


class WiFiSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_launch(self):
        self.get_data()

    def on_view(self):
        origin_x = 4
        origin_y = 56 + 4

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(origin_x, origin_y)
        self._bg_img.set_size(312, 108)
        self._bg_img.set_src(SETTING_WIFI_IMG)

        self._ssid_label = Label(
            "ssid",
            origin_x + 98,
            origin_y + 12,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu12,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)
        self._ssid_label.setText(self.ssid)

        self._pwd_label = Label(
            "pwd",
            origin_x + 98,
            origin_y + 12 + 35,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu12,
        )
        self._pwd_label.setLongMode(Label.LONG_DOT)
        self._pwd_label.setText("*" * 20)

        self._server_label = Label(
            "server",
            origin_x + 98,
            origin_y + 12 + 35 + 34,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu12,
        )
        self._server_label.setLongMode(Label.LONG_DOT)
        self._server_label.setText(self.server)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass

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
            print("set new ssid: ", self.ssid)
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
        self._origin_x = 4
        self._origin_y = 56 + 4 + 108 + 4

        M5.Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img = Image(use_sprite=False)
        self._select_img.set_pos(self._origin_x + 0, self._origin_y + 6)
        self._select_img.set_size(72, 32)
        self._select_img.set_src(SETTING_SELECT_IMG)

        self._brightness_img = Image(use_sprite=False)
        self._brightness_img.set_pos(self._origin_x + 6, self._origin_y + 0)
        self._brightness_img.set_size(60, 44)
        self._brightness_img.set_src(_brightness_options.get(self._brightness))

    def on_ready(self):
        M5.Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src(SETTING_SELECT_IMG)
        self._brightness_img._draw(False)

    def on_hide(self):
        M5.Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        # self._select_img.set_src(SETTING_UNSELECT_IMG)
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
    1: BOOT_YES_IMG,
    2: BOOT_NO_IMG,
}


class BootScreenSetting(AppBase):
    def __init__(self, icos: dict) -> None:
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
        self._origin_x = 4 + 72 + 8
        self._origin_y = 56 + 4 + 108 + 4

        M5.Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img = Image(use_sprite=False)
        self._select_img.set_pos(self._origin_x + 0, self._origin_y + 6)
        self._select_img.set_size(72, 32)
        self._select_img.set_src(SETTING_SELECT_IMG)

        self._boot_option_img = Image(use_sprite=False)
        self._boot_option_img.set_pos(self._origin_x + 6, self._origin_y + 0)
        self._boot_option_img.set_size(60, 44)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))

    def on_ready(self):
        M5.Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src(SETTING_SELECT_IMG)
        self._boot_option_img._draw(True)

    def on_hide(self):
        M5.Lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        # self._select_img.set_src(SETTING_UNSELECT_IMG)
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


class SettingsApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._wlan_app = WiFiSetting(None, data=data)
        self._menus = (
            BrightnessSetting(None),
            BootScreenSetting(None),
        )
        self._menu_selector = AppSelector(self._menus)

    def on_install(self):
        M5.Lcd.drawImage(SETTING_UNSELECTED_IMG, 5 + 62 * 0, 0)

    def on_launch(self):
        pass

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 56

        M5.Lcd.drawImage(SETTING_SELECTED_IMG, 5 + 62 * 0, 0)
        M5.Lcd.fillRect(self._origin_x, self._origin_y, 320, 184, 0x000000)
        M5.Lcd.fillRect(4 + 72 + 8 + 72 + 8, self._origin_y + 4 + 108 + 4, 72, 44, 0x404040)
        M5.Lcd.fillRect(
            4 + 72 + 8 + 72 + 8 + 72 + 8, self._origin_y + 4 + 108 + 4, 72, 44, 0x404040
        )
        M5.Lcd.drawImage(BAR1_IMG, 0, 220)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage(SETTING_UNSELECTED_IMG, 5 + 62 * 0, 0)

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        await self._menus[0]._btnb_event_handler(fw)
        self._menu_selector.current().pause()
        self._menu_selector.next().resume()

    async def _btnc_event_handler(self, fw):
        await self._menu_selector.current()._btnc_event_handler(fw)

    def start(self):
        super().start()
        self._wlan_app.start()
        for menu in self._menus:
            menu.install()
        self._menus[0].start()

    def stop(self):
        super().stop()
        self._wlan_app.stop()
        for menu in self._menus:
            menu.stop()
