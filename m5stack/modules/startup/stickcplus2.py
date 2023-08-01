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


class WiFiStatusApp:
    def __init__(self, data) -> None:
        self._ssid_label = Label(
            "",
            int(135 / 2),
            85,
            w=135,
            h=20,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x003F8C,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._ssid_label.setLongMode(Label.LONG_DOT)
        self._bg_img = Image()
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self._logo = Image()
        self._logo.set_x(26)
        self._logo.set_y(120)
        self._logo.set_size(85, 85)
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else "None"
        self._status = TaskStatus.init

    def registered(self):
        pass

    async def mount(self):
        self._bg_img.set_src("/system/stickcplus2/wificonnect.png")
        self._ssid_label.setText(self._ssid)
        self._status = TaskStatus.running
        asyncio.create_task(self.run())

    async def run(self):
        while self._status is TaskStatus.running:
            if self._wifi.connect_status() is not network.STAT_GOT_IP:
                M5.Lcd.fillCircle(68, 165, 36, 0xEEEEEE)
                await asyncio.sleep_ms(500)
                self._logo.set_src("/system/stickcplus2/wifi_logo.jpg")
                await asyncio.sleep_ms(500)
            else:
                await asyncio.sleep_ms(500)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        self._status = TaskStatus.pending
        while self._status is not TaskStatus.stop:
            await asyncio.sleep_ms(100)


class CloudStatusApp:
    def __init__(self) -> None:
        self._status_img = Image()
        self._status_img.set_x(0)
        self._status_img.set_y(0)
        self._status_img.set_size(135, 240)
        # self._status_img.set_src("/system/stickcplus2/cloud-disconnect.jpg")
        self._status = TaskStatus.init

    def registered(self):
        pass

    async def mount(self):
        self._status = TaskStatus.running
        self._src = None
        if _HAS_SERVER and M5Things.status() is 2:
            self._src = "/system/stickcplus2/cloud-connect.png"
        else:
            self._src = "/system/stickcplus2/cloud-disconnect.png"
        self._status_img.set_src(self._src)
        asyncio.create_task(self.run())

    async def run(self):
        self._update = False
        while self._status is TaskStatus.running:
            if _HAS_SERVER and M5Things.status() is 2:
                self._update = self._src is not "/system/stickcplus2/cloud-connect.png"
            else:
                self._update = self._src is not "/system/stickcplus2/cloud-disconnect.png"

            self._update and self._status_img.set_src(self._src)
            await asyncio.sleep_ms(200)

        self._status = TaskStatus.stop

    def handle_input(self):
        pass

    async def umount(self) -> None:
        self._status = TaskStatus.pending
        while self._status is not TaskStatus.stop:
            await asyncio.sleep_ms(50)


class SettingsApp:
    def __init__(self) -> None:
        pass


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


class StickCPlus2_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wifi.connect_network(ssid, pswd)
        M5.BtnA.setCallback(type=M5.BtnA.CB_TYPE.WAS_CLICKED, cb=self.BtnA_wasClicked_event)
        M5.BtnA.setCallback(type=M5.BtnA.CB_TYPE.WAS_HOLD, cb=self.BtnA_wasHold_event)
        M5.BtnB.setCallback(type=M5.BtnB.CB_TYPE.WAS_CLICKED, cb=self.BtnB_wasClicked_event)
        DEBUG and print("Run startup menu")

        self._apps = _app_generator([WiFiStatusApp((self._wifi, ssid)), CloudStatusApp()])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        loop.close()

    async def run(self):
        self._app = next(self._apps)
        asyncio.create_task(self._app.mount())
        while True:
            M5.update()
            await asyncio.sleep_ms(100)

    def BtnA_wasClicked_event(self, state):
        asyncio.create_task(self.BtnA_wasClicked_task(state))

    async def BtnA_wasClicked_task(self, state):
        print("BtnA_wasClicked_task")

    def BtnA_wasHold_event(self, state):
        asyncio.create_task(self.BtnA_wasHold_task(state))

    async def BtnA_wasHold_task(self, state):
        print("BtnA_wasHold_task")

    def BtnB_wasClicked_event(self, state):
        asyncio.create_task(self.BtnB_wasClicked_task(state))

    async def BtnB_wasClicked_task(self, state):
        print("BtnB_wasClicked_task")

        await asyncio.create_task(self._app.umount())
        self._app = next(self._apps)
        await asyncio.create_task(self._app.mount())
