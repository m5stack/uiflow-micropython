# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import _thread
import time

PERIODIC = 0x00
ONE_SHOT = 0x01


class SoftTimerScheduler:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._tims = []
        self._run = False
        self._initialized = True

    def add_timer(self, tim):
        if tim in self._tims:
            return

        self._tims.append(tim)
        if not self._run:
            _thread.start_new_thread(self._cb, ())
            self._run = True

    def del_timer(self, tim):
        while tim in self._tims:
            time.sleep_ms(100)

    def _cb(self):
        while self._run:
            # print("running...", self._tims)

            for tim in self._tims:
                if not tim.dead:
                    self.update(tim)

            time.sleep_ms(10)

        self._wait = False
        self._run = False

    def update(self, tim: "SoftTimer"):
        if time.ticks_ms() > tim.next_time:
            tim.next_time = time.ticks_ms() + tim.period
            if tim.mode == ONE_SHOT:
                tim.dead = True
            if tim.callback:
                tim.callback(tim)

    def deinit(self, tim: "SoftTimer"):
        self._wait = True
        self._run = False
        while self._wait:
            time.sleep_ms(100)


class SoftTimer:
    PERIODIC = 0x00
    ONE_SHOT = 0x01

    def __init__(self, mode=PERIODIC, period=-1, callback=None):
        if period < 10:
            return
        self.init(mode, period, callback)

    def init(self, mode=PERIODIC, period=-1, callback=None):
        # SoftTimerScheduler().del_timer(self)
        self.callback = callback
        self.next_time = time.ticks_ms() + period
        self.period = period
        self.mode = mode
        self.dead = False
        SoftTimerScheduler().add_timer(self)

    def deinit(self):
        self.dead = True
