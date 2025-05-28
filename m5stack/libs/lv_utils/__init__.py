# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
from .lv_utils import event_loop


def fs_register(fs_drv, letter, cache_size=500):
    import _lv_utils

    fs_drv.init()
    fs_drv.letter = ord(letter)
    fs_drv.open_cb = _lv_utils.fs_open_cb
    fs_drv.read_cb = _lv_utils.fs_read_cb
    fs_drv.write_cb = _lv_utils.fs_write_cb
    fs_drv.seek_cb = _lv_utils.fs_seek_cb
    fs_drv.tell_cb = _lv_utils.fs_tell_cb
    fs_drv.close_cb = _lv_utils.fs_close_cb

    if cache_size >= 0:
        fs_drv.cache_size = cache_size

    fs_drv.register()


import asyncio
import sys


class LVTaskHandler:
    _current_instance = None

    def __init__(self, freq=25, refresh_cb=None, exception_sink=None):
        if self.is_running():
            raise RuntimeError("Event loop is already running!")

        if not lv.is_initialized():
            lv.init()

        LVTaskHandler._current_instance = self

        self.delay = 1000 // freq
        self.refresh_cb = refresh_cb
        self.exception_sink = exception_sink if exception_sink else self.default_exception_sink
        self.refresh_event = asyncio.Event()
        self.refresh_task = asyncio.create_task(self.async_refresh())
        self.timer_task = asyncio.create_task(self.async_timer())

    @staticmethod
    def is_running():
        return LVTaskHandler._current_instance is not None

    @staticmethod
    def current_instance():
        return LVTaskHandler._current_instance

    async def async_refresh(self):
        while True:
            await self.refresh_event.wait()
            if lv._nesting.value == 0:
                self.refresh_event.clear()
                try:
                    lv.task_handler()
                except Exception as e:
                    if self.exception_sink:
                        self.exception_sink(e)
                if self.refresh_cb:
                    self.refresh_cb()

    async def async_timer(self):
        while True:
            await asyncio.sleep_ms(self.delay)
            lv.tick_inc(self.delay)
            self.refresh_event.set()

    def deinit(self):
        self.refresh_task.cancel()
        self.timer_task.cancel()
        LVTaskHandler._current_instance = None

    def default_exception_sink(self, e):
        sys.print_exception(e)
