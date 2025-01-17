# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from machine import I2C
from .pahub import PAHUBUnit
import struct
import time


class AIN4_20MAUnit:
    _AIN_ADDR = 0x55
    _AIN_ADC_RAW_REG = 0x00
    _AIN_CURRENT_REG = 0x20
    _AIN_CAL_REG = 0x30
    _AIN_FW_VERSION_REG = 0xFE
    _AIN_I2C_ADDR_REG = 0xFF

    def __init__(
        self,
        i2c: I2C | PAHUBUnit,
        address: int = _AIN_ADDR,
    ) -> None:
        """! Init I2C port & UNIT AIN 4-20mA I2C Address."""
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise Exception("AIN 4-20mA unit not found in Grove")

    def get_adc_raw_value(self) -> int:
        """! Get ADC raw value (12-bit).

        Retrieves the raw ADC value.

        @return The 12-bit raw ADC value.
        """
        buf = self._i2c.readfrom_mem(self._address, self._AIN_ADC_RAW_REG, 2)
        return struct.unpack("<H", buf)[0]

    def get_current_value(self) -> float:
        """! Get AIN 4-20mA current value.

        Retrieves the current value (in mA).

        @return The current value in mA, rounded to two decimal places.
        """
        buf = self._i2c.readfrom_mem(self._address, self._AIN_CURRENT_REG, 2)
        return round((struct.unpack("<H", buf)[0] / 100), 2)

    def set_cal_current(self, val: int) -> None:
        """! Set calibration current for the channel.

        Sets the calibration current for the channel.

        @param val: The calibration current value, ranging from 4 to 20 mA.

        @raise ValueError: If the value is not between 4 and 20 mA.
        """

        if not (4 <= val <= 20):
            raise ValueError("Calibration error, range is 4~20mA")
        cal_val = int(val * 100)
        self._i2c.writeto_mem(self._address, self._AIN_CAL_REG, cal_val.to_bytes(2, "little"))
        time.sleep_ms(500)

    def get_firmware_version(self) -> int:
        """! Get firmware version.

        Retrieves the firmware version of the AIN 4-20mA module.

        @return The firmware version as an integer.
        """
        return self._i2c.readfrom_mem(self._address, self._AIN_FW_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> str:
        """! Get I2C address.

        Retrieves the current I2C address of the AIN 4-20mA unit.

        @return The I2C address in hexadecimal format.
        """
        return hex(self._i2c.readfrom_mem(self._address, self._AIN_I2C_ADDR_REG, 1)[0])

    def set_i2c_address(self, address: int) -> None:
        """! Set I2C address.

        Sets a new I2C address for the AIN 4-20mA unit.

        @param address: The new I2C address, must be between 0x08 and 0x77.

        @raise ValueError: If the address is not within the range 0x08 to 0x77.
        """
        if address >= 0x08 and address <= 0x77:
            if address != self._address:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._address, self._AIN_I2C_ADDR_REG, bytearray([address]))
                self._address = address
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x7f")
