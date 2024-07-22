# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .unit_helper import UnitError


class JoystickUnit:
    def __init__(self, i2c, address: int | list | tuple = 0x52) -> None:
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise UnitError("Joystick Unit maybe not connect")
        self._buffer = memoryview(bytearray(3))
        self._swap_x = False
        self._swap_y = False

    def _read(self):
        self._i2c.readfrom_mem_into(self._address, 0x52, self._buffer)

    def get_x_raw(self):
        self._read()
        return self._buffer[0]

    def get_y_raw(self):
        self._read()
        return self._buffer[1]

    def get_x(self):
        self._read()
        if self._swap_x:
            return -(self._buffer[0] - 127)
        else:
            return self._buffer[0] - 128

    def get_y(self):
        self._read()
        if self._swap_y:
            return -(self._buffer[1] - 127)
        else:
            return self._buffer[1] - 128

    def swap_x(self, swap: bool = True):
        self._swap_x = swap

    def swap_y(self, swap: bool = True):
        self._swap_y = swap

    def get_button_status(self):
        self._read()
        return bool(self._buffer[2])
