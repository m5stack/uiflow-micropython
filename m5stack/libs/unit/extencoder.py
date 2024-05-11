# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
from .unit_helper import UnitError


class ExtEncoderUnit:
    _EXT_ENCODER_COUNT_REG = 0x00
    _EXT_ENCODER_METER_REG = 0x10
    _EXT_ENCODER_METER_STRING_REG = 0x20
    _EXT_ENCODER_RESET_REG = 0x30
    _EXT_ENCODER_PERIMETER_REG = 0x40
    _EXT_ENCODER_PULSE_REG = 0x50
    _EXT_ENCODER_ZERO_PULSE_VALUE_REG = 0x60
    _EXT_ENCODER_ZERO_MODE_REG = 0x70
    _EXT_ENCODER_FIRMWARE_VERSION_REG = 0xFE
    _EXT_ENCODER_I2C_ADDRESS_REG = 0xFF

    def __init__(self, i2c, address: int | list | tuple = 0x59):
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise UnitError("ExtEncoder Unit maybe not connect")
        self._buffer = memoryview(bytearray(10))
        self._raw_value = self._get_rotary_value()
        self._base_value = self._raw_value
        self._reset_value = 0

    def get_rotary_status(self):
        val = self._get_rotary_value()
        if val != self._raw_value:
            return True
        return False

    def get_rotary_value(self):
        return self._reset_value + self._get_rotary_value() - self._base_value

    def _get_rotary_value(self):
        data = self._read_bytes(self._EXT_ENCODER_COUNT_REG, 4)
        value = struct.unpack("<i", bytes(data))[0]
        return value

    def get_rotary_increments(self):
        tmp = self._raw_value
        self._raw_value = self._get_rotary_value()
        return self._raw_value - tmp

    def reset_rotary_value(self):
        self._write_bytes(self._EXT_ENCODER_RESET_REG, [1])

    def set_rotary_value(self, new_value):
        self._reset_value = new_value

    """abz"""

    def get_perimeter(self):
        data = self._read_bytes(self._EXT_ENCODER_PERIMETER_REG, 4)
        value = struct.unpack("<I", bytes(data))[0]
        return value

    def set_perimeter(self, perimeter):
        data = struct.pack("<I", perimeter)
        self._write_bytes(self._EXT_ENCODER_PERIMETER_REG, list(data))

    def get_pulse(self):
        data = self._read_bytes(self._EXT_ENCODER_PULSE_REG, 4)
        value = struct.unpack("<I", bytes(data))[0]
        return value

    def set_pulse(self, pulse):
        data = struct.pack("<I", pulse)
        self._write_bytes(self._EXT_ENCODER_PULSE_REG, list(data))

    def get_zero_mode(self):
        data = self._read_bytes(self._EXT_ENCODER_ZERO_MODE_REG, 1)
        return data[0]

    def set_zero_mode(self, mode):
        self._write_bytes(self._EXT_ENCODER_ZERO_MODE_REG, [mode])

    def get_meter_value(self):
        data = self._read_bytes(self._EXT_ENCODER_METER_REG, 4)
        value = struct.unpack("<i", bytes(data))[0]
        return value

    def get_zero_pulse_value(self):
        data = self._read_bytes(self._EXT_ENCODER_ZERO_PULSE_VALUE_REG, 4)
        value = struct.unpack("<i", bytes(data))[0]
        return value

    def set_zero_pulse_value(self, value):
        data = struct.pack("<i", value)
        self._write_bytes(self._EXT_ENCODER_ZERO_PULSE_VALUE_REG, list(data))

    def set_address(self, new_addr):
        self._write_bytes(self._EXT_ENCODER_I2C_ADDRESS_REG, [new_addr])
        self.addr = new_addr
        return self.addr

    def get_firmware_version(self):
        data = self._read_bytes(self._EXT_ENCODER_FIRMWARE_VERSION_REG, 1)
        return data[0]

    def _write_bytes(self, reg, data):
        buf = self._buffer[0 : 1 + len(data)]
        buf[0] = reg
        buf[1:] = bytes(data)
        self._i2c.writeto(self._address, buf)

    def _read_bytes(self, reg, length):
        buf = self._buffer[0:1]
        buf[0] = reg
        self._i2c.writeto(self._address, buf)
        buf = self._buffer[0:length]
        self._i2c.readfrom_into(self._address, buf)
        return buf
