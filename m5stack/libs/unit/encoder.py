# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .unit_helper import UnitError
import struct


class EncoderUnit:
    _ENCODER_COUNTER_VALUE_REG = 0x10
    _ENCODER_BUTTON_STATUS_REG = 0x20
    _ENCODER_RGB_LED_REG = 0x30

    def __init__(self, i2c, address: int | list | tuple = 0x40) -> None:
        self._i2c = i2c
        self._address = address
        self._buffer = memoryview(bytearray(5))
        if self._address not in self._i2c.scan():
            raise UnitError("Encoder Unit maybe not connect")
        self._last_value = self._get_rotary_value()
        self._zero_value = self._last_value

    def get_rotary_status(self):
        val = self._get_rotary_value()
        if val != self._last_value:
            return True
        return False

    def get_rotary_value(self):
        self._last_value = self._get_rotary_value()
        return self._last_value - self._zero_value

    def get_rotary_increments(self):
        tmp = self._last_value
        self._last_value = self._get_rotary_value()
        return self._last_value - tmp

    def _get_rotary_value(self):
        buf = self._read_reg_bytes(self._ENCODER_COUNTER_VALUE_REG, 2)
        return struct.unpack("<h", buf)[0]

    def reset_rotary_value(self):
        self._zero_value = self._get_rotary_value()

    def get_button_status(self) -> bool:
        buf = self._read_reg_bytes(self._ENCODER_BUTTON_STATUS_REG, 2)
        return not bool(buf[0])

    def set_color(self, index: int = 0, rgb: int = 0) -> None:
        buf = self._buffer[1:5]
        buf[0] = index
        buf[1:] = rgb.to_bytes(3, "big")
        self._write_reg_bytes(self._ENCODER_RGB_LED_REG, buf)

    def fill_color(self, rgb: int = 0) -> None:
        self.set_color(0, rgb)

    def _read_reg_bytes(self, reg: int = 0, length: int = 0) -> bytearray:
        buf = self._buffer[0:1]
        buf[0] = reg
        self._i2c.writeto(self._address, buf)
        buf = self._buffer[0:length]
        self._i2c.readfrom_into(self._address, buf)
        return buf

    def _write_reg_bytes(self, reg, data):
        buf = self._buffer[0 : 1 + len(data)]
        buf[0] = reg
        buf[1:] = bytes(data)
        self._i2c.writeto(self._address, buf)
