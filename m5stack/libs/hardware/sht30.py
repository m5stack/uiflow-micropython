# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.sht30 import SHT30 as sht30
from machine import I2C, Pin


class SHT30(sht30):
    def __init__(self):
        in_i2c = I2C(1, scl=Pin(22), sda=Pin(21))
        super().__init__(i2c=in_i2c)
