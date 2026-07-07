# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import Startup, print_access_info
import M5
import network
import widgets
import sys
import gc
import asyncio
import esp32

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = False

CHARGE_ICON = "/flash/res/stickcplus/CHG.jpg"
NO_CHARGE_ICON = "/flash/res/stickcplus/noCHG.jpg"
CLOUD_ICON = "/flash/res/stickcplus/1a.jpg"
USB_ICON = "/flash/res/stickcplus/1b.jpg"
USB_IMG = "/flash/res/stickcplus/usb.jpg"
CLOUD_IMG = "/flash/res/stickcplus/a11.jpg"
NG_IMG = "/flash/res/stickcplus/ng.jpg"
WIFI_OK_IMG = "/flash/res/stickcplus/wifi_ok.jpg"
SERVER_OK_IMG = "/flash/res/stickcplus/server_ok.jpg"
STATE_WIFI_NO_SET_IMG = "/flash/res/stickcplus/wifiNeverSet.jpg"
STATE_WIFI_NG_IMG = "/flash/res/stickcplus/wifiNG.jpg"
STATE_WIFI_OK_IMG = "/flash/res/stickcplus/wifiOKServerNG.jpg"
STATE_SERVER_OK_IMG = "/flash/res/stickcplus/wifiOKServerOK.jpg"


class AppBase:
    def __init__(self) -> None:
        self._task = None

    def on_install(self):
        pass

    def on_launch(self):
        pass

    def on_view(self):
        pass

    def on_ready(self):
        self._task = asyncio.create_task(self.on_run())

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        pass

    def on_uninstall(self):
        pass

    def install(self):
        self.on_install()

    def start(self):
        self.on_launch()
        self.on_view()
        self.on_ready()

    def pause(self):
        self.on_hide()

    def resume(self):
        self.on_ready()

    def stop(self):
        self.on_hide()
        self.on_exit()

    def uninstall(self):
        self.on_uninstall()


class AppSelector:
    def __init__(self, apps: list) -> None:
        self._apps = apps
        self._id = 0

    def prev(self):
        self._id = (self._id - 1) % len(self._apps)
        return self._apps[self._id]

    def next(self):
        self._id = (self._id + 1) % len(self._apps)
        return self._apps[self._id]

    def current(self):
        return self._apps[self._id]

    def select(self, app):
        self._id = self._apps.index(app)

    def index(self, id):
        self._id = id % len(self._apps)
        return self._apps[self._id]


class UsbApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        self._battery_label = widgets.Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=widgets.Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.Montserrat14,
        )

        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)

    def on_view(self):
        self._bg_img.set_src(USB_IMG)

    async def on_run(self):
        while True:
            # battery
            self._battery_label.set_text(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._battery_label

    async def _keycode_enter_event_handler(self, fw: "Framework") -> None:
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework") -> None:
        DEBUG and print("_keycode_dpad_down_event_handler")


class CloudApp(AppBase):
    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._user_id = None
        self._server = None
        self._wifi_status = False
        self._cloud_status = False
        self._nick_name = ""
        self._access_code = ""

    def _get_wifi_status(self) -> bool:
        return self._wifi.connect_status() == network.STAT_GOT_IP

    def _get_cloud_status(self) -> bool:
        if self._get_wifi_status() and _HAS_SERVER:
            return M5Things.status() == 2
        else:
            return False

    def on_launch(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self._bg_img.set_src(CLOUD_IMG)

        self._net_status_img = widgets.Image(use_sprite=False)
        self._net_status_img.set_x(98)
        self._net_status_img.set_y(27)
        self._net_status_img.set_size(34, 24)
        self._net_status_img.set_src(NG_IMG)

        self._server_status_img = widgets.Image(use_sprite=False)
        self._server_status_img.set_x(98)
        self._server_status_img.set_y(55)
        self._server_status_img.set_size(34, 24)
        self._server_status_img.set_src(NG_IMG)

        self._access_code_label = widgets.Label(
            self._access_code,
            67,
            99,
            w=103,
            h=29,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCBDFE0,
            font=M5.Lcd.FONTS.Montserrat24,
        )

        self._nick_name_label = widgets.Label(
            self._nick_name,
            67,
            149,
            w=129,
            h=29,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCBDFE0,
            font=M5.Lcd.FONTS.Montserrat24,
        )
        self._nick_name_label.set_long_mode(self._nick_name_label.LONG_DOT)

    def on_view(self):
        self._net_status_img.set_src(WIFI_OK_IMG if self._get_wifi_status() else NG_IMG)
        self._server_status_img.set_src(SERVER_OK_IMG if self._get_cloud_status() else NG_IMG)
        self._access_code_label.set_text(self._access_code)
        self._nick_name_label.set_text(self._nick_name)
        print_access_info(self._nick_name, self._access_code)

    async def on_run(self):
        while True:
            t = self._get_wifi_status()
            if t is not self._wifi_status:
                self._wifi_status = t
                self._net_status_img.set_src(WIFI_OK_IMG if t else NG_IMG)

            t = self._get_cloud_status()
            if t is not self._cloud_status:
                self._cloud_status = t
                self._server_status_img.set_src(SERVER_OK_IMG if t else NG_IMG)

            if _HAS_SERVER:
                t = M5Things.nick_name()
                if t != self._nick_name:
                    self._nick_name = t
                    self._nick_name_label.set_text(t)

                t = M5Things.accesscode()
                if t != self._access_code:
                    self._access_code = t
                    self._access_code_label.set_text(t)

                print_access_info(self._nick_name, self._access_code)

            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._net_status_img, self._server_status_img

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")


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


class LauncherApp(AppBase):
    def __init__(self, data=None) -> None:
        self._cloud_app = data
        self._icons = (
            CLOUD_ICON,
            USB_ICON,
        )

    def on_launch(self):
        self._icon_selector = _charge_ico(self._icons)
        self._img_src = next(self._icon_selector)
        self._id = 0

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self._bg_img.set_src(self._img_src)

        self._chg_img = widgets.Image(use_sprite=False)
        self._chg_img.set_x(59)
        self._chg_img.set_y(3)
        self._chg_img.set_size(16, 22)
        if M5.Power.isCharging():
            self._chg_img.set_src(CHARGE_ICON)
        else:
            self._chg_img.set_src(NO_CHARGE_ICON)

        self._battery_label = widgets.Label(
            str(None),
            132,
            5,
            w=47,
            h=21,
            font_align=widgets.Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCCCCCC,
            font=M5.Lcd.FONTS.Montserrat18,
        )

        self._version_label = widgets.Label(
            str(esp32.firmware_info()[3]),
            67,
            152,
            w=135,
            h=22,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0x67C94D,
            font=M5.Lcd.FONTS.Montserrat18,
        )
        self._version_label.set_text(esp32.firmware_info()[3])

    async def on_run(self):
        last_battery = -1
        last_charging = False
        while True:
            # charging status
            if last_charging != M5.Power.isCharging():
                last_charging = M5.Power.isCharging()
                self._chg_img.set_src(CHARGE_ICON if last_charging else NO_CHARGE_ICON)

            # battery level
            if last_battery != M5.Power.getBatteryLevel():
                last_battery = M5.Power.getBatteryLevel()
                self._battery_label.set_text(str(last_battery) + "%")

            await asyncio.sleep_ms(200)

    def on_exit(self):
        del self._bg_img, self._icon_selector

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        app = fw._app_selector.index(self._id + 1)
        app.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")
        self._id = self._id + 1 if self._id + 1 < len(self._icons) else 0
        self._img_src = next(self._icon_selector)
        self._bg_img.set_src(self._img_src)
        self._chg_img.set_src(CHARGE_ICON if M5.Power.isCharging() else NO_CHARGE_ICON)
        self._battery_label.set_text(str(M5.Power.getBatteryLevel()) + "%")
        self._version_label.set_text(esp32.firmware_info()[3])


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = AppSelector(self._apps)
        self._launcher = None

    def install_launcher(self, launcher: AppBase):
        self._launcher = launcher

    def install(self, app: AppBase):
        app.install()
        self._apps.append(app)

    def start(self):
        # asyncio.create_task(self.gc_task())
        asyncio.run(self.run())

    async def unload(self, app: AppBase):
        # app = self._apps.pop()
        app.stop()

    async def load(self, app: AppBase):
        app.start()

    async def reload(self, app: AppBase):
        app.stop()
        app.start()

    async def run(self):
        if self._launcher:
            self._app_selector.select(self._launcher)
            self._launcher.start()

        # asyncio.create_task(self.gc_task())
        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                M5.Speaker.tone(4000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_enter_event_handler"):
                    await app._keycode_enter_event_handler(self)
            if M5.BtnPWR.wasClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_back_event_handler"):
                    await app._keycode_back_event_handler(self)
            if M5.BtnB.wasClicked():
                M5.Speaker.tone(6000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_dpad_down_event_handler"):
                    await app._keycode_dpad_down_event_handler(self)

            await asyncio.sleep_ms(100)

    async def gc_task(self):
        while True:
            gc.collect()
            DEBUG and print("heap RAM free:", gc.mem_free())
            DEBUG and print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)


class StickCPlus_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self._wifi.connect_network(
            ssid, pswd, protocol=protocol, ip=ip, netmask=netmask, gateway=gateway, dns=dns
        )
        M5.Power.setExtOutput(False)
        M5.Speaker.setVolume(100)
        M5.Speaker.tone(4000, 50)

        DEBUG and print("Run StickC Plus startup menu")

        cloud_app = CloudApp((self._wifi, ssid))
        usb_app = UsbApp()
        launcher = LauncherApp(data=cloud_app)

        fw = Framework()
        fw.install_launcher(launcher)
        fw.install(launcher)
        fw.install(cloud_app)
        fw.install(usb_app)
        fw.start()
