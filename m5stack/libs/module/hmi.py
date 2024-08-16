# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
import struct
import time


class HMIModule:
    """! HMI Module is a human-computer interactive module.

    @en Module HMI 英文介绍
    @cn Module HMI 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/HMI%20Module
    @image https://static-cdn.m5stack.com/resource/docs/products/module/HMI%20Module/img-4c227abf-0a4c-4e3a-b711-b81a35899aaf.webp
    @category module

    """

    _HMI_ADDR = 0x41

    _HMI_ENCODER_REG = 0x00
    _HMI_INCREMENT_REG = 0x10
    _HMI_BUTTON_REG = 0x20
    _HMI_LED_REG = 0x30
    _HMI_RESET_COUNTER_REG = 0x40
    _HMI_FIRMWARE_VERSION_REG = 0xFE
    _HMI_I2C_ADDRESS_REG = 0xFF

    def __init__(self, address: int | list | tuple = _HMI_ADDR) -> None:
        """! Init I2C Module HMI I2C Address.

        @param address I2C address of the HMIModule.
        """
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("HMI Module not found in Base")

    def get_rotary_value(self) -> int:
        """! Get the current value of the rotary.

        @return: The value of the rotary.
        """
        buf = self._i2c.readfrom_mem(self._i2c_addr, self._HMI_ENCODER_REG, 4)
        return struct.unpack("<i", buf)[0]

    def set_rotary_value(self, value: int) -> None:
        """! Set the rotary value.

        @param value: rotary value(-2147483648-2147483647).
        """
        byte_data = [value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]

        self._i2c.writeto_mem(self._i2c_addr, self._HMI_ENCODER_REG, bytes(byte_data))

    def reset_rotary_value(self) -> None:
        """! Reset the rotary value."""
        self._i2c.writeto_mem(self._i2c_addr, self._HMI_RESET_COUNTER_REG, bytes([1]))

    def get_rotary_increments(self) -> int:
        """! Get the increment value of the rotary.

        @return: The increment value of the rotary.
        """
        buf = self._i2c.readfrom_mem(self._i2c_addr, self._HMI_INCREMENT_REG, 4)
        return struct.unpack("<i", buf)[0]

    def get_button_status(self, btn_num: int) -> int:
        """! Get the state of a specific button.

        @param btn_num: Button number (1 to 3).
        @return: The state of the button.
        """
        if not (1 <= btn_num <= 3):
            raise ValueError("Btn select error")
        reg = self._HMI_BUTTON_REG + btn_num - 1
        buf = self._i2c.readfrom_mem(self._i2c_addr, reg, 1)
        return 0 if struct.unpack("<b", buf)[0] else 1

    def get_led_state(self, led_num: int) -> int:
        """! Get the state of a specific LED.

        @param led_num: LED number (1 to 2).
        @return: The state of the LED.
        """
        if not (1 <= led_num <= 2):
            raise ValueError("LED select error")
        reg = self._HMI_LED_REG + led_num - 1
        buf = self._i2c.readfrom_mem(self._i2c_addr, reg, 1)
        return struct.unpack("<b", buf)[0]

    def set_led_state(self, led_num: int, state: int) -> None:
        """! Set the state of a specific LED.

        @param led_num: LED number (1 to 2).
        @param state: The state to set for the LED.
        """
        if not (1 <= led_num <= 2):
            raise ValueError("LED select error")
        reg = self._HMI_LED_REG + led_num - 1
        self._i2c.writeto_mem(self._i2c_addr, reg, bytes([state]))

    def get_firmware_version(self) -> int:
        """! Get the firmware version of the HMI module.

        @return: The firmware version number.
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._HMI_FIRMWARE_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> int:
        """! Get the current I2C address of the HMI module.

        @return: The I2C address as a hex string.
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._HMI_I2C_ADDRESS_REG, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """! Set a new I2C address for the HMI module.
        @param addr: The new I2C address to set.
        """
        if addr >= 0x01 and addr <= 0x7F:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, self._HMI_I2C_ADDRESS_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x01~0x7f")
