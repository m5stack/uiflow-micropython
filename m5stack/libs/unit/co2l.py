# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from driver.scd40 import SCD40

CO2L_I2C_ADDR = 0x62


class CO2LUnit(SCD40):
    def __init__(self, i2c: I2C | PAHUBUnit, address: int = CO2L_I2C_ADDR) -> None:
        super().__init__(i2c=i2c, address=address)
