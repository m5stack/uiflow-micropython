# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import m5can
import sys

if sys.platform != "esp32":
    from typing import Literal


class CANUnit(m5can.CAN):
    _timing_table = {
        # prescaler, sjw, bs1, bs2, triple_sampling
        25000: (128, 3, 16, 8, False),
        50000: (80, 3, 15, 4, False),
        100000: (40, 3, 15, 4, False),
        125000: (32, 3, 15, 4, False),
        250000: (16, 3, 15, 4, False),
        500000: (8, 3, 15, 4, False),
        800000: (4, 3, 16, 8, False),
        1000000: (4, 3, 15, 4, False),
    }

    def __init__(
        self,
        id: Literal[0, 1],
        port: list | tuple = None,
        mode: int = m5can.CAN.NORMAL,
        *args,
        **kwargs,
    ):
        if len(kwargs) == 1:
            (prescaler, sjw, bs1, bs2, triple_sampling) = self._timing_table.get(
                kwargs.get("baudrate")
            )
        elif len(args) == 5:
            (prescaler, sjw, bs1, bs2, triple_sampling) = args
        super().__init__(
            0,
            mode,
            port[1],
            port[0],
            prescaler,
            sjw,
            bs1,
            bs2,
            triple_sampling,
        )


# can_0 = CANUnit(0, (33, 32), CANUnit.NORMAL, baudrate=1000000)
# can_0 = CANUnit(0, (33, 32), CANUnit.NORMAL, 4, 3, 15, 4, False)

MiniCANUnit = CANUnit
