# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import app_base
import machine
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
        self._app_selector = app_base.AppSelector(self._apps)
        self._launcher = None
        self._bar = None

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

        self.i2c0 = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2), freq=100000)
        self._kb_status = False
        if 0x5F in self.i2c0.scan():
            self._kb = CardKBUnit(self.i2c0)
            self._event = KeyEvent()
            self._kb_status = True

        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btna_next_event_handler"):
                    await app._btna_next_event_handler(self)
            if M5.BtnB.wasClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btnb_enter_event_handler"):
                    await app._btnb_enter_event_handler(self)
            elif M5.BtnB.wasHold():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btnb_back_event_handler"):
                    await app._btnb_back_event_handler(self)
                app.stop()
                self._app_selector.select(self._launcher)
                self._launcher.start()
            elif M5.BtnB.wasDoubleClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btnb_ctrl_event_handler"):
                    await app._btnb_ctrl_event_handler(self)
            if M5.BtnC.wasClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_btnc_next_event_handler"):
                    await app._btnc_next_event_handler(self)
            await asyncio.sleep_ms(10)

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
