# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct


class JoystickHat:
    def __init__(self, i2c, address: int | list | tuple = 0x38) -> None:
        self._i2c = i2c
        self._address = address
        if self._address in self._i2c.scan():
            pass
        else:
            raise Exception("Joystick Hat maybe not connect")
        self._buffer = memoryview(bytearray(3))
        self._swap_x = False
        self._swap_y = False

    def _read(self):
        self._i2c.readfrom_mem_into(self._address, 0x02, self._buffer)

    def get_x_raw(self):
        self._read()
        return self._buffer[0]

    def get_y_raw(self):
        self._read()
        return self._buffer[1]

    def get_x(self):
        self._read()
        x = struct.unpack_from("b", self._buffer, 0)[0]
        if self._swap_x:
            return -(x + 1) if x >= 0 else abs(x) - 1
        else:
            return x

    def get_y(self):
        self._read()
        y = struct.unpack_from("b", self._buffer, 1)[0]
        if self._swap_y:
            return -(y + 1) if y >= 0 else abs(y) - 1
        else:
            return y

    def swap_x(self, swap: bool = True):
        self._swap_x = swap

    def swap_y(self, swap: bool = True):
        self._swap_y = swap

    def get_button_status(self):
        self._read()
        return not bool(self._buffer[2])
