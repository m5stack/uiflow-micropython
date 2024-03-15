# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase, AppSelector
import uasyncio as asyncio
import M5
import gc
import time
from machine import I2C, Pin
from unit import CardKBUnit, KeyCode


class KeyEvent:
    key = 0
    status = False


binary_data = None
_wav_path = None


def _playWav(wav: str):
    global binary_data, _wav_path
    if binary_data is None or _wav_path is not wav:
        with open(wav, "rb") as f:
            binary_data = f.read()
        _wav_path = wav
        if wav is "/system/common/wav/click.wav":
            M5.Speaker.setVolume(64)
        else:
            M5.Speaker.setVolume(127)
    M5.Speaker.playWav(binary_data)


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = AppSelector(self._apps)
        self._launcher = None
        self._bar = None
        self._last_app = None

    def install_bar(self, bar: AppBase):
        self._bar = bar

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
            self._app_selector.select(self._launcher)
            self._launcher.start()
            self._last_app = self._launcher

        self.i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
        self._kb_status = False
        if 0x5F in self.i2c0.scan():
            self._kb = CardKBUnit(self.i2c0)
            self._event = KeyEvent()
            self._kb_status = True

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
                        _playWav("/system/common/wav/click.wav")
                        x = M5.Touch.getX()
                        y = M5.Touch.getY()
                        select_app = None
                        for app in self._apps:
                            if self._is_select(app, x, y):
                                select_app = app
                                self._app_selector.select(select_app)
                                break
                        if select_app != None:
                            if self._last_app != select_app and self._last_app != None:
                                self._last_app.stop()
                                select_app.start()
                                self._last_app = select_app
                        else:
                            app = self._app_selector.current()
                            if hasattr(app, "_click_event_handler"):
                                await app._click_event_handler(x, y, self)
                    last_touch_time = time.ticks_ms()

            if self._kb_status:
                if self._kb.is_pressed():
                    _playWav("/system/common/wav/click.wav")
                    self._event.key = self._kb.get_key()
                    self._event.status = False
                    await self.handle_input(self._event)

            await asyncio.sleep_ms(10)

    async def handle_input(self, event: KeyEvent):
        if event.key is KeyCode.KEYCODE_RIGHT:
            self._last_app.stop()
            app = self._app_selector.next()
            app.start()
            self._last_app = app
            event.status = True
        if KeyCode.KEYCODE_LEFT == event.key:
            self._last_app.stop()
            app = self._app_selector.prev()
            app.start()
            self._last_app = app
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

    @staticmethod
    def _is_select(app: AppBase, x, y):
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
