# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.scd40 import SCD40 as _SCD40


class SCD40(_SCD40):
    def __init__(self) -> None:
        i2c1 = machine.I2C(1, scl=machine.Pin(12), sda=machine.Pin(11), freq=100000)
        super().__init__(i2c1, SCD40.SCD40_I2C_ADDR)
