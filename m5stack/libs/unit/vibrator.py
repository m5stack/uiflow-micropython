# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.haptic import Haptic


class VibratorUnit(Haptic):
    def __init__(self, port: tuple = (26, 0)):
        super().__init__(port[1])
