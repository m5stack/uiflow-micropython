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
            cls._instance = object.__new__(cls)
            cls._instance._tims = []
            cls._run = False
        return cls._instance

    def add_timer(self, tim):
        self._tims.append(tim)
        if not self._run:
            _thread.start_new_thread(self._cb, ())
            self._run = True

    def del_timer(self, tim):
        while tim in self._tims:
            time.sleep_ms(100)

    def _cb(self):
        while self._run:
            to_delete = []
            for tim in self._tims:
                if tim.dead:
                    to_delete.append(tim)
                else:
                    self.update(tim)
            for tim in to_delete:
                self._tims.remove(tim)
            to_delete = []
            #             if not self._tims:
            #                 break;
            time.sleep_ms(10)
        self._wait = False
        self._run = False

    def update(self, tim):
        if time.ticks_ms() > tim.next_time:
            tim.next_time = time.ticks_ms() + tim.period
            tim.callback and tim.callback()
            if tim.mode == ONE_SHOT:
                tim.dead = True

    def deinit(self, tim):
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
        SoftTimerScheduler().del_timer(self)
        self.callback = callback
        self.next_time = time.ticks_ms() + period
        self.period = period
        self.mode = mode
        self.dead = False
        SoftTimerScheduler().add_timer(self)

    def deinit(self):
        self.dead = True
