# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import Startup
import M5
import network
import widgets
import os
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

CHARGE_ICON = "/system/nesso-n1/CHG.jpg"
NO_CHARGE_ICON = "/system/nesso-n1/noCHG.jpg"
CLOUD_ICON = "/system/nesso-n1/1a.jpg"
USB_ICON = "/system/nesso-n1/1b.jpg"
APPLIST_ICON = "/system/nesso-n1/1c.jpg"
LORACHAT_ICON = "/system/nesso-n1/1d.jpg"
SETUP_ICON = "/system/nesso-n1/1e.jpg"
USB_IMG = "/system/nesso-n1/usb.jpg"
APPLIST_IMG = "/system/nesso-n1/APPLIST.jpg"
CLOUD_IMG = "/system/nesso-n1/a11.jpg"
NG_IMG = "/system/nesso-n1/ng.jpg"
WIFI_OK_IMG = "/system/nesso-n1/wifi_ok.jpg"
SERVER_OK_IMG = "/system/nesso-n1/server_ok.jpg"
PLACEHOLDER_IMG = "/system/nesso-n1/placeholder.jpg"
STATE_WIFI_NO_SET_IMG = "/system/nesso-n1/wifiNeverSet.jpg"
STATE_WIFI_NG_IMG = "/system/nesso-n1/wifiNG.jpg"
STATE_WIFI_OK_IMG = "/system/nesso-n1/wifiOKServerNG.jpg"
STATE_SERVER_OK_IMG = "/system/nesso-n1/wifiOKServerOK.jpg"


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
            font=M5.Lcd.FONTS.DejaVu12,
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


class RunApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_ready(self):
        M5.Lcd.clear()
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt


class ListApp(AppBase):
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
            font=M5.Lcd.FONTS.DejaVu12,
        )
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)

        self._labels = []
        self._label0 = None
        self._label1 = None
        self._label2 = None
        self._lebals = []
        self._lebal0 = None
        self._lebal1 = None
        self._lebal2 = None

        self._files = []
        for file in os.listdir("apps"):
            if file.endswith(".py"):
                self._files.append(file)
        self._files_number = len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def on_view(self):
        self._bg_img.set_src(APPLIST_IMG)
        if self._label0 is None:
            self._label0 = widgets.Label(
                "",
                25,
                108,
                w=85,
                h=22,
                fg_color=0xFFFFFF,
                bg_color=0x333333,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label0.set_long_mode(widgets.Label.LONG_DOT)
        if self._label1 is None:
            self._label1 = widgets.Label(
                "",
                25,
                108 + 22 + 5,
                w=85,
                h=22,
                fg_color=0x999999,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label1.set_long_mode(widgets.Label.LONG_DOT)
        if self._label2 is None:
            self._label2 = widgets.Label(
                "",
                25,
                108 + 22 + 5 + 22 + 5,
                w=85,
                h=22,
                fg_color=0x4D4D4D,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label2.set_long_mode(widgets.Label.LONG_DOT)

        if len(self._labels) != 3:
            self._labels.clear()
            self._labels.append(self._label0)
            self._labels.append(self._label1)
            self._labels.append(self._label2)

        if self._lebal0 is None:
            self._lebal0 = widgets.Label(
                "",
                25,
                108 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x999999,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal0.set_long_mode(widgets.Label.LONG_DOT)

        if self._lebal1 is None:
            self._lebal1 = widgets.Label(
                "",
                25,
                108 - 22 - 5 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x4D4D4D,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal1.set_long_mode(widgets.Label.LONG_DOT)

        if self._lebal2 is None:
            self._lebal2 = widgets.Label(
                "",
                25,
                108 - 22 - 5 - 22 - 5 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x333333,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal2.set_long_mode(widgets.Label.LONG_DOT)

        if len(self._lebals) != 3:
            self._lebals.clear()
            self._lebals.append(self._lebal0)
            self._lebals.append(self._lebal1)
            self._lebals.append(self._lebal2)

        for label, file in zip(self._labels, self._files):
            # print("file:", file)
            file and label and label.set_text(file)

    async def on_run(self):
        while True:
            # battery
            self._battery_label.set_text(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._battery_label, self._labels, self._files, self._lebals

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        M5.Lcd.clear()
        execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")
        self._file_pos += 1

        if self._file_pos >= len(self._files):
            self._file_pos = 0

        for label in self._labels:
            label.set_text("")

        for label, file in zip(self._labels, self._files[self._file_pos :]):
            file and label and label.set_text(file)

        for label in self._lebals:
            label.set_text("")

        files = self._files[: self._file_pos]
        files.reverse()

        for label, file in zip(self._lebals, files):
            file and label and label.set_text(file)


class LoRaChatApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_view(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.drawImage(PLACEHOLDER_IMG, 0, 0, 135, 240)

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


class SetupApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_view(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.drawImage(PLACEHOLDER_IMG, 0, 0, 135, 240)

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


class CloudApp(AppBase):
    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._user_id = None
        self._server = None
        self._wifi_status = False
        self._cloud_status = False

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
        self._net_status_img.set_y(2)
        self._net_status_img.set_size(34, 24)
        self._net_status_img.set_src(NG_IMG)

        self._server_status_img = widgets.Image(use_sprite=False)
        self._server_status_img.set_x(98)
        self._server_status_img.set_y(30)
        self._server_status_img.set_size(34, 24)
        self._server_status_img.set_src(NG_IMG)

        M5.Lcd.fillRect(3, 164, 129, 46, 0xF3F3F3)

    def on_view(self):
        self._net_status_img.set_src(WIFI_OK_IMG if self._get_wifi_status() else NG_IMG)
        self._server_status_img.set_src(SERVER_OK_IMG if self._get_cloud_status() else NG_IMG)

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
            APPLIST_ICON,
            LORACHAT_ICON,
            SETUP_ICON,
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
            font=M5.Lcd.FONTS.DejaVu18,
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
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._version_label.set_text(esp32.firmware_info()[3])

        self.nvs = esp32.NVS("uiflow")
        self._state_img = widgets.Image(use_sprite=False)
        self._state_img.set_x(6)
        self._state_img.set_y(6)
        self._state_img.set_size(16, 16)
        self._state_img.set_src(self._get_state_img())

    def _get_state_img(self) -> str:
        if self.nvs.get_str("ssid0") == "":
            return STATE_WIFI_NO_SET_IMG
        if not self._cloud_app._get_wifi_status():
            return STATE_WIFI_NG_IMG
        if not self._cloud_app._get_cloud_status():
            return STATE_WIFI_OK_IMG
        return STATE_SERVER_OK_IMG

    async def on_run(self):
        last_battery = -1
        last_charging = False
        last_state_img = ""
        while True:
            # connection status
            if last_state_img != self._get_state_img():
                last_state_img = self._get_state_img()
                self._state_img.set_src(last_state_img)

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
        self._state_img.set_src(self._get_state_img())


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
            if M5.BtnA.wasSingleClicked():
                M5.Speaker.tone(4000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_enter_event_handler"):
                    await app._keycode_enter_event_handler(self)
            if M5.BtnA.wasDoubleClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_back_event_handler"):
                    await app._keycode_back_event_handler(self)
            if M5.BtnB.wasSingleClicked():
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


class NessoN1_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wifi.connect_network(ssid, pswd)
        M5.Speaker.setVolume(255)
        M5.Speaker.tone(4000, 50)

        DEBUG and print("Run startup menu")

        cloud_app = CloudApp((self._wifi, ssid))
        usb_app = UsbApp()
        list_app = ListApp()
        lorachat_app = LoRaChatApp()
        setup_app = SetupApp()
        launcher = LauncherApp(data=cloud_app)

        fw = Framework()
        fw.install_launcher(launcher)
        fw.install(launcher)
        fw.install(cloud_app)
        fw.install(usb_app)
        fw.install(list_app)
        fw.install(lorachat_app)
        fw.install(setup_app)
        fw.start()
