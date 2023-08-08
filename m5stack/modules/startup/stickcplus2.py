from . import Startup
import M5
import network
from widgets.label import Label
from widgets.image import Image

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


class TaskStatus:
    init = const(0)
    running = const(1)
    pending = const(2)
    stop = const(3)


class AppBase:
    def __init__(self) -> None:
        self._status = TaskStatus.init

    def registered(self):
        pass

    async def mount(self):
        self._status = TaskStatus.running
        asyncio.create_task(self.run())

    async def run(self):
        while self._status is TaskStatus.running:
            await asyncio.sleep_ms(500)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        if self._status is TaskStatus.running:
            self._status = TaskStatus.pending
            while self._status is not TaskStatus.stop:
                await asyncio.sleep_ms(100)


class ListApp(AppBase):
    def __init__(self) -> None:
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
        self._status = TaskStatus.running

    def registered(self):
        pass

    async def mount(self):
        self._status = TaskStatus.running
        asyncio.create_task(self.run())

    async def run(self):
        while self._status is TaskStatus.running:
            await asyncio.sleep_ms(500)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        if self._status is TaskStatus.running:
            self._status = TaskStatus.pending
            while self._status is not TaskStatus.stop:
                await asyncio.sleep_ms(100)


_cloud_icos_0 = {
    0: "/system/stickcplus2/cloud1.png",
    1: "/system/stickcplus2/cloud2.png",
    2: "/system/stickcplus2/cloud3.png",
    3: "/system/stickcplus2/cloud4.png",
    4: "/system/stickcplus2/cloud5.png",
}

