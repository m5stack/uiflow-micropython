# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import Pin
import time
from micropython import const

CHANNEL_A_128 = const(1)
CHANNEL_A_64 = const(3)
CHANNEL_B_32 = const(2)

DATA_BITS = const(24)
MAX_VALUE = const(0x7FFFFF)
MIN_VALUE = const(0x800000)


class WEIGHTUnit:
    def __init__(self, port) -> None:
        self.hx711data = Pin(port[0], Pin.IN)
        self.hx711clk = Pin(port[1], Pin.OUT)
        self.zero_value = 0
        self.hx711clk.value(0)
        self._channel = 1
        self._scale = 1.0

    @property
    def get_raw_weight(self) -> int:
        count = 0
        if self.is_ready_wait():
            for i in range(24):
                self.hx711clk.value(1)
                time.sleep_us(1)
                self.hx711clk.value(0)
                time.sleep_us(1)
                if self.hx711data.value():
                    count += 1
                count = count << 1
        else:
            return 0

        gain_m = self._channel
        while gain_m:
            self.hx711clk.value(1)
            time.sleep_us(1)
            self.hx711clk.value(0)
            time.sleep_us(1)
            gain_m -= 1
        count = count ^ 0x800000
        return count

    @property
    def get_scale_weight(self) -> int:
        return int((self.get_raw_weight - self.zero_value) * self._scale)

    def set_tare(self) -> None:
        self.zero_value = self.get_raw_weight

    def set_calibrate_scale(self, weight):
        self._scale = (1.0 * weight) / (self.get_raw_weight - self.zero_value)

    def is_ready_wait(self) -> bool:
        times = 0
        while self.hx711data.value():
            times += 1
            time.sleep_ms(10)
            if times > 25:
                break
        return not self.hx711data.value()

    def set_channel(self, chan: int) -> None:
        self._channel = chan
        for i in range(self._channel):
            self.hx711clk.value(1)
            time.sleep_us(1)
            self.hx711clk.value(0)
            time.sleep_us(1)
