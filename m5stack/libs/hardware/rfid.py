# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C, Pin
from unit import RFIDUnit


class RFID(RFIDUnit):
    def __init__(self) -> None:
        in_i2c = I2C(1, scl=Pin(12), sda=Pin(11))
        super().__init__(in_i2c)
