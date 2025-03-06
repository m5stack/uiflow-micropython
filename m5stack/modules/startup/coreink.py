# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# CoreInk startup script
from startup import Startup
import M5
import network
import widgets
import os
import sys
import gc
import machine
import binascii
import asyncio

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = True

STARTUP_BG_IMG = "/flash/res/coreink/Startup.bmp"
FLOW_BG_IMG = "/flash/res/coreink/Flow.bmp"
CONFIG_BG_IMG = "/flash/res/coreink/Config.bmp"
APPLIST_BG_IMG = "/flash/res/coreink/AppList.bmp"

WIFI_IMG = "/flash/res/coreink/wifi.bmp"
WIFI_ERR_IMG = "/flash/res/coreink/wifi_err.bmp"
SERVER_IMG = "/flash/res/coreink/server.bmp"
SERVER_ERR_IMG = "/flash/res/coreink/server_err.bmp"


class AppBase:
    def __init__(self) -> None:
        self._task = None

    def on_launch(self):
        DEBUG and print("Base Launch")
        pass

    def on_view(self):
        pass

    def on_ready(self):
        self._task = asyncio.create_task(self.on_run())

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(500)

    async def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        pass


class Framework:
    def __init__(self, apps) -> None:
        self._apps = apps
        self._app = None
        self._current_app = 0

    async def unload(self, app: int):
        await self._apps[app].on_hide()

    async def load(self, app: int):
        self._app = self._apps[app]
        self._app.on_launch()
        self._app.on_view()
        self._app.on_ready()

    async def reload(self, app: int):
        await self._apps[app].on_hide()
        self._apps[app].on_ready()

    async def run(self):
        asyncio.create_task(self.load(0))
        # asyncio.create_task(self.gc_task())
        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                asyncio.create_task(self._app._keycode_back_event_handler(self))
            if M5.BtnB.wasClicked():
                asyncio.create_task(self._app._keycode_enter_event_handler(self))
            if M5.BtnC.wasClicked():
                asyncio.create_task(self._app._keycode_dpad_down_event_handler(self))

            if M5.BtnEXT.wasClicked():
                self._current_app = (self._current_app + 1) % len(self._apps)
                DEBUG and print("Switch to %d" % self._current_app)
                await self._app.on_hide()
                self._app.on_exit()
                await self.load(self._current_app)
            await asyncio.sleep_ms(100)

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)


class FlowApp(AppBase):
    def __init__(self, sprite, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._mac = None
        self._user_id = None
        self._cloud_status = 0
        self._sprite = sprite

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).upper()

    def _get_cloud_status(self):
        _cloud_status = {
            network.STAT_IDLE: 0,
            network.STAT_CONNECTING: 0,
            network.STAT_GOT_IP: 1,
            network.STAT_NO_AP_FOUND: 2,
            network.STAT_WRONG_PASSWORD: 2,
            network.STAT_BEACON_TIMEOUT: 2,
            network.STAT_ASSOC_FAIL: 2,
            network.STAT_HANDSHAKE_TIMEOUT: 2,
        }[self._wifi.connect_status()]

        if _cloud_status != 1 or _HAS_SERVER is not True:
            return _cloud_status

        if M5Things.status() == 2:
            _cloud_status = 4
        else:
            _cloud_status = 3
        return _cloud_status

    def _get_user_id(self):
        if _HAS_SERVER:
            return None if len(M5Things.info()[1]) == 0 else M5Things.info()[1]
        else:
            return None

    def _load_data(self):
        self._mac = self._get_mac()
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def _update_data(self):
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def _load_view(self):
        # bg img
        self._bg_img.set_src(FLOW_BG_IMG)

        # ssid
        self._mac_label.set_text_color(0x000000, 0xFFFFFF)
        self._mac_label.set_text(self._mac)

        # user id
        self._user_id_label.set_text(str(self._user_id))

        # server, wifi
        if self._cloud_status == 0 or self._cloud_status == 2:
            self._wifi_img.set_src(WIFI_ERR_IMG)
        else:
            self._wifi_img.set_src(WIFI_IMG)

        if self._cloud_status == 4:
            self._server_img.set_src(SERVER_IMG)
        else:
            self._server_img.set_src(SERVER_ERR_IMG)

        self._sprite.push(0, 0)

    def on_launch(self):
        DEBUG and print("Flow Launch")
        self._mac = self._get_mac()
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def on_view(self):
        self._mac_label = widgets.Label(
            str(None),
            15,
            63,
            w=138,
            h=24,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
            parent=self._sprite,
        )
        self._mac_label.set_long_mode(widgets.Label.LONG_DOT)

        self._user_id_label = widgets.Label(
            str(None),
            15,
            119,
            w=138,
            h=24,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
            parent=self._sprite,
        )
        self._user_id_label.set_long_mode(widgets.Label.LONG_DOT)

        self._bg_img = widgets.Image(
            use_sprite=False,
            parent=self._sprite,
        )
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(200, 200)

        self._wifi_img = widgets.Image(
            use_sprite=False,
            parent=self._sprite,
        )
        self._wifi_img.set_x(4)
        self._wifi_img.set_y(176)
        self._wifi_img.set_size(32, 24)

        self._server_img = widgets.Image(
            use_sprite=False,
            parent=self._sprite,
        )
        self._server_img.set_x(40)
        self._server_img.set_y(176)
        self._server_img.set_size(32, 24)

        self._load_view()

    async def on_run(self):
        while True:
            t = self._get_cloud_status()
            if t is not self._cloud_status:
                self._cloud_status = t
                self._update_data()
                self._load_view()
                await asyncio.sleep_ms(1000)
            else:
                await asyncio.sleep_ms(1000)

    def on_exit(self):
        DEBUG and print("Flow Exit")
        try:
            del self._mac_label, self._user_id_label
        except:
            pass
        del self._bg_img

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        pass

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        pass