_cloud_icos_1 = {
    0: "/system/stickcplus2/cloud6.png",
    1: "/system/stickcplus2/cloud7.png",
    2: "/system/stickcplus2/cloud8.png",
    3: "/system/stickcplus2/cloud10.png",
    4: "/system/stickcplus2/cloud9.png",
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

        self._bg_img = Image()
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self.icos = None
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._user_id = None
        self._cloud_status = 0
        self._status = TaskStatus.init

    def registered(self):
        pass

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
        self._icos = {
            "uiflow2.m5stack.com": _cloud_icos_0,
            "sg.m5stack.com": _cloud_icos_1,
        }[self._get_server()]
        self._cloud_status = self._get_cloud_status()
        self._user_id = self._get_user_id()
        print("status:", self._cloud_status)

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

    async def mount(self):
        self._load_data()
        self._load_view()

        # task
        M5.BtnB.setCallback(type=M5.BtnB.CB_TYPE.WAS_CLICKED, cb=self.BtnB_wasClicked_event)
        self._status = TaskStatus.running
        asyncio.create_task(self.run())

    async def run(self):
        while self._status is TaskStatus.running:
            t = self._get_cloud_status()
            if t is not self._cloud_status:
                self._cloud_status = t
                self._load_view()
                await asyncio.sleep_ms(500)
            else:
                await asyncio.sleep_ms(500)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        if self._status is TaskStatus.running:
            self._status = TaskStatus.pending
            while self._status is not TaskStatus.stop:
                await asyncio.sleep_ms(100)

    def BtnB_wasClicked_event(self, state):
        asyncio.create_task(self.BtnB_wasClicked_task(state))

    async def BtnB_wasClicked_task(self, state):
        print("BtnB_wasClicked_task")
        if self._get_server() == "uiflow2.m5stack.com":
            self._set_server("sg.m5stack.com")
        else:
            self._set_server("uiflow2.m5stack.com")
        await asyncio.create_task(self.umount())
        asyncio.create_task(self.mount())


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


_menu_icos = (
    (ListApp(), "/system/stickcplus2/mode1.png"),
    (None, "/system/stickcplus2/mode2.png"),
    (None, "/system/stickcplus2/mode3.png"),
    (None, "/system/stickcplus2/mode4.png"),
)


class MenuApp(AppBase):
    def __init__(self) -> None:
        self._status_img = Image()
        self._status_img.set_x(0)
        self._status_img.set_y(0)
        self._status_img.set_size(135, 240)
        self._status = TaskStatus.init

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
        self._icos = _charge_ico(_menu_icos)

    def registered(self):
        pass

    async def mount(self):
        self._status = TaskStatus.running
        self.app, src = next(self._icos)
        self._status_img.set_src(src)

        # task
        M5.BtnA.setCallback(type=M5.BtnA.CB_TYPE.WAS_CLICKED, cb=self.BtnA_wasClicked_event)
        M5.BtnB.setCallback(type=M5.BtnB.CB_TYPE.WAS_CLICKED, cb=self.BtnB_wasClicked_event)
        asyncio.create_task(self.run())

    async def run(self):
        while self._status is TaskStatus.running:
            # battery
            self._battery_label.setText(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(500)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        if self._status is TaskStatus.running:
            self._status = TaskStatus.pending
            while self._status is not TaskStatus.stop:
                await asyncio.sleep_ms(100)

    def BtnA_wasClicked_event(self, state):
        asyncio.create_task(self.BtnA_wasClicked_task(state))

    async def BtnA_wasClicked_task(self, state):
        print("BtnA_wasClicked_task")
        await asyncio.create_task(self.umount())
        asyncio.create_task(self.app.mount())

    def BtnB_wasClicked_event(self, state):
        asyncio.create_task(self.BtnB_wasClicked_task(state))

    async def BtnB_wasClicked_task(self, state):
        print("BtnB_wasClicked_task")
        self.app, src = next(self._icos)
        self._status_img.set_src(src)
        self._battery_label.setText(str(M5.Power.getBatteryLevel()))


def _app_generator(icos):
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
        self._bg_img = Image()
        self._bg_img.set_pos(0, 0)
        self._bg_img.set_size(135, 240)
        self._cloud_app, self._menu_app = data

    def registered(self):
        pass

    async def mount(self):
        print("mount")
        self._bg_img.set_src("/system/stickcplus2/bk.png")
        M5.BtnA.setCallback(type=M5.BtnA.CB_TYPE.WAS_CLICKED, cb=self.BtnA_wasClicked_event)
        M5.BtnB.setCallback(type=M5.BtnB.CB_TYPE.WAS_CLICKED, cb=self.BtnB_wasClicked_event)
        self._status = TaskStatus.running
        asyncio.create_task(self.run())

    async def run(self):
        while self._status is TaskStatus.running:
            await asyncio.sleep_ms(500)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        if self._status is TaskStatus.running:
            self._status = TaskStatus.pending
            while self._status is not TaskStatus.stop:
                await asyncio.sleep_ms(100)

    def BtnA_wasClicked_event(self, state):
        asyncio.create_task(self.BtnA_wasClicked_task(state))

    async def BtnA_wasClicked_task(self, state):
        print("BtnA_wasClicked_task")
        await asyncio.create_task(self.umount())
        await asyncio.create_task(self._cloud_app.mount())

    def BtnB_wasClicked_event(self, state):
        asyncio.create_task(self.BtnB_wasClicked_task(state))

    async def BtnB_wasClicked_task(self, state):
        print("BtnB_wasClicked_task")
        await asyncio.create_task(self.umount())
        await asyncio.create_task(self._menu_app.mount())


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._launcher = None

    def register_launcher(self, launcher: AppBase):
        self._launcher = launcher

    def register(self, app: AppBase):
        self._apps.append(app)

    def run(self):
        pass


class StickCPlus2_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wifi.connect_network(ssid, pswd)
        M5.BtnB.setCallback(type=M5.BtnB.CB_TYPE.WAS_HOLD, cb=self.BtnB_wasHold_event)
        DEBUG and print("Run startup menu")

        self._launcher = LauncherApp(data=(CloudApp((self._wifi, ssid)), MenuApp()))
        self._apps_tree = []
        # self._apps = _app_generator([CloudApp((self._wifi, ssid)), MenuApp()])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        loop.close()

    async def run(self):
        self._apps_tree.append(self._launcher)
        asyncio.create_task(self._launcher.mount())
        while True:
            M5.update()
            await asyncio.sleep_ms(100)

    def BtnB_wasHold_event(self, state):
        asyncio.create_task(self.BtnB_wasHold_task(state))

    async def BtnB_wasHold_task(self, state):
        print("BtnB_wasHold_event")
        if self._apps_tree:
            app = self._apps_tree.pop(0)
            await asyncio.create_task(app.umount())
            app = self._apps_tree.pop(0)
            asyncio.create_task(app.mount())
