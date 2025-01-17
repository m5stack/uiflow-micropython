# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.neopixel.ws2812 import WS2812
from hardware import Button
import random
import time
import struct


class NECOUnit(WS2812, Button):
    """
    note:
        en: The Neco Unit is a unique RGB light board unit that features an adorable cat ear shape. It is designed with precision and comprises 35 WS2812C-2020 RGB lamp beads, providing vibrant and customizable lighting effects.

    details:
        link: https://docs.m5stack.com/en/unit/Neco%20Unit
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/Neco%20Unit/img-bb90b98e-1718-4a9d-8e36-afebfa1ee7d3.webp
        category: Unit

    example:
        - ../../../examples/unit/neco/neco_cores3_example.py

    m5f2:
        - unit/neco/neco_cores3_example.m5f2
    """

    def __init__(self, port: tuple, number: int = 70, active_low: bool = True) -> None:
        """
        note:
            en: Initialize the NECOUnit with a specific port, LED count, and active low configuration for the button.

        params:
            port:
                note: A tuple containing the port information, where the first element is for the button and the second is for the WS2812 LEDs.
            number:
                note: The number of LEDs in the WS2812 strip. Default is 70.
            active_low:
                note: Boolean flag indicating whether the button is active low. Default is True.
        """
        WS2812.__init__(self, port[1], number)
        Button.__init__(self, port[0], active_low=active_low)
        self.total_led = number

    def set_color_from(self, begin: int, end: int, rgb: int, per_delay: int = 0) -> None:
        """
        note:
            en: Set the color for a range of LEDs from the begin index to the end index with a specified color.

        params:
            begin:
                note: The starting LED index.
            end:
                note: The ending LED index.
            rgb:
                note: The color to set, in RGB format.
            per_delay:
                note: The delay between setting each LED's color, in milliseconds. Default is 0.
        """
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        for i in range(begin, end + 1):
            self.set_color(i, rgb)
            time.sleep_ms(per_delay)

    def set_color_saturation_from(
        self, begin: int, end: int, rgb: int, per_delay: int = 0
    ) -> None:
        """
        note:
            en: Set the color saturation for a range of LEDs from the begin index to the end index with a specified color and saturation.

        params:
            begin:
                note: The starting LED index.
            end:
                note: The ending LED index.
            rgb:
                note: The base color in RGB format.
            per_delay:
                note: The delay between setting each LED's color, in milliseconds. Default is 0.
        """
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        bright = int(100 / (end - begin))
        for i in range(begin, end + 1):
            self.set_color(i, self.color_saturation(rgb, (100 - ((i - begin) * bright))))
            time.sleep_ms(per_delay)

    def color_saturation(self, rgb: int, saturation: float):
        """
        note:
            en: Adjust the color saturation of an RGB color.

        params:
            rgb:
                note: The base color in RGB format.
            saturation:
                note: The desired saturation level (0 to 100).

        returns:
            note: The new color with adjusted saturation, in RGB format.
        """
        saturation = saturation / 100
        r = int(((rgb & 0xFF0000) >> 16) * saturation)
        g = int(((rgb & 0x00FF00) >> 8) * saturation)
        b = int((rgb & 0xFF) * saturation)
        buf = struct.pack("bbbb", b, g, r, 0x00)
        return struct.unpack("i", buf)[0]

    def set_color_running_from(self, begin: int, end: int, rgb: int, per_delay: int = 0) -> None:
        """
        note:
            en: Set the color for a range of LEDs from the begin index to the end index, then clear them one by one,
                 creating a running effect.

        params:
            begin:
                note: The starting LED index.
            end:
                note: The ending LED index.
            rgb:
                note: The color to set, in RGB format.
            per_delay:
                note: The delay between setting and clearing each LED's color, in milliseconds. Default is 0.
        """
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        for i in range(begin, end + 1):
            self.set_color(i, rgb)
            time.sleep_ms(per_delay)
            self.set_color(i, 0x00)

    def set_random_color_random_led_from(self, begin: int, end: int) -> None:
        """
        note:
            en: Set a random color to each LED in a random order within the specified range.

        params:
            begin:
                note: The starting LED index.
            end:
                note: The ending LED index.
        """
        begin = min(self.total_led - 1, max(begin, 0))
        end = min(self.total_led - 1, max(end, 0))
        begin, end = (begin, end) if begin < end else (end, begin)
        for i in range(begin, end + 1):
            color_in = random.randint(0, 0xFFFFFF)
            self.set_color(i, color_in)
