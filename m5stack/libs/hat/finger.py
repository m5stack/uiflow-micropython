# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.fpc1020a.fpc1020a import FPC1020A
from machine import UART
import sys

if sys.platform != "esp32":
    from typing import Literal


class FingerHat(FPC1020A):
    def __init__(self, id: Literal[0, 1, 2] = 2, port: list | tuple = None):
        uart2 = UART(id, 19200, tx=port[1], rx=port[0])
        super().__init__(uart2)
