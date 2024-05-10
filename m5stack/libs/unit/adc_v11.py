# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.ads1110 import ADS1110
from micropython import const
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time


class AdcV11Unit(ADS1110):
    def __init__(self, i2c: I2C | PAHUBUnit) -> None:
        super().__init__(i2c=i2c)
        self._available()
        self.divider_offset = 100 / 610

    def _available(self):
        check = False
        for i in range(3):
            if self._i2c_addr in self._i2c.scan():
                check = True
                break
            time.sleep(0.2)
        if not check:
            raise UnitError("ADC V1.1 Unit not found in Grove")

    def get_voltage(self):
        data = self.get_adc_raw_value
        vol = (
            data
            * 2.048
            / 2 ** (self.mini_code[self.rate] - 1)
            / self.gain_code[self.gain]
            / self.divider_offset
        )
        return round(vol, 2)
