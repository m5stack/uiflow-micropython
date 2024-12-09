# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import struct

ANGLE8_ADDR = 0x43

ADC12_START_REG = 0x00
ADC12_END_REG = 0x0F
ADC8_START_REG = 0x10
ADC8_END_REG = 0x17
BUTTON_REG = 0x20
RGB_START_REG = 0x30
RGB_END_REG = 0x53
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF

TOTAL_LED = 9


class Angle8Unit:
    """
    note:
        en: UNIT 8Angle is an input unit integrating 8 adjustable potentiometers, internal STM32F030 microcomputer as acquisition and communication processor, and the host computer adopts I2C communication interface, each adjustable potentiometer corresponds to 1 RGB LED light, and there is also a physical toggle switch and its corresponding RGB LED light, containing 5V->3V3 DCDC circuit.

    details:
        link: https://docs.m5stack.com/en/unit/8Angle
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/8Angle/img-b698604d-29dd-4506-b662-4752e1f03a28.webp
        category: Unit

    example:
        - ../../../examples/unit/angle8unit/angle8unit_cores3_example.py

    m5f2:
        - unit/angle8unit/angle8unit_cores3_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = ANGLE8_ADDR) -> None:
        """
        note:
            en: Initialize the Angle8Unit with the specified I2C interface and address.

        params:
            i2c:
                note: The I2C or PAHUBUnit instance for communication.
            address:
                note: The I2C address of the device (default is ANGLE8_ADDR).
        """
        self._i2c = i2c
        if address >= 1 and address <= 127:
            self._i2c_addr = address
        self.available()

    def available(self) -> None:
        """
        note:
            en: Check if the device is available on the I2C bus.

        params:
            note:
        """
        if self._i2c_addr not in self._i2c.scan():
            raise UnitError("Angle 8 unit maybe not connect")

    def get_adc12_raw(self, channel: int = 0) -> int:
        """
        note:
            en: Get the raw 12-bit ADC value from the specified channel.

        params:
            channel:
                note: The channel number (1 to 8).
        """
        channel -= 1
        if not ((channel * 2) >= ADC12_START_REG and (channel * 2) <= ADC12_END_REG):
            channel = ADC12_START_REG
        buf = self.readfrommem((ADC12_START_REG + (channel * 2)), 2)
        return struct.unpack("<h", buf)[0]

    def get_adc8_raw(self, channel: int = 0) -> int:
        """
        note:
            en: Get the raw 8-bit ADC value from the specified channel.

        params:
            channel:
                note: The channel number (1 to 8).
        """
        channel -= 1
        channel += ADC8_START_REG
        if not (channel >= ADC8_START_REG and channel <= ADC8_END_REG):
            channel = ADC8_START_REG
        return self.readfrommem(channel, 1)[0]

    def get_switch_status(self) -> bool:
        """
        note:
            en: Get the status of the switch button.

        params:
            note:
        """
        return bool(self.readfrommem(BUTTON_REG, 1)[0])

    def set_led_rgb(self, channel: int, rgb: int, bright: int = 50) -> None:
        """
        note:
            en: Set the RGB color and brightness of the specified LED channel.

        params:
            channel:
                note: The LED channel number (0 to 8).
            rgb:
                note: The RGB color value (0x00 to 0xFFFFFF).
            bright:
                note: The brightness level (0 to 100, default is 50).
        """
        channel -= 1
        channel = RGB_START_REG + (channel * 4)
        if not (channel >= RGB_START_REG and channel <= RGB_END_REG):
            channel = RGB_START_REG
        r = (rgb & 0xFF0000) >> 16
        g = (rgb & 0x00FF00) >> 8
        b = rgb & 0xFF
        time.sleep_ms(2)
        self._i2c.writeto_mem(self._i2c_addr, channel, bytearray([r, g, b, bright]))

    def set_led_rgb_from(
        self, begin: int, end: int, rgb: int, bright: int = 50, per_delay: int = 0
    ) -> None:
        """
        note:
            en: Set the RGB color and brightness for a range of LED channels.

        params:
            begin:
                note: The starting LED channel (0 to 8).
            end:
                note: The ending LED channel (0 to 8).
            rgb:
                note: The RGB color value (0x00 to 0xFFFFFF).
            bright:
                note: The brightness level (0 to 100, default is 50).
            per_delay:
                note: The delay in milliseconds between setting each channel (default is 0).
        """
        begin = min(TOTAL_LED, max(begin, 1))
        end = min(TOTAL_LED, max(end, 1))
        if begin > end:
            begin, end = end, begin
        for i in range(begin, end + 1):
            self.set_led_rgb(i, rgb, bright)
            time.sleep_ms(per_delay)

    def set_angle_sync_bright(self, channel: int, rgb: int) -> None:
        """
        note:
            en: Set the LED brightness synchronized with the angle value.

        params:
            channel:
                note: The LED channel number (0 to 8).
            rgb:
                note: The RGB color value (0x00 to 0xFFFFFF).
        """
        bright = self._map(self.get_adc12_raw(channel), 0, 4095, 0, 100)
        self.set_led_rgb(channel, rgb, bright)

    def get_device_spec(self, mode: int) -> int:
        """
        note:
            en: Get device specifications such as firmware version or I2C address.

        params:
            mode:
                note: The register to read (FW_VER_REG or I2C_ADDR_REG).
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.readfrommem(mode, 1)[0]

    def set_i2c_address(self, address: int) -> None:
        """
        note:
            en: Set a new I2C address for the device.

        params:
            address:
                note: The new I2C address (1 to 127).
        """
        if address >= 1 and address <= 127:
            if address != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, I2C_ADDR_REG, bytearray([address]))
                self._i2c_addr = address
                time.sleep_ms(200)

    def readfrommem(self, reg, num) -> bytearray:
        """
        note:
            en: Read a specified number of bytes from a device register.

        params:
            reg:
                note: The register address to read from.
            num:
                note: The number of bytes to read.
        """
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self._i2c.writeto(self._i2c_addr, buf)
        buf = bytearray(num)
        self._i2c.readfrom_into(self._i2c_addr, buf)
        return buf

    def _convert_12_to_24(self, val: int) -> int:
        """
        note:
            en: Convert a 12-bit RGB value to a 24-bit RGB value.

        params:
            val:
                note: The 12-bit RGB value to convert.
        """
        red = (val >> 8) * 17
        green = ((val & 0xF0) >> 4) * 17
        blue = (val & 0x0F) * 17
        return red << 16 | green << 8 | blue

    def _map(self, val, in_min, in_max, out_min, out_max) -> int:
        """
        note:
            en: Map a value from one range to another.

        params:
            val:
                note: The input value to map.
            in_min:
                note: The minimum value of the input range.
            in_max:
                note: The maximum value of the input range.
            out_min:
                note: The minimum value of the output range.
            out_max:
                note: The maximum value of the output range.
        """
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
