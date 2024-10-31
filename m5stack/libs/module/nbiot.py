# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7020 import SIM7020
import sys

if sys.platform != "esp32":
    from typing import Literal


class NBIOTModule(SIM7020):
    def __init__(self, id: Literal[0, 1, 2], tx: int, rx: int) -> None:
        self.uart = machine.UART(
            id, tx=tx, rx=rx, baudrate=115200, bits=8, parity=None, stop=1, rxbuf=1024
        )
        super().__init__(uart=self.uart)
        if not self.check_modem_is_ready():
            raise Exception("NBIOT module not found in mbus")
        self.set_command_echo_mode(0)
