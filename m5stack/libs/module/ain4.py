# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
import struct
import time


class AIN4Module:
    """! Module AIN4 is a Slide Potentiometer with color indicator.

    @en Module AIN4 英文介绍
    @cn Module AIN4 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/AIN4-20mA%20Module%2013.2
    @image https://static-cdn.m5stack.com/resource/docs/products/module/AIN4-20mA%20Module%2013.2/img-ddec758e-78ce-43e8-9af7-bc101f3dc175.webp
    @category module

    @example

    """

    _AIN_ADDR = 0x55

    _AIN_ADC_RAW_REG = 0x00
    _AIN_CURRENT_REG = 0x20
    _AIN_CAL_REG = 0x30
    _AIN_FW_VERSION_REG = 0xFE
    _AIN_I2C_ADDR_REG = 0xFF

    def __init__(self, address: int | list | tuple = _AIN_ADDR) -> None:
        """! Init I2C Module AIN 4-20mA I2C Address.

        @param i2c I2C port to use.
        @param address I2C address of the AIN4Module.
        """
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("AIN 4-20mA Module not found in Base")

    def get_adc_raw_value(self, channel: int = 1) -> int:
        """! Get ADC raw value (12-bit).

        Retrieves the raw ADC value from the specified channel.

        @param channel: The channel number (1 to 4) to read the ADC value from.
        @return The 12-bit raw ADC value.

        @raise ValueError: If the channel is not in the range 1 to 4.
        """
        if not (1 <= channel <= 4):
            raise ValueError("Channel selection error")
        reg = self._AIN_ADC_RAW_REG + (channel - 1) * 2
        buf = self._i2c.readfrom_mem(self._i2c_addr, reg, 2)
        return struct.unpack("<H", buf)[0]

    def get_current_value(self, channel: int = 1) -> int:
        """! Get AIN 4-20mA current value.

        Retrieves the current value (in mA) from the specified channel.

        @param channel: The channel number (1 to 4) to read the current value from.
        @return The current value in mA, rounded to two decimal places.

        @raise ValueError: If the channel is not in the range 1 to 4.
        """
        if not (1 <= channel <= 4):
            raise ValueError("Channel selection error")
        reg = self._AIN_CURRENT_REG + (channel - 1) * 2
        buf = self._i2c.readfrom_mem(self._i2c_addr, reg, 2)
        return round((struct.unpack("<H", buf)[0] / 100), 2)

    def set_cal_current(self, channel: int, val: int) -> None:
        """! Set calibration current for a given channel.

        Sets the calibration current for the specified channel.

        @param channel: The channel number (1 to 4) to set the calibration for.
        @param val: The calibration current value, ranging from 4 to 20 mA.

        @raise ValueError: If the channel is not in the range 1 to 4, or if the value is not between 4 and 20 mA.
        """
        if not (1 <= channel <= 4):
            raise ValueError("Channel selection error")
        if not (4 <= val <= 20):
            raise ValueError("Calibration error, range is 4~20mA")
        reg = self._AIN_CAL_REG + (channel - 1) * 2
        cal_val = int(val * 100)
        data = bytes([cal_val & 0xFF, (cal_val >> 8) & 0xFF])
        self._i2c.writeto_mem(self._i2c_addr, reg, data)
        time.sleep_ms(500)

    def get_firmware_version(self) -> int:
        """! Get firmware version.

        Retrieves the firmware version of the AIN 4-20mA module.

        @return The firmware version as an integer.
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._AIN_FW_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> int:
        """! Get I2C address.

        Retrieves the current I2C address of the AIN 4-20mA module.

        @return The I2C address in hexadecimal format.
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._AIN_I2C_ADDR_REG, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """! Set I2C address.

        Sets a new I2C address for the AIN 4-20mA module.

        @param addr: The new I2C address, must be between 0x08 and 0x78.

        @raise ValueError: If the address is not within the range 0x08 to 0x78.
        """
        if addr >= 0x08 and addr <= 0x78:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, self._AIN_I2C_ADDR_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x78")
