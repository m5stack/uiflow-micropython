from ..app import AppBase, generator, AppSelector
import M5
from M5 import Widgets
from widgets.image import Image
from widgets.label import Label
import esp32
from common.font import MontserratMedium16

class WiFiSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self._lcd = icos

    def on_launch(self):
        self.get_data()

    def on_view(self):
        origin_x = 4
        origin_y = 4

        self._bg_img = Image(use_sprite=False, parent=self._lcd)
        self._bg_img.set_pos(origin_x, origin_y)
        self._bg_img.set_size(312, 108)
        self._bg_img.set_src("/system/fire/SettingWifi.png")

        self._ssid_label = Label(
            "ssid",
            origin_x + 98,
            origin_y + 12,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
            parent=self._lcd
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
            font=MontserratMedium16.FONT,
            parent=self._lcd
        )
        self._pwd_label.setLongMode(Label.LONG_DOT)
        self._pwd_label.setText('*' * 20)

        self._server_label = Label(
            "server",
            origin_x + 98,
            origin_y + 12 + 35 + 34,
            w=144,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
            parent=self._lcd
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
    64: "/system/fire/screen25.png",
    128: "/system/fire/screen50.png",
    192: "/system/fire/screen75.png",
    255: "/system/fire/screen100.png",
}


class BrightnessSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos

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
        self._origin_y = 4 + 108 + 4

        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img = Image(use_sprite=False, parent=self._lcd)
        self._select_img.set_pos(self._origin_x + 0, self._origin_y + 6)
        self._select_img.set_size(72, 32)
        self._select_img.set_src("/system/fire/settingSelect.png")

        self._brightness_img = Image(use_sprite=False, parent=self._lcd)
        self._brightness_img.set_pos(self._origin_x + 6, self._origin_y + 0)
        self._brightness_img.set_size(60, 44)
        self._brightness_img.set_src(_brightness_options.get(self._brightness))

    def on_ready(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src("/system/fire/settingSelect.png")
        self._brightness_img._draw(False)

    def on_hide(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src("/system/fire/settingUnselect.png")
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
    1: "/system/fire/boot_Yes.png",
    2: "/system/fire/boot_No.png",
}


class BootScreenSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self._lcd = icos

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
        self._origin_y = 4 + 108 + 4

        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img = Image(use_sprite=False, parent=self._lcd)
        self._select_img.set_pos(self._origin_x + 0, self._origin_y + 6)
        self._select_img.set_size(72, 32)
        self._select_img.set_src("/system/fire/settingSelect.png")

        self._boot_option_img = Image(use_sprite=False, parent=self._lcd)
        self._boot_option_img.set_pos(self._origin_x + 6, self._origin_y + 0)
        self._boot_option_img.set_size(60, 44)
        self._boot_option_img.set_src(_boot_options.get(self._boot_option))

    def on_ready(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src("/system/fire/settingSelect.png")
        self._boot_option_img._draw(True)

    def on_hide(self):
        self._lcd.fillRect(self._origin_x, self._origin_y, 72, 44, 0x000000)
        self._select_img.set_src("/system/fire/settingUnselect.png")
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
        self._lcd = icos
        self._wlan_app = WiFiSetting(self._lcd, data=data)
        self._menus = (
            BrightnessSetting(self._lcd),
            BootScreenSetting(self._lcd),
        )
        self._menu_selector = AppSelector(self._menus)

    def on_install(self):
        M5.Lcd.drawImage("/system/fire/setting_unselected.png", 5 + 62 * 0, 0)

    def on_launch(self):
        pass

    def on_view(self):
        self._origin_x = 0
        self._origin_y = 56

        M5.Lcd.drawImage("/system/fire/setting_selected.png", 5 + 62 * 0, 0)

        self._lcd.clear()
        self._lcd.fillRect(4 + 72 + 8 + 72 + 8, 4 + 108 + 4, 72, 44, 0x404040)
        self._lcd.fillRect(4 + 72 + 8 + 72 + 8 + 72 + 8, 4 + 108 + 4, 72, 44, 0x404040)
        self._lcd.drawImage("/system/fire/bar1.png", 0, 220 - 56)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage("/system/fire/setting_unselected.png", 5 + 62 * 0, 0)

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
