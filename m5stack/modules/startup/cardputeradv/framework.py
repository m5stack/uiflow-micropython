# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import app_base
from hardware import MatrixKeyboard
import M5
import gc
import asyncio
from unit import KeyCode


class KeyEvent:
    key = 0
    status = False


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = app_base.AppSelector(self._apps)
        self._launcher = None
        self._bar = None
        self._sidebar = None

    def install_bar(self, bar: app_base.AppBase):
        self._bar = bar

    def install_sidebar(self, bar: app_base.AppBase):
        self._sidebar = bar

    def install_launcher(self, launcher: app_base.AppBase):
        self._launcher = launcher

    def install(self, app: app_base.AppBase):
        app.install()
        self._apps.append(app)

    def start(self):
        # asyncio.create_task(self.gc_task())
        asyncio.run(self.run())

    async def unload(self, app: app_base.AppBase):
        # app = self._apps.pop()
        app.stop()

    async def load(self, app: app_base.AppBase):
        app.start()

    async def reload(self, app: app_base.AppBase):
        app.stop()
        app.start()

    async def run(self):
        kb = MatrixKeyboard()
        event = KeyEvent()

        self._bar and self._bar.start()
        self._sidebar and self._sidebar.start()
        if self._launcher:
            self._app_selector.select(self._launcher)
            self._launcher.start()

        while True:
            M5.update()
            # kb.tick()
            if kb.is_pressed():
                M5.Speaker.tone(3500, 50)
                event.key = kb.get_key()
                event.status = False
                await self.handle_input(event)

            if M5.BtnA.wasClicked():
                app = self._app_selector.current()
                if hasattr(app, "_btna_event_handler"):
                    await app._btna_event_handler(self)
                app.stop()
                self._app_selector.select(self._launcher)
                self._launcher.start()

            await asyncio.sleep_ms(10)

    async def handle_input(self, event: KeyEvent):
        print("key:", event.key)

        app = self._app_selector.current()
        if hasattr(app, "_kb_event_handler"):
            await app._kb_event_handler(event, self)

        if event.status is False:
            if event.key == KeyCode.KEYCODE_ESC:  # ESC key
                app = self._app_selector.current()
                if hasattr(app, "_btna_event_handler"):
                    await app._btna_event_handler(self)
                app.stop()
                self._app_selector.select(self._launcher)
                self._launcher.start()
                return

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)
