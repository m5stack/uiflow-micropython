# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from driver.mlx90640 import MLX90640

try:
    from typing import Union
except ImportError:
    pass

THERMAL_ADDR = 0x33


class THERMALUnit(MLX90640):
    def __init__(self, i2c: Union[I2C, PAHUBUnit]):
        self._thermal_addr = THERMAL_ADDR
        self._thermal_i2c = i2c
        self._available()
        super().__init__(self._thermal_i2c, self._thermal_addr)

    def _available(self):
        if self._thermal_addr not in self._thermal_i2c.scan():
            raise UnitError("Thermal unit maybe not connect")

    @property
    def get_max_temperature(self):
        return round(max(self._framebuf), 2)

    @property
    def get_min_temperature(self):
        return round(min(self._framebuf), 2)

    @property
    def get_midpoint_temperature(self):
        return round(self._framebuf[384], 2)

    def get_pixel_temperature(self, x, y):
        if (x * y) > 768 or (x * y) < 0:
            return
        return round(self._framebuf[(x * y) - 1], 2)

    def get_temperature_buffer(self):
        return self._framebuf

    def set_refresh_rate(self, rate):
        """
        REFRESH_0_5_HZ = 0b000  # 0.5Hz
        REFRESH_1_HZ = 0b001  # 1Hz
        REFRESH_2_HZ = 0b010  # 2Hz
        REFRESH_4_HZ = 0b011  # 4Hz
        REFRESH_8_HZ = 0b100  # 8Hz
        REFRESH_16_HZ = 0b101  # 16Hz
        REFRESH_32_HZ = 0b110  # 32Hz
        REFRESH_64_HZ = 0b111  # 64Hz
        """
        self.refresh_rate = rate

    @property
    def get_refresh_rate(self):
        return self.refresh_rate

    def update_temperature_buffer(self):
        return self.get_frame()
