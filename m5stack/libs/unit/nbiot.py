# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import machine
from driver.simcom.sim7020 import SIM7020

if sys.platform != "esp32":
    from typing import Union


class NBIOTUnit(SIM7020):
    """Create an NBIOTUnit object.

    :param uart_or_id: The UART object or UART ID.
    :type uart_or_id: machine.UART | int
    :param port: A list or tuple containing the RX and TX pin numbers. Required if uart_or_id is an ID.
    :type port: list | tuple
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import NBIOTUnit
            import machine

            # Using UART ID and pins (rx, tx)
            nbiot = NBIOTUnit(1, (16, 17))

            # Or using UART object
            uart = machine.UART(1, tx=17, rx=16)
            nbiot = NBIOTUnit(uart)
    """

    def __init__(
        self,
        uart_or_id: "Union[machine.UART, int]",
        port: "Union[list, tuple, None]" = None,
        verbose: bool = False,
    ) -> None:
        if isinstance(uart_or_id, machine.UART):
            self.uart = uart_or_id
        elif isinstance(uart_or_id, int) and port is not None:
            self.uart = machine.UART(
                uart_or_id,
                tx=port[1],
                rx=port[0],
                baudrate=115200,
                bits=8,
                parity=None,
                stop=1,
                rxbuf=1024,
            )
        else:
            raise ValueError("Invalid arguments: must provide either UART or (id + port)")

        super().__init__(uart=self.uart, verbose=verbose)
