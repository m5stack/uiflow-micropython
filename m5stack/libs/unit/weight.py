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
    """
    note:
        en: WEIGHT integrates a HX711 24 bits A/D chip that is specifically designed for electronic weighing device.

    details:
        link: https://docs.m5stack.com/en/unit/WEIGHT
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/WEIGHT/img-a0113c8c-ed62-43b9-ad38-5cb934811d9e.webp
        category: Unit

    example:
        - ../../../examples/unit/weight/weight_cores3_example.py

    m5f2:
        - unit/weight/weight_cores3_example.m5f2
    """

    def __init__(self, port) -> None:
        """
        note:
            en: Initialize the WEIGHTUnit with specified port pins.

        params:
            port:
                note: A tuple containing data and clock pin numbers.
        """
        self.hx711data = Pin(port[0], Pin.IN)
        self.hx711clk = Pin(port[1], Pin.OUT)
        self.zero_value = 0
        self.hx711clk.value(0)
        self._channel = 1
        self._scale = 1.0

    @property
    def get_raw_weight(self) -> int:
        """
        note:
            en: Read the raw weight value from the HX711.

        params:
            note:

        returns:
            note: The raw weight value as an integer.
        """
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
        """
        note:
            en: Get the scaled weight value based on calibration.

        params:
            note:

        returns:
            note: The scaled weight value as an integer.
        """
        return int((self.get_raw_weight - self.zero_value) * self._scale)

    def set_tare(self) -> None:
        """
        note:
            en: Set the tare weight to zero out the scale.

        params:
            note:
        """
        self.zero_value = self.get_raw_weight

    def set_calibrate_scale(self, weight):
        """
        note:
            en: Calibrate the scale with a known weight.

        params:
            weight:
                note: The known weight used for calibration.
        """
        self._scale = (1.0 * weight) / (self.get_raw_weight - self.zero_value)

    def is_ready_wait(self) -> bool:
        """
        note:
            en: Check if the HX711 is ready to provide data.

        params:
            note:

        returns:
            note: True if the HX711 is ready, False otherwise.
        """
        times = 0
        while self.hx711data.value():
            times += 1
            time.sleep_ms(10)
            if times > 25:
                break
        return not self.hx711data.value()

    def set_channel(self, chan: int) -> None:
        """
        note:
            en: Set the channel for the HX711.

        params:
            chan:
                note: The channel to set (1, 2, or 3).
        """
        self._channel = chan
        for i in range(self._channel):
            self.hx711clk.value(1)
            time.sleep_us(1)
            self.hx711clk.value(0)
            time.sleep_us(1)


class WeightUnit(WEIGHTUnit):
    def __init__(self, port) -> None:
        super().__init__(port)
