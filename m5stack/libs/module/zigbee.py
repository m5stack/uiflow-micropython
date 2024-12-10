# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from unit import ZigbeeUnit
import sys

if sys.platform != "esp32":
    from typing import Literal


class ZigbeeModule(ZigbeeUnit):
    def __init__(self, id: Literal[0, 1, 2], tx: int, rx: int, verbose=True):
        super().__init__(id, (rx, tx), verbose)
