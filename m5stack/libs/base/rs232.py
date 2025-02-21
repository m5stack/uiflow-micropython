# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine


class AtomRS232:
    def __new__(
        cls,
        id,
        **kwargs,
    ):
        return machine.UART(
            id,
            **kwargs,
        )


AtomRS485 = AtomRS232
# uart1 = RS232Module(1, baudrate=115200, bits=8, parity=None, stop=1, tx=0, rx=35)
