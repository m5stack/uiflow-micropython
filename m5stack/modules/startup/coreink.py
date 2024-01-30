# -*- encoding: utf-8 -*-
# CoreInk startup script
from startup import Startup
import M5
import network
from widgets.label import Label
from widgets.image import Image
import os
import sys
import gc
import machine
import binascii

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = True

STARTUP_BG_IMG = '/flash/res/coreink/Startup.bmp'
FLOW_BG_IMG = '/flash/res/coreink/Flow.bmp'
CONFIG_BG_IMG = '/flash/res/coreink/Config.bmp'

WIFI_IMG = '/flash/res/coreink/wifi.bmp'
WIFI_ERR_IMG = '/flash/res/coreink/wifi_err.bmp'
SERVER_IMG = '/flash/res/coreink/server.bmp'
SERVER_ERR_IMG = '/flash/res/coreink/server_err.bmp'

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
                DEBUG and print('Switch to %d' %self._current_app)
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
    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._mac = None
        self._user_id = None
        self._cloud_status = 0

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

        if _cloud_status is not 1 or _HAS_SERVER is not True:
            return _cloud_status

        if M5Things.status() == 2:
            _cloud_status = 4
        else:
            _cloud_status = 3
        return _cloud_status

    def _get_user_id(self):
        if _HAS_SERVER:
            return None if len(M5Things.info()[1]) is 0 else M5Things.info()[1]
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
        self._mac_label.setTextColor(0x000000, 0xffffff)
        self._mac_label.setText(self._mac)

        # user id
        self._user_id_label.setText(str(self._user_id))

        # server, wifi
        if self._cloud_status == 0 or self._cloud_status == 2:
            self._wifi_img.set_src(WIFI_ERR_IMG)
        else:
            self._wifi_img.set_src(WIFI_IMG)

        if self._cloud_status == 4:
            self._server_img.set_src(SERVER_IMG)
        else:
            self._server_img.set_src(SERVER_ERR_IMG)

    def on_launch(self):
        DEBUG and print("Flow Launch")
        self._mac = self._get_mac()
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def on_view(self):
        self._mac_label = Label(
            str(None),
            15,
            63,
            w=138,
            h=24,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._mac_label.setLongMode(Label.LONG_DOT)

        self._user_id_label = Label(
            str(None),
            15,
            119,
            w=138,
            h=24,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._user_id_label.setLongMode(Label.LONG_DOT)

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(200, 200)

        self._wifi_img = Image(use_sprite=False)
        self._wifi_img.set_x(4)
        self._wifi_img.set_y(176)
        self._wifi_img.set_size(32, 24)

        self._server_img = Image(use_sprite=False)
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
    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._server = None
        self._cloud_status = 0

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

        if _cloud_status is not 1 or _HAS_SERVER is not True:
            return _cloud_status

        if M5Things.status() == 2:
            _cloud_status = 4
        else:
            _cloud_status = 3
        return _cloud_status

    def _load_data(self):
        self._server = self._get_server()
        self._cloud_status = self._get_cloud_status()

    def _update_data(self):
        self._cloud_status = self._get_cloud_status()

    def _load_view(self, load_bg = True):
        # bg img
        if load_bg:
            self._bg_img.set_src(CONFIG_BG_IMG)

        # ssid
        self._ssid_label.setTextColor(0x000000, 0xffffff)
        self._ssid_label.setText(self._ssid)

        # user id
        self._server_label.setText(self._server)

    def on_launch(self):
        DEBUG and print("Config Launch")
        self._server = self._get_server()
        self._cloud_status = self._get_cloud_status()

    def on_view(self):
        self._ssid_label = Label(
            str(None),
            15,
            63,
            w=138,
            h=24,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)

        self._server_label = Label(
            str(None),
            15,
            119,
            w=138,
            h=24,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._server_label.setLongMode(Label.LONG_DOT)

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(200, 200)

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
        DEBUG and print("Config Exit")
        try:
            del self._ssid_label, self._server_label
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
        # print("_keycode_dpad_down_event_handler")
        if self._server == "uiflow2.m5stack.com":
            self._server = "sg.m5stack.com"
        else:
            self._server = "uiflow2.m5stack.com"
        # self._set_server(self._server)
        self._update_data()
        self._load_view(load_bg=False)


# CoreInk startup menu
class CoreInk_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        DEBUG and print('Corink startup')
        DEBUG and M5.Lcd.drawCenterString("Corink startup2", 100, 100)
        self._wifi.connect_network(ssid, pswd)

        # bg_img = Image(use_sprite=False)
        # bg_img.set_pos(0, 0)
        # bg_img.set_size(200, 200)
        # bg_img.set_src(STARTUP_BG_IMG)

        # import time
        # time.sleep_ms(3000)

        flow_app = FlowApp((self._wifi, ssid))
        config_app = ConfigApp((self._wifi, ssid))

        fw = Framework([flow_app, config_app])
        asyncio.run(fw.run())

coreink = CoreInk_Startup()
coreink.startup('Real-Internet', 'ENIAC2333')