class ConfigApp(AppBase):
    def __init__(self, sprite, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._server = None
        self._cloud_status = 0
        self._sprite = sprite

    def _get_server(self):
        import esp32

        nvs = esp32.NVS("uiflow")
        try:
            return nvs.get_str("server")
        finally:
            pass

    def _set_server(self, server):
        import esp32

        nvs = esp32.NVS("uiflow")
        try:
            nvs.set_str("server", server)
            nvs.commit()
        finally:
            pass

    def _load_data(self):
        self._server = self._get_server()

    def _update_data(self):
        pass

    def _load_view(self, load_bg=True):
        # bg img
        if load_bg:
            self._bg_img.set_src(CONFIG_BG_IMG)

        # ssid
        self._ssid_label.set_text_color(0x000000, 0xFFFFFF)
        self._ssid_label.set_text(self._ssid)

        # user id
        self._server_label.set_text(self._server)

        self._sprite.push(0, 0)

    def on_launch(self):
        DEBUG and print("Config Launch")
        self._server = self._get_server()

    def on_view(self):
        self._ssid_label = widgets.Label(
            str(None),
            15,
            63,
            w=138,
            h=24,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
            parent=self._sprite,
        )
        self._ssid_label.set_long_mode(widgets.Label.LONG_DOT)

        self._server_label = widgets.Label(
            str(None),
            15,
            119,
            w=138,
            h=24,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
            parent=self._sprite,
        )
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)

        self._bg_img = widgets.Image(use_sprite=False, parent=self._sprite)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(200, 200)

        self._load_view()

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        DEBUG and print("Config Exit")
        del self._ssid_label, self._server_label
        del self._bg_img

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        pass

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        if self._server == "uiflow2.m5stack.com":
            self._server = "sg.m5stack.com"
        else:
            self._server = "uiflow2.m5stack.com"
        # self._set_server(self._server)
        self._update_data()
        self._load_view(load_bg=False)


class AppListApp(AppBase):
    def __init__(self, sprite) -> None:
        self._sprite = sprite
        super().__init__()

    def on_launch(self):
        self._bg_img = widgets.Image(use_sprite=False, parent=self._sprite)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(200, 200)

        self._labels = []

        self._files = []
        for file in os.listdir("apps"):
            if file.endswith(".py"):
                self._files.append(file)
        self._files_number = len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def on_view(self):
        self._bg_img.set_src(APPLIST_BG_IMG)

        if len(self._labels) != 5:
            for i in range(5):
                self._labels.append(
                    widgets.Label(
                        "",
                        14,
                        37 + 27 * i,
                        w=138,
                        h=24,
                        fg_color=0x000000,
                        bg_color=0xFFFFFF,
                        font=M5.Lcd.FONTS.DejaVu18,
                        parent=self._sprite,
                    )
                )
                self._labels[-1].set_long_mode(widgets.Label.LONG_DOT)

        for label, file in zip(self._labels, self._files):
            # print("file:", file)
            file and label and label.set_text(file)

        self._sprite.push(0, 0)

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._labels, self._files

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        M5.Lcd.clear()
        execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        self._file_pos -= 1

        if self._file_pos < 0:
            self._file_pos = 0

        try:
            for i in range(len(self._labels)):
                file = self._files[i]
                if self._file_pos == i:
                    self._labels[i].set_text(">" + file)
                else:
                    self._labels[i].set_text(file)
        except:
            pass

        self._sprite.push(0, 0)
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        self._file_pos += 1

        if self._file_pos >= len(self._files):
            self._file_pos = 0

        if self._file_pos >= len(self._labels):
            self._file_pos = 0

        try:
            for i in range(len(self._labels)):
                file = self._files[i]
                if self._file_pos == i:
                    self._labels[i].set_text(">" + file)
                else:
                    self._labels[i].set_text(file)
        except:
            pass

        self._sprite.push(0, 0)


# CoreInk startup menu
class CoreInk_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        DEBUG and print("Corink startup")
        # DEBUG and M5.Lcd.drawCenterString("Corink startup2", 100, 100)
        self._wifi.connect_network(ssid, pswd)

        sprite = M5.Lcd.newCanvas(200, 200, 1, False)
        sprite.drawBmp(STARTUP_BG_IMG, 0, 0)
        sprite.push(0, 0)

        import time

        time.sleep_ms(3000)
        M5.Lcd.clear()

        flow_app = FlowApp(sprite, (self._wifi, ssid))
        config_app = ConfigApp(sprite, (self._wifi, ssid))
        applist_app = AppListApp(sprite)

        fw = Framework([flow_app, config_app, applist_app])
        asyncio.run(fw.run())
