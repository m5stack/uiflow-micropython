# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.sgp30 import SGP30
from .pahub import PAHUBUnit
from .unit_helper import UnitError


SGP30_I2C_ADDR = 0x58


class TVOCUnit(SGP30):
    def __init__(self, i2c: I2C | PAHUBUnit, address: int = SGP30_I2C_ADDR) -> None:
        """! initialize Function
        set I2C Pins, SGP30 Address
        """
        self._i2c = i2c
        self._i2c_addr = address
        self.available()
        super().__init__(i2c=i2c, addr=address)

    def available(self) -> None:
        """! Is there available or Not? Check."""
        if self._i2c_addr not in self._i2c.scan():
            raise UnitError("TVOC/eCO2 unit not found in Grove")

    def set_baseline_co2_tvoc(self, co2eq, tvoc):
        self.set_iaq_baseline(co2eq, tvoc)

    def set_relative_humidity(self, humidity_per, temp_c):
        abs_humi = self.convert_r_to_a_humidity(temp_c, humidity_per)
        self.set_absolute_humidity(abs_humi)
