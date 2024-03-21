# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import struct

KMETER_ADDR = 0x66

TEMP_CELSIUS_REG = 0x00
TEMP_FAHREN_REG = 0x04
TEMP_INT_CELSIUS_REG = 0x10
TEMP_INT_FAHREN_REG = 0x14
TEMP_READY_REG = 0x20
TEMP_STR_CELSIUS_REG = 0x30
TEMP_STR_FAHREN_REG = 0x40
TEMP_INTSTR_CELSIUS_REG = 0x50
TEMP_INTSTR_FAHREN_REG = 0x60
FIRM_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class KMETER_ISOUnit:
    def __init__(
        self, i2c: I2C | PAHUBUnit, addr=KMETER_ADDR, address: int | list | tuple = KMETER_ADDR
    ):
        # TODO: 2.0.6 移除 addr 参数
        """! Kmeter Initialize Function
        addr: 1 ~ 127
        """
        address = addr
        self.kmeter_i2c = i2c
        if address >= 0x01 and address <= 0x7F:
            self.unit_addr = address
        if self.unit_addr not in self.kmeter_i2c.scan():
            raise UnitError("Kmeter iso unit maybe not connect")

    def get_kmeter_thermo(self, temp=0):
        """! get thermocouple temperature value."""
        buff = self.kmeter_i2c.readfrom_mem(self.unit_addr, TEMP_CELSIUS_REG + (4 * temp), 4)
        return round((self.int_convert(buff) / 100), 2)

    def get_kmeter_internal(self, temp=0):
        """! get internal temperature value."""
        buff = self.kmeter_i2c.readfrom_mem(self.unit_addr, TEMP_INT_CELSIUS_REG + (4 * temp), 4)
        return round(self.int_convert(buff) / 100, 2)

    @property
    def get_data_available_status(self):
        """! get temperature measurement value is ready?"""
        status = self.kmeter_i2c.readfrom_mem(self.unit_addr, TEMP_READY_REG, 1)[0]
        return False if status else True

    def get_kmeter_thermo_string(self, temp=0):
        """! get thermocouple temperature string value."""
        return self.kmeter_i2c.readfrom_mem(
            self.unit_addr, TEMP_STR_CELSIUS_REG + (temp * 0x10), 1
        ).decode() + str(
            float(
                self.kmeter_i2c.readfrom_mem(
                    self.unit_addr, TEMP_STR_CELSIUS_REG + (temp * 0x10), 8
                ).decode()
            )
        )

    def get_kmeter_internal_string(self, temp=0):
        """! get internal temperature string value."""
        return self.kmeter_i2c.readfrom_mem(
            self.unit_addr, TEMP_INTSTR_CELSIUS_REG + (temp * 0x10), 1
        ).decode() + str(
            float(
                self.kmeter_i2c.readfrom_mem(
                    self.unit_addr, TEMP_INTSTR_CELSIUS_REG + (temp * 0x10), 8
                ).decode()
            )
        )

    def get_device_spec(self, mode) -> int:
        """! Get device firmware version and i2c address.
        mode: 0xFE and 0xFF
        """
        if mode >= FIRM_VER_REG and mode <= I2C_ADDR_REG:
            return self.kmeter_i2c.readfrom_mem(self.unit_addr, mode, 1)[0]

    def set_i2c_address(self, addr) -> None:
        """! Set i2c address.
        addr:  1 to 127
        """
        if addr >= 0x01 and addr <= 0x7F:
            if addr != self.unit_addr:
                self.kmeter_i2c.writeto_mem(self.unit_addr, I2C_ADDR_REG, struct.pack("b", addr))
                self.unit_addr = addr
                time.sleep_ms(200)

    def int_convert(self, value):
        return struct.unpack("<i", value)[0]


class KMeterISOUnit(KMETER_ISOUnit):
    def __init__(self, i2c: I2C | PAHUBUnit, address: int | list | tuple = KMETER_ADDR) -> None:
        super().__init__(i2c, addr=address)
