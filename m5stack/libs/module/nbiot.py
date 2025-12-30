# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import machine
from driver.simcom.sim7020 import SIM7020

if sys.platform != "esp32":
    from typing import Union


class NBIOTModule(SIM7020):
    """Create an NBIOTModule object.

    :param uart_or_id: The UART object or UART ID.
    :type uart_or_id: machine.UART | int
    :param int tx: The UART TX pin. Required if uart_or_id is an ID.
    :param int rx: The UART RX pin. Required if uart_or_id is an ID.
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import NBIOTModule
            import machine

            # Using UART ID and pins (rx, tx)
            nbiot = NBIOTModule(1, tx=17, rx=16)

            # Or using UART object
            uart = machine.UART(1, tx=17, rx=16)
            nbiot = NBIOTModule(uart)
    """

    def __init__(
        self,
        uart_or_id: "Union[machine.UART, int]",
        tx: "Union[int, None]" = None,
        rx: "Union[int, None]" = None,
        verbose: bool = False,
    ) -> None:
        if isinstance(uart_or_id, machine.UART):
            self.uart = uart_or_id

        elif isinstance(uart_or_id, int) and tx is not None and rx is not None:
            self.uart = machine.UART(
                uart_or_id,
                tx=tx,
                rx=rx,
                baudrate=115200,
                bits=8,
                parity=None,
                stop=1,
                rxbuf=1024,
            )
        else:
            raise ValueError("Invalid arguments: please provide UART instance or (id, tx, rx)")

        super().__init__(uart=self.uart, verbose=verbose)
