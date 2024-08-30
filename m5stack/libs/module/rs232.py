# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine


class RS232Module:
    def __new__(
        cls,
        id,
        **kwargs,
    ):
        return machine.UART(
            id,
            **kwargs,
        )


# uart1 = RS232Module(1, baudrate=115200, bits=8, parity=None, stop=1, tx=0, rx=35)
