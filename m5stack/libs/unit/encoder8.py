# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time


class ENCODER8Unit:
    """
    note:
        en: UNIT 8Encoder is a set of 8 rotary encoders as one of the input unit, the internal use of STM32 single-chip microcomputer as the acquisition and communication processor, and the host computer using I2C communication interface, each rotary encoder corresponds to 1 RGB LED light, encoder in addition to left and right rotation, but also radially pressed, in addition to a physical toggle switch and its corresponding RGB LED light, including 5V->3V3 DCDC circuit.

    details:
        link: https://docs.m5stack.com/en/unit/8Encoder
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/8Encoder/img-f745fc18-6237-4bc8-8500-6c91ce7e2d75.webp
        category: Unit

    example:
        - ../../../examples/unit/encoder8/encoder8_cores3_example.py

    m5f2:
        - unit/encoder8/encoder8_cores3_example.m5f2
    """

    _ENCODER8_ADDR = 0x41

    _ENCODER_CNT_START_REG = 0x00
    _ENCODER_CNT_END_REG = 0x1F
    _ENCODER_INC_START_REG = 0x20
    _ENCODER_INC_END_REG = 0x3F
    _ENCODER_CNT_RST_START_REG = 0x40
    _ENCODER_CNT_RST_END_REG = 0x47
    _ENCODER_BUTTON_START_REG = 0x50
    _ENCODER_BUTTON_END_REG = 0x57
    _ENCODER_SWITCH_REG = 0x60
    _ENCODER_RGB_START_REG = 0x70
    _ENCODER_RGB_END_REG = 0x8A
    _ENCODER_FW_VER_REG = 0xFE
    _ENCODER_I2C_ADDR_REG = 0xFF
    _ENCODER_TOTAL_LED = 9

    def __init__(
        self,
        i2c: I2C | PAHUBUnit,
        slave_addr: int = _ENCODER8_ADDR,
        address: int | list | tuple = 0x41,
    ) -> None:
        """
        note:
            en: Initialize the Encoder8 Unit with the specified I2C interface and address.

        params:
            i2c:
                note: The I2C interface or PAHUBUnit instance for communication.
            slave_addr:
                note: Deprecated parameter, kept for backward compatibility.
            address:
                note: The I2C address of the Encoder8 Unit. Default is 0x41.
        """
        address = slave_addr
        self.encoder8_i2c = i2c
        self.init_i2c_address(address)

    def init_i2c_address(self, slave_addr: int = _ENCODER8_ADDR) -> None:
        """
        note:
            en: Set or change the I2C address of the Encoder8 Unit.

        params:
            slave_addr:
                note: The new I2C address to set. Range: 1 to 127.
        """
        if slave_addr >= 1 and slave_addr <= 127:
            self.i2c_addr = slave_addr
        self.available()

    def available(self) -> None:
        """
        note:
            en: Check if the Encoder8 Unit is connected on the I2C bus.

        params:
            note:
        """
        if self.i2c_addr in self.encoder8_i2c.scan():
            pass
        else:
            raise UnitError("Encoder 8 unit maybe not connect")

    def get_counter_value(self, channel: int = 1) -> int:
        """
        note:
            en: Get the current counter value of the specified channel.

        params:
            channel:
                note: The encoder channel (1-8). Default is 1.

        returns:
            note: The current counter value as an integer.
        """
        channel = min(8, max(channel, 1)) - 1
        channel *= 4
        if not (channel >= self._ENCODER_CNT_START_REG and channel <= self._ENCODER_CNT_END_REG):
            channel = self._ENCODER_CNT_START_REG
        buf = self.read_reg_data(channel, 4)
        return struct.unpack("<i", buf)[0]

    def set_counter_value(self, channel: int = 1, value: int = 0) -> None:
        """
        note:
            en: Set the counter value for the specified channel.

        params:
            channel:
                note: The encoder channel (1-8). Default is 1.
            value:
                note: The counter value to set.
        """
        channel = min(8, max(channel, 1)) - 1
        channel *= 4
        if not (channel >= self._ENCODER_CNT_START_REG and channel <= self._ENCODER_CNT_END_REG):
            channel = self._ENCODER_CNT_START_REG
        self.write_reg_data(channel, struct.pack("<i", value))

    def get_increment_value(self, channel: int = 1) -> int:
        """
        note:
            en: Get the incremental value of the specified channel.

        params:
            channel:
                note: The encoder channel (1-8). Default is 1.

        returns:
            note: The incremental value as an integer.
        """
        channel = min(8, max(channel, 1)) - 1
        channel = self._ENCODER_INC_START_REG + (channel * 4)
        if not (channel >= self._ENCODER_INC_START_REG and channel <= self._ENCODER_INC_END_REG):
            channel = self._ENCODER_INC_START_REG
        buf = self.read_reg_data(channel, 4)
        return struct.unpack("<i", buf)[0]

    def reset_counter_value(self, channel: int = 1) -> None:
        """
        note:
            en: Reset the counter value for the specified channel.

        params:
            channel:
                note: The encoder channel (1-8). Default is 1.
        """
        channel = min(8, max(channel, 1)) - 1
        channel += self._ENCODER_CNT_RST_START_REG
        if not (
            channel >= self._ENCODER_CNT_RST_START_REG and channel <= self._ENCODER_CNT_RST_END_REG
        ):
            channel = self._ENCODER_CNT_RST_START_REG
        self.write_reg_data(channel, [0x01])

    def get_button_status(self, channel: int = 1) -> bool:
        """
        note:
            en: Get the button status for the specified channel.

        params:
            channel:
                note: The encoder channel (1-8). Default is 1.

        returns:
            note: True if the button is pressed, False otherwise.
        """
        channel = min(8, max(channel, 1)) - 1
        channel += self._ENCODER_BUTTON_START_REG
        if not (
            channel >= self._ENCODER_BUTTON_START_REG and channel <= self._ENCODER_BUTTON_END_REG
        ):
            channel = self._ENCODER_BUTTON_START_REG
        return self.read_reg_data(channel, 1)[0] == 0

    def get_switch_status(self) -> bool:
        """
        note:
            en: Get the status of the global switch.

        params:
            note:

        returns:
            note: True if the switch is on, False otherwise.
        """
        return bool(self.read_reg_data(self._ENCODER_SWITCH_REG, 1)[0])

    def set_led_rgb(self, channel: int = 1, rgb: int = 0) -> None:
        """
        note:
            en: Set the RGB color of the specified channel's LED.

        params:
            channel:
                note: The encoder channel (1-8). Default is 1.
            rgb:
                note: The RGB color value (0-0xFFFFFF). Default is 0.
        """
        channel = min(8, max(channel, 1)) - 1
        channel = self._ENCODER_RGB_START_REG + (channel * 3)
        if not (channel >= self._ENCODER_RGB_START_REG and channel <= self._ENCODER_RGB_END_REG):
            channel = self._ENCODER_RGB_START_REG
        self.write_reg_data(channel, rgb.to_bytes(3, "big"))

    def set_led_rgb_from(self, begin: int = 0, end: int = 0, rgb: int = 0) -> None:
        """
        note:
            en: Set the RGB color for a range of channels' LEDs.

        params:
            begin:
                note: The starting channel index. Default is 0.
            end:
                note: The ending channel index. Default is 0.
            rgb:
                note: The RGB color value (0-0xFFFFFF). Default is 0.
        """
        begin = min(self._ENCODER_TOTAL_LED, max(begin, 0))
        end = min(self._ENCODER_TOTAL_LED, max(end, 0))
        for i in range(begin, end + 1):
            self.set_led_rgb(i, rgb)

    def get_device_status(self, mode: int = 0xFE) -> int:
        """
        note:
            en: Get the device firmware version or I2C address.

        params:
            mode:
                note: The mode to read. 0xFE for firmware version, 0xFF for I2C address. Default is 0xFE.

        returns:
            note: The value read from the specified mode register.
        """
        if mode >= self._ENCODER_FW_VER_REG and mode <= self._ENCODER_I2C_ADDR_REG:
            return self.read_reg_data(mode, 1)[0]

    def set_i2c_address(self, addr: int = 0x41) -> None:
        """
        note:
            en: Set a new I2C address for the device.

        params:
            addr:
                note: The new I2C address. Default is 0x41.
        """
        if addr >= 0x08 and addr <= 0x77:
            if addr != self.i2c_addr:
                self.write_reg_data(self._ENCODER_I2C_ADDR_REG, [addr])
                self.i2c_addr = addr
                time.sleep_ms(50)

    def read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        """
        note:
            en: Read data from a specified register.

        params:
            reg:
                note: The register address to read from.
            num:
                note: The number of bytes to read.

        returns:
            note: The requested value as an integer.
        """
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.encoder8_i2c.writeto(self.i2c_addr, buf)
        buf = bytearray(num)
        self.encoder8_i2c.readfrom_into(self.i2c_addr, buf)
        return buf

    def write_reg_data(self, reg, byte_lst):
        """
        note:
            en: Write data to a specified register.

        params:
            reg:
                note: The register address to write to.
            byte_lst:
                note: A list of bytes to write to the register.
        """
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self.encoder8_i2c.writeto(self.i2c_addr, buf)

    def deinit(self):
        """
        note:
            en: Deinitialize the Encoder8 Unit instance.

        params:
            note:
        """
        pass


class Encoder8Unit(ENCODER8Unit):
    def __init__(
        self, i2c: I2C | PAHUBUnit, address: int | list | tuple = ENCODER8Unit._ENCODER8_ADDR
    ) -> None:
        super().__init__(i2c, slave_addr=address)
