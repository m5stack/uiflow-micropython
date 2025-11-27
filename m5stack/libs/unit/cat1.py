# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.ml307r import ML307R
from driver.simcom.common import Modem
from collections import namedtuple
from .unit_helper import UnitError
import sys

if sys.platform != "esp32":
    from typing import Literal

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class Cat1Unit(ML307R, Modem):
    """Create an Cat1Unit object

    :param int id: The UART ID to use (0, 1, or 2). Default is 2.
    :param port: A list or tuple containing the TX and RX pin numbers.
    :type port: list | tuple
    :param verbose: Enable verbose output for debugging. Default is False.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import Cat1Unit

            cat1cn_0 = Cat1Unit(2, port=(33, 32))
    """

    def __init__(
        self,
        uart_or_id,
        port: list | tuple = None,
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

        Modem.__init__(self, uart=self.uart, verbose=verbose)

        if not self.check_modem_is_ready():
            raise UnitError("NBIOT unit not found in Grove")
        self.set_command_echo_mode(0)

        ML307R.__init__(self, uart=self.uart, verbose=verbose)
