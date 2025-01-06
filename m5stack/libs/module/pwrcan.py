# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import m5can
import sys

if sys.platform != "esp32":
    from typing import Literal


class PwrCANModule(m5can.CAN):
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
        tx,
        rx,
        mode: int = m5can.CAN.NORMAL,
        *args,
        **kwargs,
    ):
        print("CAN")
        if len(kwargs) == 1:
            (prescaler, sjw, bs1, bs2, triple_sampling) = self._timing_table.get(
                kwargs.get("baudrate")
            )
        elif len(args) == 5:
            (prescaler, sjw, bs1, bs2, triple_sampling) = args

        super().__init__(
            0,
            mode,
            tx,
            rx,
            prescaler,
            sjw,
            bs1,
            bs2,
            triple_sampling,
        )


class PwrCANModuleRS485:
    def __new__(
        cls,
        id,
        **kwargs,
    ):
        return machine.UART(
            id,
            **kwargs,
        )


# can_0 = PwrCANModule(0, 32, 33, PwrCANModule.NORMAL, baudrate=1000000)
# can_0 = PwrCANModule(0, 32, 33, PwrCANModule.NORMAL, 4, 3, 15, 4, False)
# rs485_0 = PwrCANModuleRS485(1, baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10, txbuf=256, rxbuf=256, timeout=0, timeout_char=0, invert=0, flow=0)
