# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class JoyCHat:
    def __init__(self, i2c, address: int | list | tuple = 0x38) -> None:
        self._i2c = i2c
        self._address = address
        if self._address in self._i2c.scan():
            pass
        else:
            raise Exception("Joyc Hat maybe not connect")
        self._buffer = memoryview(bytearray(5))
        self._swap_x = False
        self._swap_y = False

    def _read(self):
        self._i2c.readfrom_mem_into(self._address, 0x60, self._buffer)

    def get_x_raw(self, channel: int = 0):
        self._read()
        return self._buffer[0] if channel == 0 else self._buffer[2]

    def get_y_raw(self, channel: int = 0):
        self._read()
        return self._buffer[1] if channel == 0 else self._buffer[3]

    def get_x(self, channel: int = 0):
        self._read()
        x = self._buffer[0] if channel == 0 else self._buffer[2]
        if self._swap_x:
            return -(x - 127)
        else:
            return x - 128

    def get_y(self, channel: int = 0):
        self._read()
        y = self._buffer[1] if channel == 0 else self._buffer[3]
        if self._swap_y:
            return -(y - 127)
        else:
            return y - 128

    def swap_x(self, swap: bool = True):
        self._swap_x = swap

    def swap_y(self, swap: bool = True):
        self._swap_y = swap

    def get_button_status(self, channel: int = 0):
        self._read()
        return bool(self._buffer[4] & (0x10 if channel == 0 else 0x01))

    def fill_color(self, rgb: int = 0) -> None:
        buffer = self._buffer[0:3]
        buffer[:] = rgb.to_bytes(3, "big")
        self._i2c.writeto_mem(self._address, 0x20, buffer)
