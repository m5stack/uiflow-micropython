# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.neopixel.ws2812 import WS2812
from hardware import Button
import random
import time
import struct


class NECOUnit(WS2812, Button):
    def __init__(self, port: tuple, number: int = 70, active_low: bool = True) -> None:
        WS2812.__init__(self, port[1], number)
        Button.__init__(self, port[0], active_low=active_low)
        self.total_led = number

    def set_color_from(self, begin: int, end: int, rgb: int, per_delay: int = 0) -> None:
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        for i in range(begin, end + 1):
            self.set_color(i, rgb)
            time.sleep_ms(per_delay)

    def set_color_saturation_from(
        self, begin: int, end: int, rgb: int, per_delay: int = 0
    ) -> None:
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        bright = int(100 / (end - begin))
        for i in range(begin, end + 1):
            self.set_color(i, self.color_saturation(rgb, (100 - ((i - begin) * bright))))
            time.sleep_ms(per_delay)

    def color_saturation(self, rgb: int, saturation: float):
        saturation = saturation / 100
        r = int(((rgb & 0xFF0000) >> 16) * saturation)
        g = int(((rgb & 0x00FF00) >> 8) * saturation)
        b = int((rgb & 0xFF) * saturation)
        buf = struct.pack("bbbb", b, g, r, 0x00)
        return struct.unpack("i", buf)[0]

    def set_color_running_from(self, begin: int, end: int, rgb: int, per_delay: int = 0) -> None:
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        for i in range(begin, end + 1):
            self.set_color(i, rgb)
            time.sleep_ms(per_delay)
            self.set_color(i, 0x00)

    def set_random_color_random_led_from(self, begin: int, end: int) -> None:
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        for i in range(begin, end + 1):
            color_in = random.randint(0, 0xFFFFFF)
            self.set_color(i, color_in)
