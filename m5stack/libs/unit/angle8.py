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


class ANGLE8Unit:
    def __init__(self, i2c: I2C | PAHUBUnit, address: int = ANGLE8_ADDR) -> None:
        """! angle 8 channel initialize function
        set I2C port
        address : 1 to 127
        """
        self._i2c = i2c
        if address >= 1 and address <= 127:
            self._i2c_addr = address
        self.available()

    def available(self) -> None:
        if self._i2c_addr not in self._i2c.scan():
            raise UnitError("Angle 8 unit maybe not connect")

    def get_adc12_raw(self, channel: int = 0) -> int:
        """! get adc12 raw data."""
        channel -= 1
        if not ((channel * 2) >= ADC12_START_REG and (channel * 2) <= ADC12_END_REG):
            channel = ADC12_START_REG
        buf = self.readfrommem((ADC12_START_REG + (channel * 2)), 2)
        return struct.unpack("<h", buf)[0]

    def get_adc8_raw(self, channel: int = 0) -> int:
        """! get adc8 raw data."""
        channel -= 1
        channel += ADC8_START_REG
        if not (channel >= ADC8_START_REG and channel <= ADC8_END_REG):
            channel = ADC8_START_REG
        return self.readfrommem(channel, 1)[0]

    @property
    def get_switch_status(self) -> bool:
        """! get switch status."""
        return bool(self.readfrommem(BUTTON_REG, 1)[0])

    def set_led_rgb(self, channel: int, rgb: int, bright: int = 50) -> None:
        """! set rgb led color.
        channel: 0 ~ 8
        rgb: 0x00 ~ 0xffffff
        brightness: 0 ~ 100
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
        """! set rgb led color.
        begin: 0 ~ 8
        end: 0 ~ 8
        rgb: 0x00 ~ 0xffffff
        brightness: 0 ~ 100
        per_delay:0~
        """
        begin = min(TOTAL_LED, max(begin, 1))
        end = min(TOTAL_LED, max(end, 1))
        if begin > end:
            begin, end = end, begin
        for i in range(begin, end + 1):
            self.set_led_rgb(i, rgb, bright)
            time.sleep_ms(per_delay)

    def set_angle_sync_bright(self, channel: int, rgb: int) -> None:
        """! set angle sync bright.
        channel: 0 ~ 8
        rgb: 0x00 ~ 0xffffff
        """
        bright = self._map(self.get_adc12_raw(channel), 0, 4095, 0, 100)
        self.set_led_rgb(channel, rgb, bright)

    def get_device_spec(self, mode: int) -> int:
        """! get firmware version and i2c address.
        mode: 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.readfrommem(mode, 1)[0]

    def set_i2c_address(self, address: int) -> None:
        """! set i2c address.
        address :  1 to 127
        """
        if address >= 1 and address <= 127:
            if address != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, I2C_ADDR_REG, bytearray([address]))
                self._i2c_addr = address
                time.sleep_ms(200)

    def readfrommem(self, reg, num) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self._i2c.writeto(self._i2c_addr, buf)
        buf = bytearray(num)
        self._i2c.readfrom_into(self._i2c_addr, buf)
        return buf

    def _convert_12_to_24(self, val: int) -> int:
        red = (val >> 8) * 17
        green = ((val & 0xF0) >> 4) * 17
        blue = (val & 0x0F) * 17
        return red << 16 | green << 8 | blue

    def _map(self, val, in_min, in_max, out_min, out_max) -> int:
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
