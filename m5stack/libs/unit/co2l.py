# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .co2 import CO2Unit
from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError

CO2_I2C_ADDR = 0x62


class CO2LUnit(CO2Unit):
    def __init__(self, i2c: I2C | PAHUBUnit, address: int = CO2_I2C_ADDR) -> None:
        """! Is there available or Not? Check."""
        if address not in i2c.scan():
            raise UnitError("CO2L unit maybe not connect")
        super().__init__(i2c=i2c, address=address)
