# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from . import app_base
import asyncio
import M5
import gc
import time
import machine
from unit import CardKBUnit, KeyCode
import hardware


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
        self.i2c0 = machine.I2C(0, scl=machine.Pin(15), sda=machine.Pin(13), freq=100000)
        self._kb_status = False
        if 0x5F in self.i2c0.scan():
            self._kb = CardKBUnit(self.i2c0)
            self._event = KeyEvent()
            self._kb_status = True
        rotary = hardware.Rotary()

        self._bar and self._bar.start()
        if self._launcher:
            self._app_selector.select(self._launcher)
            self._launcher.start()

        last_touch_time = time.ticks_ms()
        while True:
            M5.update()
            if M5.Touch.getCount() > 0:
                detail = M5.Touch.getDetail(0)
                cur_time = time.ticks_ms()
                if cur_time - last_touch_time > 150:
                    if detail[9]:  # isHolding
                        pass
                    else:
                        M5.Speaker.tone(3500, 50)
                        x = M5.Touch.getX()
                        y = M5.Touch.getY()
                        app = self._app_selector.current()
                        if hasattr(app, "_click_event_handler"):
                            await app._click_event_handler(x, y, self)
                    last_touch_time = time.ticks_ms()

            if rotary.get_rotary_status():
                app = self._app_selector.current()
                app.stop()
                if rotary.get_rotary_increments() > 0:
                    M5.Speaker.tone(7000, 20)
                    app = self._app_selector.next()
                else:
                    M5.Speaker.tone(6000, 20)
                    app = self._app_selector.prev()
                app.start()

            if self._kb_status:
                if self._kb.is_pressed():
                    M5.Speaker.tone(3500, 50)
                    self._event.key = self._kb.get_key()
                    self._event.status = False
                    await self.handle_input(self._event)

            await asyncio.sleep_ms(10)

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
