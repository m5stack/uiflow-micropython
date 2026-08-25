# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import app_base
from . import layout
import asyncio
import M5
import gc
import time
import machine
from unit import CardKBUnit, KeyCode


class KeyEvent:
    key = 0
    status = False


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = app_base.AppSelector(self._apps)
        self._launcher = None
        self._bar = None
        self._last_app = None
        self._overlay = None

    def install_bar(self, bar: app_base.AppBase):
        self._bar = bar

    def install_overlay(self, overlay):
        # A widget that stays on screen across all apps, e.g. the power off
        # button. It is redrawn after every app switch.
        self._overlay = overlay

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
        self._start_app(app)

    async def reload(self, app: app_base.AppBase):
        app.stop()
        self._start_app(app)

    def _start_app(self, app: app_base.AppBase):
        layout.begin_full_refresh()
        try:
            app.start()
            self._overlay and self._overlay.show(app)
        finally:
            layout.end_full_refresh()

    async def run(self):
        if self._launcher:
            self._app_selector.select(self._launcher)
            self._start_app(self._launcher)
            self._last_app = self._launcher
        self._bar and self._bar.start()

        self._kb_status = False
        if not layout.IS_PAPERMONO:
            self.i2c0 = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2), freq=100000)
            if 0x5F in self.i2c0.scan():
                self._kb = CardKBUnit(self.i2c0)
                self._event = KeyEvent()
                self._kb_status = True

        last_touch_time = time.ticks_ms()
        touch_locked = False
        release_samples = 0
        while True:
            M5.update()
            touch_count = M5.Touch.getCount()
            if layout.IS_PAPERMONO:
                if touch_count > 0:
                    release_samples = 0
                    if not touch_locked:
                        touch_locked = True
                        await self._handle_touch(M5.Touch.getX(), M5.Touch.getY())
                elif touch_locked:
                    release_samples += 1
                    if release_samples >= 5:
                        touch_locked = False
                        release_samples = 0
            elif touch_count > 0:
                cur_time = time.ticks_ms()
                if cur_time - last_touch_time > 150:
                    detail = M5.Touch.getDetail(0)
                    if detail[9]:  # isHolding
                        pass
                    else:
                        await self._handle_touch(M5.Touch.getX(), M5.Touch.getY())
                    last_touch_time = time.ticks_ms()

            if self._kb_status:
                if self._kb.is_pressed():
                    M5.Speaker.playWavFile("/system/common/wav/click.wav")
                    self._event.key = self._kb.get_key()
                    self._event.status = False
                    await self.handle_input(self._event)

            self._overlay and self._overlay.tick()

            await asyncio.sleep_ms(10)

    async def _handle_touch(self, x, y):
        M5.Speaker.playWavFile("/system/common/wav/click.wav")
        x, y = layout.touch_point(x, y)
        if self._overlay and self._overlay.handle(x, y):
            return
        select_app = None
        for app in self._apps:
            if self._is_select(app, x, y):
                select_app = app
                self._app_selector.select(select_app)
                break
        if select_app is not None:
            if self._last_app != select_app and self._last_app is not None:
                self._last_app.stop()
                self._start_app(select_app)
                self._last_app = select_app
                self._bar and self._bar.refresh()
        else:
            app = self._app_selector.current()
            if hasattr(app, "_click_event_handler"):
                await app._click_event_handler(x, y, self)

    async def handle_input(self, event: KeyEvent):
        if event.key is KeyCode.KEYCODE_RIGHT:
            self._last_app.stop()
            app = self._app_selector.next()
            self._start_app(app)
            self._last_app = app
            event.status = True
        if KeyCode.KEYCODE_LEFT == event.key:
            self._last_app.stop()
            app = self._app_selector.prev()
            self._start_app(app)
            self._last_app = app
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

    @staticmethod
    def _is_select(app: app_base.AppBase, x, y):
        descriptor = app.descriptor
        if x < descriptor.x:
            return False
        if x > (descriptor.x + descriptor.w):
            return False
        if y < descriptor.y:
            return False
        if y > (descriptor.y + descriptor.h):
            return False
        return True
