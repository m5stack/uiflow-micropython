# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct


class MiniJoyHat:
    _ADC_REG = 0x00
    _INT10_REG = 0x10
    _INT8_REG = 0x20
    _BTN_REG = 0x30
    _RGB_REG = 0x40
    _CALIBRATION_REG = 0x50
    _FIRMWARE_REG = 0xF0
    _I2C_ADDR_REG = 0xF0

    def __init__(self, i2c, address: int | list | tuple = 0x54):
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise Exception("MiniJoy Hat maybe not connect")
        self._buffer = memoryview(bytearray(12))
        self._swap_x = False
        self._swap_y = False

    def get_x_i10(self):
        buffer = self._buffer[0:2]
        self._i2c.readfrom_mem_into(self._address, self._INT10_REG, buffer)
        return struct.unpack("<h", buffer)[0]

    def get_y_i10(self):
        buffer = self._buffer[0:2]
        data = self._i2c.readfrom_mem_into(self._address, self._INT10_REG + 2, buffer)
        return struct.unpack("<h", data)[0]

    def get_x_raw(self):
        buffer = self._buffer[0:1]
        self._i2c.readfrom_mem_into(self._address, self._INT8_REG, buffer)
        return struct.unpack("<b", buffer)[0]

    def get_y_raw(self):
        buffer = self._buffer[0:1]
        self._i2c.readfrom_mem_into(self._address, self._INT8_REG + 1, buffer)
        return struct.unpack("<b", buffer)[0]

    def get_x(self):
        x = self.get_x_raw()
        if self._swap_x:
            return -(x + 1) if x >= 0 else abs(x) - 1
        else:
            return x

    def get_y(self):
        y = self.get_y_raw()
        if self._swap_y:
            return -(y + 1) if y >= 0 else abs(y) - 1
        else:
            return y

    def swap_x(self, swap: bool = True):
        self._swap_x = swap

    def swap_y(self, swap: bool = True):
        self._swap_y = swap

    def get_button_status(self):
        buffer = self._buffer[0:1]
        self._i2c.readfrom_mem_into(self._address, self._BTN_REG, buffer)
        return not bool(buffer[0])

    def fill_color(self, rgb: int = 0) -> None:
        buffer = self._buffer[0:3]
        buffer[:] = rgb.to_bytes(3, "big")
        self._i2c.writeto_mem(self._address, self._RGB_REG, buffer)

    def read_calibration(self):
        buffer = self._buffer[0:12]
        self._i2c.readfrom_mem_into(self._address, self._CALIBRATION_REG, buffer)
        return struct.unpack("<HHHHHH", buffer)

    def get_firmware_version(self):
        buffer = self._buffer[0:1]
        self._i2c.readfrom_mem_into(self._address, self._FIRMWARE_REG, buffer)
        return buffer[0]

    def set_i2c_address(self, new_addr):
        buffer = self._buffer[0:1]
        buffer[0] = new_addr & 0xFF
        self._address = new_addr
        self._i2c.writeto_mem(self._address, self._I2C_ADDR_REG, buffer)

    def read_i2c_address(self):
        buffer = self._buffer[0:1]
        self._i2c.readfrom_mem_into(self._address, self._I2C_ADDR_REG, buffer)
        return buffer[0]
