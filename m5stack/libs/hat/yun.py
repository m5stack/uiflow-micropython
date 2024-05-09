# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.bmp280 import BMP280
from driver.sht20 import SHT20
from .hat_helper import HatError
import struct


class YUNHat:
    def __init__(self, i2c: I2C, address: int | list | tuple = 0x38):
        self.i2c = i2c
        self.i2c_addr = address
        self._available()
        self.bmp280 = BMP280(i2c=i2c)
        self.sht20 = SHT20(i2c=i2c)

    def _available(self):
        if self.i2c_addr not in self.i2c.scan():
            raise HatError("Yun hat maybe not found.")

    def set_all_rgb_led(self, rgb):
        buff = bytearray(4)
        buff[0] = 14
        buff[1] = (rgb & 0xFF0000) >> 16
        buff[2] = (rgb & 0x00FF00) >> 8
        buff[3] = rgb & 0x0000FF
        self.i2c.writeto_mem(self.i2c_addr, 0x01, buff)

    def set_rgb_led(self, pos, rgb):
        buff = bytearray(4)
        buff[0] = pos - 1
        buff[1] = (rgb & 0xFF0000) >> 16
        buff[2] = (rgb & 0x00FF00) >> 8
        buff[3] = rgb & 0x0000FF
        self.i2c.writeto_mem(self.i2c_addr, 0x01, buff)

    @property
    def get_light_brightness(self):
        buf = self.i2c.readfrom_mem(self.i2c_addr, 0x00, 2)
        return struct.unpack("<h", buf)[0]

    @property
    def get_bmp280_temperature(self):
        return self.bmp280.measure()[0]

    @property
    def get_sht20_temperature(self):
        return round(self.sht20.temperature, 2)

    @property
    def get_pressure(self):
        return round((self.bmp280.measure()[1] / 100), 2)

    @property
    def get_humidity(self):
        return round(self.sht20.humidity, 2)
