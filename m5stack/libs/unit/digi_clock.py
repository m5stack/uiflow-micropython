# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   digi_clock.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import I2C
import struct
import time


class DigiClockUnit:
    """! UNIT-Digi-Clock is a 2.1 inch 4-digit 7-segment display module.

    @en UNIT-Digi-Clock is a 2.1 inch 4-digit 7-segment display module. There are decimal points on each digit and an extra wire for colon-dots in the center, which can display Decimals and Clock. This module adopts TM1637 as the driver IC, and STM32F030 as I2C communication. I2C address can be modified per 4-bit dip switch. The red LED supports 8 brightness. And we have reserved 4 fixing holes there.
    @cn UNIT-Digi-Clock是一个2.1英寸4位7段数码管显示模块。 每个数字上都有小数点，中间有一个额外的冒号点的线，可以显示小数点和时钟。 该模块采用TM1637作为驱动IC，STM32F030作为I2C通信。 I2C地址可以根据4位拨码开关进行修改。 红色LED支持8级亮度。 我们在那里预留了4个固定孔。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/digi_clock
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/digi_clock/digi_clock_01.webp
    @category unit

    @example
        import time
        from hardware import *
        from unit import DigiClockUnit
        i2c = I2C(1, scl=33, sda=32)
        digi_clock = DigiClockUnit(i2c)
        digi_clock.set_string("00:00")
        digi_clock.set_brightness(8)


    """

    SEGMENTS_BASE_REG = 0x00
    ASCII_BASE_REG = 0x10
    STRING_BASE_REG = 0x20
    BRIGHTNESS_BASE_REG = 0x30
    FW_VER_REG = 0xFE

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x30) -> None:
        """! Initialize the DigiClockUnit.

        @param i2c I2C port to use.
        @param address I2C address of the DigiClockUnit.
        """
        self.i2c = i2c
        self.addr = address
        self._available()

    def _available(self) -> None:
        """! Check if DigiClockUnit is available on the I2C bus.

        Raises:
            Exception: If the DigiClockUnit is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("DigiClockUnit not found on I2C bus.")

    def clear(self) -> None:
        """! Clear the display.

        @en %1 Clear the display.
        @cn %1 清除显示。

        """
        self.i2c.writeto_mem(self.addr, self.SEGMENTS_BASE_REG, bytes([0x00] * 6))

    def set_brightness(self, brightness: int) -> None:
        """! Set the brightness of the display.

        @en %1 Set the brightness of the display to %2.
        @cn %1 将显示的亮度设置为%2。

        @param brightness The brightness of the display, range from 0 to 8.
        """
        brightness = brightness % 9
        self.i2c.writeto_mem(self.addr, self.BRIGHTNESS_BASE_REG, struct.pack("B", brightness))

    def set_raw(self, data: int, index: int) -> None:
        """! Write raw data to the display.

        @en %1 Write raw data %2 to the %3th digit.
        @cn %1 将原始数据%2写入到第%3位。

        @param data The data to write.
        @param index The index of the data, range from 0 to 4.
        """
        index = index % 5
        self.i2c.writeto_mem(self.addr, self.SEGMENTS_BASE_REG + index, struct.pack("B", data))

    def set_char(self, char: str, index: int) -> None:
        """! Write a character to the display.

        @en %1 Write character %2 to the %3th digit.
        @cn %1 将字符%2写入到第%3位。

        @param char The character to write.
        @param index The index of the character, range from 0 to 4.
        """
        index = index % 5
        char_code = ord(char[0])
        self.i2c.writeto_mem(self.addr, self.ASCII_BASE_REG + index, struct.pack("B", char_code))

    def set_string(self, string: str) -> None:
        """! Write a string to the display.

        @en %1 Set string %2 to the display.
        @cn %1 设置字符串%2。

        @param string The string to write.
        """
        string = string[:9]
        self._write_reg_data(self.STRING_BASE_REG, string.encode())

    def get_fw_version(self) -> int:
        """! Get the firmware version of the DigiClockUnit.

        @en %1 Get the firmware version of the DigiClockUnit.
        @cn %1 获取DigiClockUnit的固件版本。
        @return: The firmware version.
        """
        return self._read_reg_data(self.FW_VER_REG, 1)[0]

    def _read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
        buf = bytearray(num)
        self.i2c.readfrom_into(self.addr, buf)
        return buf

    def _write_reg_data(self, reg, byte_lst):
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
