# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.sen55 import SEN55 as _SEN55


class SEN55(_SEN55):
    def __init__(self) -> None:
        i2c1 = machine.I2C(1, scl=machine.Pin(12), sda=machine.Pin(11), freq=100000)
        super().__init__(i2c1, SEN55.SEN55_I2C_ADDR)
