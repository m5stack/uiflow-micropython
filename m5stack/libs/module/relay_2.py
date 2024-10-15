# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
from .module_helper import ModuleError
import time


class Relay2Module:
    """! Relay2 Module controls two relays.

    @en Module Relay2 英文介绍
    @cn Module Relay2 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/2Relay
    @image https://static-cdn.m5stack.com/resource/docs/products/module/2Relay/img-07c98873-5b75-4c92-ab16-64c890c6166e.webp
    @category module

    """

    _RELAY2_ADDR = 0x25
    _RELAY2_CONTROL_REG = 0x00
    _RELAY2_FIRMWARE_VERSION_REG = 0xFE
    _RELAY2_I2C_ADDR_REG = 0xFF

    def __init__(self, address: int | list | tuple = _RELAY2_ADDR) -> None:
        """! Initialize the 2Relay Module with the specified I2C address.

        @param address: I2C address of the Relay2Module.
        """
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("2 Relay Module not found in Base")

    def set_relay_state(self, num: int, state: bool) -> None:
        """! Set the state of a specific relay.

        @param num: The relay number (1 or 2).
        @param state: True to turn on, False to turn off.
        """
        data = True if state else False
        self._i2c.writeto_mem(self._i2c_addr, self._RELAY2_CONTROL_REG + (num - 1), bytes([data]))

    def get_relay_status(self, num: int) -> int:
        """! Get the status of a specific relay.

        @param num: The relay number (1 or 2).
        @return: The state of the relay (1 for on, 0 for off).
        """
        return bool(self._read_reg_data(self._RELAY2_CONTROL_REG + (num - 1), 1)[0] & 0x01)

    def set_all_relay_state(self, state: bool) -> None:
        """! Set the state of both relays simultaneously.

        @param state: True to turn on both relays, False to turn off both relays.
        """
        data = bytes([1 if state else 0, 1 if state else 0])
        self._i2c.writeto_mem(self._i2c_addr, self._RELAY2_CONTROL_REG, data)

    def get_firmware_version(self) -> int:
        """! Get the firmware version of the Relay2 Module.

        @return: The firmware version number.
        """
        return self._read_reg_data(self._RELAY2_FIRMWARE_VERSION_REG, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """! Set a new I2C address for the Relay2 Module.

        @param addr: The new I2C address to set.
        """
        if 0x08 <= addr <= 0x77:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, self._RELAY2_I2C_ADDR_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x77")

    def get_i2c_address(self) -> int:
        """! Get the current I2C address of the Relay2 Module.

        @return: The I2C address as a hex string.
        """
        return self._read_reg_data(self._RELAY2_I2C_ADDR_REG, 1)[0]

    def _read_reg_data(self, sub_reg: int, num: int) -> bytes:
        """! Helper function to read data from a specific register.

        @param sub_reg: The sub-register to read from.
        @param num: The number of bytes to read.
        @return: The data read from the register.
        """
        self._i2c.writeto(self._i2c_addr, bytes([sub_reg]))
        return self._i2c.readfrom(self._i2c_addr, num)
