# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from micropython import const
from driver.scd40 import SCD40


CO2_I2C_ADDR = const(0x62)


class CO2Unit(SCD40):
    def __init__(self, i2c: I2C | PAHUBUnit, address: int = CO2_I2C_ADDR) -> None:
        super().__init__(i2c, address)
