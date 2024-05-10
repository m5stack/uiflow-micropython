# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .pir import PIRUnit
from micropython import const


class HallEffectUnit(PIRUnit):
    IRQ_ACTIVE = const(0)
    IRQ_NEGATIVE = const(1)

    def __init__(self, port) -> None:
        super().__init__(port)
