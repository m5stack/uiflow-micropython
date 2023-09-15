from .app import AppBase, AppSelector
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import M5
import gc

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

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)
