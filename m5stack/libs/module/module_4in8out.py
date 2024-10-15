# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
import struct
import time


class Module4In8Out:
    """! 4In8Out Module is a human-computer interactive module.

    @en Module 4In8Out 英文介绍
    @cn Module 4In8Out 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/4in8out
    @image https://static-cdn.m5stack.com/resource/docs/products/module/4in8out/4in8out_01.webp
    @category module

    """

    _MODULE4IN8OUT_ADDR = 0x45

    _MODULE4IN8OUT_SWTICH_REG = 0x10
    _MODULE4IN8OUT_LOAD_REG = 0x20
    _MODULE4IN8OUT_FIRMWARE_VERSION_REG = 0xFE
    _MODULE4IN8OUT_I2C_ADDRESS_REG = 0xFF

    def __init__(self, address: int | list | tuple = _MODULE4IN8OUT_ADDR) -> None:
        """! Init I2C Module 4In8Out I2C Address.

        @param address I2C address of the 4In8OutModule.
        """
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("4In8Out Module not found in Base")

    def get_switch_value(self, switch_num: int) -> bool:
        """! Get the current value of the rotary.

        @return: The value of the rotary.
        """
        buf = self._read_reg_data(self._MODULE4IN8OUT_SWTICH_REG + switch_num - 1, 1)
        return bool(struct.unpack("<b", buf)[0])

    def get_load_state(self, load_num: int) -> bool:
        """! Get the state of a specific LED.

        @param load_num: Load number (1 to 8).
        @return: The state of the Load.
        """
        buf = self._read_reg_data(self._MODULE4IN8OUT_LOAD_REG + load_num - 1, 1)
        return bool(struct.unpack("<b", buf)[0])

    def set_load_state(self, load_num: int, state: int) -> None:
        """! Set the state of a specific Load.

        @param load_num: Load number (1 to 8).
        @param state: The state to set for the Load.
        """
        reg = self._MODULE4IN8OUT_LOAD_REG + load_num - 1
        self._i2c.writeto_mem(self._i2c_addr, reg, bytes([state]))

    def get_firmware_version(self) -> int:
        """! Get the firmware version of the 4In8Out module.

        @return: The firmware version number.
        """
        return self._read_reg_data(self._MODULE4IN8OUT_FIRMWARE_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> int:
        """! Get the current I2C address of the 4In8Out module.

        @return: The I2C address as a hex string.
        """
        return self._read_reg_data(self._MODULE4IN8OUT_I2C_ADDRESS_REG, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """! Set a new I2C address for the 4In8Out module.
        @param addr: The new I2C address to set.
        """
        if 0x08 <= addr <= 0x78:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(
                    self._i2c_addr, self._MODULE4IN8OUT_I2C_ADDRESS_REG, bytearray([addr])
                )
                self._i2c_addr = addr
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x78")

    def _read_reg_data(self, sub_reg: int, num: int) -> bytes:
        """! Helper function to read data from a specific register.

        @param sub_reg: The sub-register to read from.
        @param num: The number of bytes to read.
        @return: The data read from the register.
        """
        self._i2c.writeto(self._i2c_addr, bytes([sub_reg]))
        return self._i2c.readfrom(self._i2c_addr, num)
