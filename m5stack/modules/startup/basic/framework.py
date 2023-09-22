from .app import AppBase, AppSelector
import uasyncio as asyncio
import M5
import gc

from machine import I2C, Pin
from unit import CardKB, KeyCode


class KeyEvent:
    key = 0
    status = False


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
            while True:
                app = self._app_selector.current()
                if app != self._launcher:
                    app = self._app_selector.next()
                else:
                    break
            self._launcher.start()
        # asyncio.create_task(self.gc_task())

        self.i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
        self._kb_status = False
        if 0x5F in self.i2c0.scan():
            self._kb = CardKB(self.i2c0)
            self._event = KeyEvent()
            self._kb_status = True

        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btna_event_handler"):
                    await app._btna_event_handler(self)
                app.stop()
                app = self._app_selector.next()
                app.start()
            if M5.BtnB.wasClicked():
                M5.Speaker.tone(4000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btnb_event_handler"):
                    asyncio.create_task(app._btnb_event_handler(self))
            if M5.BtnC.wasClicked():
                M5.Speaker.tone(6000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btnc_event_handler"):
                    asyncio.create_task(app._btnc_event_handler(self))
            await asyncio.sleep_ms(100)

            if self._kb_status:
                if self._kb.is_pressed():
                    M5.Speaker.tone(3500, 50)
                    self._event.key = self._kb.get_key()
                    self._event.status = False
                    await self.handle_input(self._event)

    async def handle_input(self, event: KeyEvent):
        if event.key is KeyCode.KEYCODE_RIGHT:
            app = self._app_selector.current()
            app.stop()
            app = self._app_selector.next()
            app.start()
            event.status = True
        if KeyCode.KEYCODE_LEFT == event.key:
            app = self._app_selector.current()
            app.stop()
            app = self._app_selector.prev()
            app.start()
            event.status = True
        if event.status == False:
            app = self._app_selector.current()
            if hasattr(app, "_kb_event_handler"):
                await app._kb_event_handler(event, self)

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)
