# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7020 import SIM7020
from driver.simcom.common import Modem
import sys

if sys.platform != "esp32":
    from typing import Literal


class NBIOTModule(SIM7020, Modem):
    def __init__(
        self,
        uart_or_id: machine.UART | int,
        tx: int = None,
        rx: int = None,
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

        Modem.__init__(self, uart=self.uart, verbose=verbose)
        SIM7020.__init__(self, uart=self.uart, verbose=verbose)

        if not self.check_modem_is_ready():
            raise Exception("NBIOT module not found in mbus")
        self.set_command_echo_mode(0)
