# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase, AppSelector
from machine import I2C, Pin
from unit import CardKBUnit, KeyCode
import M5
import gc
import asyncio


class KeyEvent:
    key = 0
    status = False


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = AppSelector(self._apps)
        self._launcher = None
        self._bar = None

    def install_bar(self, bar: AppBase):
        self._bar = bar

    def install_sidebar(self, bar: AppBase):
        self._sidebar = bar

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
        self._bar and self._bar.start()
        if self._launcher:
            while True:
                app = self._app_selector.current()
                if app != self._launcher:
                    app = self._app_selector.next()
                else:
                    break
            self._launcher.start()
        # asyncio.create_task(self.gc_task())

        self.i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
        self._kb_status = False
        if 0x5F in self.i2c0.scan():
            self._kb = CardKBUnit(self.i2c0)
            self._event = KeyEvent()
            self._kb_status = True

        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                app = self._app_selector.current()
                if hasattr(app, "_btna_next_event_handler"):
                    await app._btna_next_event_handler(self)
            if M5.BtnB.wasClicked():
                app = self._app_selector.current()
                if hasattr(app, "_btnb_enter_event_handler"):
                    await app._btnb_enter_event_handler(self)
            elif M5.BtnB.wasHold():
                app = self._app_selector.current()
                if hasattr(app, "_btnb_back_event_handler"):
                    await app._btnb_back_event_handler(self)
                app.stop()
                self._app_selector.select(self._launcher)
                self._launcher.start()
            elif M5.BtnB.wasDoubleClicked():
                app = self._app_selector.current()
                if hasattr(app, "_btnb_ctrl_event_handler"):
                    await app._btnb_ctrl_event_handler(self)
            if M5.BtnC.wasClicked():
                app = self._app_selector.current()
                if hasattr(app, "_btnc_next_event_handler"):
                    await app._btnc_next_event_handler(self)
            await asyncio.sleep_ms(10)

            if self._kb_status:
                if self._kb.is_pressed():
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
        if event.status is False:
            app = self._app_selector.current()
            if hasattr(app, "_kb_event_handler"):
                await app._kb_event_handler(event, self)

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)
