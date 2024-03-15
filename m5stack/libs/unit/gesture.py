# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from driver.paj7620 import PAJ7620U2
import time
import struct

try:
    from typing import Union
except ImportError:
    pass

RAWDATA = 1
STRING = 2


class GESTUREUnit(PAJ7620U2):
    def __init__(self, i2c: Union[I2C, PAHUBUnit]) -> None:
        self.i2c = i2c
        super(GESTUREUnit, self).__init__(i2c)
        self._available()
        self.begin()

    def _available(self) -> None:
        for i in range(10):
            time.sleep_ms(100)
            if self.i2c_addr in self.i2c.scan():
                break
            if i >= 9:
                raise UnitError("Gesture unit maybe not connect")

    def get_hand_gestures(self):
        return self.get_gesture()
