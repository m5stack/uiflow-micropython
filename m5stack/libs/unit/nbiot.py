# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7020 import SIM7020
from driver.simcom.common import Modem
from collections import namedtuple
from .unit_helper import UnitError
import sys

if sys.platform != "esp32":
    from typing import Literal

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class NBIOTUnit(SIM7020, Modem):
    def __init__(
        self,
        uart_or_id: machine.UART | int,
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
        SIM7020.__init__(self, uart=self.uart, verbose=verbose)

        if not self.check_modem_is_ready():
            raise UnitError("NBIOT unit not found in Grove")
        self.set_command_echo_mode(0)
