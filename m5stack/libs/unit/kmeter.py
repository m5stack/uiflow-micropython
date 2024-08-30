# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from micropython import const
import time
import struct


class KMeterUnit:
    CELSIUS = True
    FAHRENHEIT = False

    _KMETER_ADDR = const(0x66)
    _TEMPERATURE_REG = const(0x00)
    _FIRM_VER_REG = const(0x06)
    _I2C_ADDR_REG = const(0x08)
    _SLEEP_TIME_REG = const(0x0E)
    _WAKEUP_REG = const(0x10)

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = _KMETER_ADDR) -> None:
        #! Kmeter Initialize Function
        #! address : 0x08 to 0x77
        self._i2c = i2c
        self._i2c_addr = address
        if address not in self._i2c.scan():
            raise UnitError("Kmeter unit maybe not found in Grove")

    def get_thermocouple_temperature(self, scale=CELSIUS) -> float:
        #! get thermocouple temperature calculate value.
        buf = self._i2c.readfrom_mem(self._i2c_addr, self._TEMPERATURE_REG, 2)
        self.thermo_couple = (struct.unpack(">h", buf[0:2])[0] >> 2) * 0.25
        return round(self.thermo_couple if scale else ((self.thermo_couple * 9 / 5) + 32), 2)

    def get_internal_temperature(self, scale=CELSIUS) -> float:
        #! get internal temperature calculate value.
        buf = self._i2c.readfrom_mem(self._i2c_addr, self._TEMPERATURE_REG + 2, 2)
        self.internal_temp = (struct.unpack(">h", buf[0:2])[0] >> 4) * 0.0625
        return round(self.internal_temp if scale else ((self.internal_temp * 9 / 5) + 32), 2)

    def get_sleep_time(self) -> int:
        #! get sleep time in seconds.
        return struct.unpack(
            ">H", self._i2c.readfrom_mem(self._i2c_addr, self._SLEEP_TIME_REG, 2)
        )[0]

    def set_sleep_time(self, sleep=0) -> None:
        #! set sleep time in seconds.
        self._i2c.writeto_mem(self._i2c_addr, self._SLEEP_TIME_REG, struct.pack(">H", sleep))

    def set_wakeup_trigger(self, mode=True) -> None:
        #! set wakeup trigger in timer or i2c scl low level.
        self._i2c.writeto_mem(self._i2c_addr, self._WAKEUP_REG, b"\xee" if mode else b"\xef")

    def get_firmware_version(self) -> float:
        #! get firmware version.
        buf = self._i2c.readfrom_mem(self._i2c_addr, self._FIRM_VER_REG, 2)
        return float("{0}.{1}".format(buf[0], buf[1]))

    def get_i2c_address(self) -> int:
        #! get i2c address.
        return self._i2c.readfrom_mem(self._i2c_addr, self._I2C_ADDR_REG, 1)[0]

    def set_i2c_address(self, addr) -> None:
        #! set i2c address.
        if addr >= 0x08 and addr <= 0x77:
            if addr != self._i2c_addr:
                self._i2c.writeto_mem(
                    self._i2c_addr, self._I2C_ADDR_REG, struct.pack("bb", addr, ~(addr))
                )
                self._i2c_addr = addr
                time.sleep_ms(200)
