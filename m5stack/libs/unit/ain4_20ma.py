# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from machine import I2C
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time

AIN_ADDR = 0x55

AIN_RAW16_REG = 0x00
AIN_RAW8_REG = 0x10
AIN_CURRENT_REG = 0x20
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class AIN4_20MAUnit:
    def __init__(
        self,
        i2c: I2C | PAHUBUnit,
        address: int | list | tuple = AIN_ADDR,
    ) -> None:
        """! Init I2C port & UNIT AIN 4-20mA I2C Address."""
        self._i2c = i2c
        self._i2c_addr = AIN_ADDR
        if address >= 0x01 and address <= 0x7F:
            self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise UnitError("AIN 4-20mA unit not found in Grove")

    def get_adc_raw16_value(self) -> int:
        """! get adc raw 16bit value."""
        buf = self._i2c.readfrom_mem(self._i2c_addr, AIN_RAW16_REG, 2)
        return struct.unpack("<H", buf)[0]

    def get_adc_raw8_value(self) -> int:
        """! get adc raw 8bit value."""
        return self._i2c.readfrom_mem(self._i2c_addr, AIN_RAW8_REG, 1)[0]

    def get_4_20ma_current_value(self) -> int:
        """! get ain 4-20mA current value."""
        buf = self._i2c.readfrom_mem(self._i2c_addr, AIN_CURRENT_REG, 2)
        return round((struct.unpack("<h", buf)[0] / 100), 2)

    def get_device_spec(self, mode: int) -> int:
        """! get firmware version and i2c address.
        mode: 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self._i2c.readfrom_mem(self._i2c_addr, mode, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """! set i2c address.
        addr: 0x01 to 0x7F
        """
        if addr >= 0x01 and addr <= 0x7F:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, I2C_ADDR_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
