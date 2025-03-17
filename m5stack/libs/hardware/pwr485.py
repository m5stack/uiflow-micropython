# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine


class PWR485:
    """Construct a PWR485 object of the given id.

    PWR485 class inherits UART class, See :ref:`hardware.UART <hardware.UART>` for more details.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hadrware import PWR485

            pwr485_0 = PWR485(2, baudrate=115200, bits=8, parity=None, stop=1, tx=0, rx=39, rts=46, mode=PWR485.MODE_RS485_HALF_DUPLEX)
    """

    MODE_UART = machine.UART.MODE_UART
    MODE_RS485_HALF_DUPLEX = machine.UART.MODE_RS485_HALF_DUPLEX
    MODE_IRDA = machine.UART.MODE_IRDA
    MODE_RS485_COLLISION_DETECT = machine.UART.MODE_RS485_COLLISION_DETECT
    MODE_RS485_APP_CTRL = machine.UART.MODE_RS485_APP_CTRL

    def __new__(
        cls,
        id,
        **kwargs,
    ):
        return machine.UART(
            id,
            **kwargs,
        )
