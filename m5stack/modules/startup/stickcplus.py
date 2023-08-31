from . import Startup
import M5
import network
from widgets.label import Label
from widgets.image import Image
import os
import sys
import gc

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

if M5.getBoard() == M5.BOARD.M5StickCPlus:
    APPLIST_IMG = "res/stickcplus/APPLIST.jpg"
    BK_IMG = "res/stickcplus/bk.jpg"
    CLOUD1_IMG = "res/stickcplus/cloud1.jpg"
    CLOUD2_IMG = "res/stickcplus/cloud2.jpg"
    CLOUD3_IMG = "res/stickcplus/cloud3.jpg"
    CLOUD4_IMG = "res/stickcplus/cloud4.jpg"
    CLOUD5_IMG = "res/stickcplus/cloud5.jpg"
    CLOUD6_IMG = "res/stickcplus/cloud6.jpg"
    CLOUD7_IMG = "res/stickcplus/cloud7.jpg"
    CLOUD8_IMG = "res/stickcplus/cloud8.jpg"
    CLOUD9_IMG = "res/stickcplus/cloud9.jpg"
    CLOUD10_IMG = "res/stickcplus/cloud10.jpg"
    MODE1_IMG = "res/stickcplus/mode1.jpg"
    MODE2_IMG = "res/stickcplus/mode2.jpg"
    MODE3_IMG = "res/stickcplus/mode3.jpg"
    MODE4_IMG = "res/stickcplus/mode4.jpg"
    USB_IMG = "res/stickcplus/usb.jpg"
elif M5.getBoard() == M5.BOARD.M5StickCPlus2:
    APPLIST_IMG = "/system/stickcplus2/APPLIST.png"
    BK_IMG = "/system/stickcplus2/bk.png"
    CLOUD1_IMG = "/system/stickcplus2/cloud1.png"
    CLOUD2_IMG = "/system/stickcplus2/cloud2.png"
    CLOUD3_IMG = "/system/stickcplus2/cloud3.png"
    CLOUD4_IMG = "/system/stickcplus2/cloud4.png"
    CLOUD5_IMG = "/system/stickcplus2/cloud5.png"
    CLOUD6_IMG = "/system/stickcplus2/cloud6.png"
    CLOUD7_IMG = "/system/stickcplus2/cloud7.png"
    CLOUD8_IMG = "/system/stickcplus2/cloud8.png"
    CLOUD9_IMG = "/system/stickcplus2/cloud9.png"
    CLOUD10_IMG = "/system/stickcplus2/cloud10.png"
    MODE1_IMG = "/system/stickcplus2/mode1.png"
    MODE2_IMG = "/system/stickcplus2/mode2.png"
    MODE3_IMG = "/system/stickcplus2/mode3.png"
    MODE4_IMG = "/system/stickcplus2/mode4.png"
    USB_IMG = "/system/stickcplus2/usb.png"


class AppBase:
    def __init__(self) -> None:
        self._task = None

    def on_launch(self):
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


class UsbApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        self._battery_label = Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu12,
        )

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)

    def on_view(self):
        self._bg_img.set_src(USB_IMG)

    async def on_run(self):
        while True:
            # battery
            self._battery_label.setText(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._battery_label

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        pass

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        pass


class RunApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_ready(self):
        M5.Lcd.clear()
        execfile("main.py")
        sys.exit(0)


class ListApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        self._battery_label = Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu12,
        )
        self._bg_img = Image(use_sprite=False)
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
            self._label0 = Label(
                "",
                25,
                108,
                w=85,
                h=22,
                fg_color=0xFFFFFF,
                bg_color=0x333333,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label0.setLongMode(Label.LONG_DOT)
        if self._label1 is None:
            self._label1 = Label(
                "",
                25,
                108 + 22 + 5,
                w=85,
                h=22,
                fg_color=0x999999,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label1.setLongMode(Label.LONG_DOT)
        if self._label2 is None:
            self._label2 = Label(
                "",
                25,
                108 + 22 + 5 + 22 + 5,
                w=85,
                h=22,
                fg_color=0x4D4D4D,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label2.setLongMode(Label.LONG_DOT)

        if len(self._labels) is not 3:
            self._labels.clear()
            self._labels.append(self._label0)
            self._labels.append(self._label1)
            self._labels.append(self._label2)

        if self._lebal0 is None:
            self._lebal0 = Label(
                "",
                25,
                108 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x999999,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal0.setLongMode(Label.LONG_DOT)

        if self._lebal1 is None:
            self._lebal1 = Label(
                "",
                25,
                108 - 22 - 5 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x4D4D4D,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal1.setLongMode(Label.LONG_DOT)

        if self._lebal2 is None:
            self._lebal2 = Label(
                "",
                25,
                108 - 22 - 5 - 22 - 5 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x333333,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal2.setLongMode(Label.LONG_DOT)

        if len(self._lebals) is not 3:
            self._lebals.clear()
            self._lebals.append(self._lebal0)
            self._lebals.append(self._lebal1)
            self._lebals.append(self._lebal2)

        for label, file in zip(self._labels, self._files):
            # print("file:", file)
            file and label and label.setText(file)

    async def on_run(self):
        while True:
            # battery
            self._battery_label.setText(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._battery_label, self._labels, self._files, self._lebals

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        M5.Lcd.clear()
        execfile("apps/" + self._files[self._file_pos])
        sys.exit(0)

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        self._file_pos += 1

        if self._file_pos >= len(self._files):
            self._file_pos = 0

        for label in self._labels:
            label.setText("")

        for label, file in zip(self._labels, self._files[self._file_pos :]):
            file and label and label.setText(file)

        for label in self._lebals:
            label.setText("")

        files = self._files[: self._file_pos]
        files.reverse()

        for label, file in zip(self._lebals, files):
            file and label and label.setText(file)


_cloud_icos_0 = {
    0: CLOUD1_IMG,
    1: CLOUD2_IMG,
    2: CLOUD3_IMG,
    3: CLOUD4_IMG,
    4: CLOUD5_IMG,
}

_cloud_icos_1 = {
    0: CLOUD6_IMG,
    1: CLOUD7_IMG,
    2: CLOUD8_IMG,
    3: CLOUD10_IMG,
    4: CLOUD9_IMG,
}

_txt_bg_colors = {
    0: 0xCCCCCC,
    1: 0x33CC99,
    2: 0xFF6666,
    3: 0x00CCFF,
    4: 0x00CCFF,
}


class CloudApp(AppBase):
    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._user_id = None
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

    def _get_user_id(self):
        if _HAS_SERVER:
            return None if len(M5Things.status()[1]) is 0 else M5Things.status()[1]
        else:
            return None

    def _load_data(self):
        self._server = self._get_server()
        self._icos = {
            "uiflow2.m5stack.com": _cloud_icos_0,
            "sg.m5stack.com": _cloud_icos_1,
        }[self._server]
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def _update_data(self):
        self._icos = {
            "uiflow2.m5stack.com": _cloud_icos_0,
            "sg.m5stack.com": _cloud_icos_1,
        }[self._server]
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def _load_view(self):
        # bg img
        self._bg_img.set_src(self._icos.get(self._cloud_status))

        # ssid
        self._ssid_label.setTextColor(0x000000, _txt_bg_colors.get(self._cloud_status))
        self._ssid_label.setText(self._ssid)

        # user id
        self._user_id_label.setText(str(self._user_id))

        # rssi
        if self._cloud_status in (3, 4):
            self._rssi_label.setTextColor(0x000000, _txt_bg_colors.get(self._cloud_status))
            self._rssi_label.setText(str(self._wifi.get_rssi()))

        # battery
        self._battery_label.setText(str(M5.Power.getBatteryLevel()))

    def on_launch(self):
        self._server = self._get_server()
        self._icos = {
            "uiflow2.m5stack.com": _cloud_icos_0,
            "sg.m5stack.com": _cloud_icos_1,
        }[self._server]
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()

    def on_view(self):
        self._battery_label = Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu12,
        )

        self._ssid_label = Label(
            str(None),
            int(135 / 2),
            55,
            w=135,
            h=20,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCCCCCC,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)

        self._rssi_label = Label(
            str(None),
            65,
            82,
            w=135,
            h=20,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCCCCCC,
            font=M5.Lcd.FONTS.DejaVu12,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)

        self._user_id_label = Label(
            str(None),
            int(135 / 2),
            170,
            w=135,
            h=20,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x000000,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._user_id_label.setLongMode(Label.LONG_DOT)

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)

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
        del self._battery_label, self._ssid_label, self._rssi_label, self._user_id_label
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
        self._set_server(self._server)
        self._update_data()
        self._load_view()


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


class MenuApp(AppBase):
    def __init__(self, data=None) -> None:
        self._cloud_app = data
        self._menus = (
            (self._cloud_app, MODE1_IMG),
            (UsbApp(), MODE2_IMG),
            (RunApp(), MODE3_IMG),
            (ListApp(), MODE4_IMG),
        )

    def on_launch(self):
        self._icos = _charge_ico(self._menus)
        self._app, self._img_src = next(self._icos)

    def on_view(self):
        self._status_img = Image(use_sprite=False)
        self._status_img.set_x(0)
        self._status_img.set_y(0)
        self._status_img.set_size(135, 240)
        self._status_img.set_src(self._img_src)

        self._tips_label = Label(
            "",
            67,
            108 - 22 - 5 - 22 - 5 - 22 - 5,
            w=135,
            h=20,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x00CCFF,
            bg_color=0x000000,
            font=M5.Lcd.FONTS.DejaVu18,
        )

        self._battery_label = Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu12,
        )
        self._battery_label.setText(str(M5.Power.getBatteryLevel()))

    async def on_run(self):
        while True:
            # battery
            self._battery_label.setText(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        if self._app:
            await fw.unload(self)
            await fw.load(self._app)

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        self._app, src = next(self._icos)
        self._status_img.set_src(src)
        self._battery_label.setText(str(M5.Power.getBatteryLevel()))
        if type(self._app) == RunApp:
            self._tips_label.setText("main.py")


class LauncherApp(AppBase):
    def __init__(self, data=None) -> None:
        self._cloud_app, self._menu_app = data

    def on_view(self):
        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(0, 0)
        self._bg_img.set_size(135, 240)
        self._bg_img.set_src(BK_IMG)

    def on_exit(self):
        del self._bg_img

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        await fw.unload(self)
        await fw.load(self._cloud_app)

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        await fw.unload(self)
        await fw.load(self._menu_app)


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._launcher = None

    def install_launcher(self, launcher: AppBase):
        self._launcher = launcher

    def install(self, app: AppBase):
        self._apps.append(app)

    async def unload(self, app: AppBase):
        # app = self._apps.pop()
        await app.on_hide()

    async def load(self, app: AppBase):
        self._apps.append(app)
        app.on_launch()
        app.on_view()
        app.on_ready()

    async def reload(self, app: AppBase):
        await app.on_hide()
        app.on_ready()

    async def run(self):
        asyncio.create_task(self.load(self._launcher))
        # asyncio.create_task(self.gc_task())
        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                M5.Speaker.tone(4000, 50)
                app = self._apps[-1]
                asyncio.create_task(app._keycode_enter_event_handler(self))
            if M5.BtnB.wasClicked():
                M5.Speaker.tone(6000, 50)
                app = self._apps[-1]
                asyncio.create_task(app._keycode_dpad_down_event_handler(self))
            if M5.BtnPWR.wasClicked():
                M5.Speaker.tone(3500, 50)
                if self._apps and len(self._apps) > 1:
                    app = self._apps.pop()
                    await app._keycode_back_event_handler(self)
                    await app.on_hide()
                    app.on_exit()
                    app = self._apps[-1]
                    app.on_launch()
                    app.on_view()
                    app.on_ready()
            await asyncio.sleep_ms(100)

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)


class StickCPlus_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wifi.connect_network(ssid, pswd)
        M5.Speaker.setVolume(255)
        M5.Speaker.tone(4000, 50)

        bg_img = Image(use_sprite=False)
        bg_img.set_pos(0, 0)
        bg_img.set_size(135, 240)
        bg_img.set_src(BK_IMG)
        M5.Lcd.setBrightness(0)
        import time

        for i in range(0, 128, 20):
            M5.Lcd.setBrightness(i)
            time.sleep_ms(80)
        DEBUG and print("Run startup menu")

        cloud_app = CloudApp((self._wifi, ssid))
        menu_app = MenuApp(data=cloud_app)
        launcher = LauncherApp(data=(cloud_app, menu_app))

        fw = Framework()
        fw.install_launcher(launcher)
        asyncio.run(fw.run())
