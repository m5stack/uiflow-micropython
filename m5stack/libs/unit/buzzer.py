# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.haptic import Haptic


class BuzzerUnit(Haptic):
    def __init__(self, port):
        super().__init__(port[1], freq=4000)
