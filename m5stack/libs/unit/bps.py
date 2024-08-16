# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from driver.bmp280 import BMP280
from driver.qmp6988 import QMP6988


_BMP280_I2C_ADDR = 0x76
_QMP6988_I2C_ADDR = 0x70


class BPSUnit:
    def __init__(self, i2c: I2C | PAHUBUnit, address: int = _BMP280_I2C_ADDR) -> None:
        # Check for the presence of known devices
        try:
            bmp280 = {_BMP280_I2C_ADDR: True, _QMP6988_I2C_ADDR: False}.get(i2c.scan()[0])
            if bmp280 is None:
                raise UnitError("BPS unit maybe not found in Grove")
        except:
            raise UnitError("BPS unit maybe not found in Grove")
        self._bps = BMP280(i2c=i2c) if bmp280 else QMP6988(i2c=i2c)

    def get_temperature(self) -> float:
        return round(self._bps.measure()[0], 2)

    def get_pressure(self) -> float:
        return round((self._bps.measure()[1] / 100), 2)

    def get_altitude(self) -> float:
        return round(44330.0 * (1.0 - (self._bps.measure()[1] / 101325.0) ** (1 / 5.255)), 2)
