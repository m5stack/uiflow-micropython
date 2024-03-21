# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.neopixel.sk6812 import SK6812


class RGBUnit(SK6812):
    def __init__(self, port, number):
        super().__init__(port[1], number)
