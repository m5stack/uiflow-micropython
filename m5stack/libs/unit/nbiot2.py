# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7028 import SIM7028
from .unit_helper import UnitError
import sys

if sys.platform != "esp32":
    from typing import Literal


class NBIOT2Unit(SIM7028):
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None) -> None:
        self.uart = machine.UART(
            id, tx=port[1], rx=port[0], baudrate=115200, bits=8, parity=None, stop=1, rxbuf=1024
        )
        super().__init__(uart=self.uart)
        for i in range(0, 3):
            self.modem_status = self.check_modem_is_ready()
            if self.modem_status:
                break
        if not self.modem_status:
            raise UnitError("NBIOT2 unit not found in Grove")
        del self.modem_status
        self.set_command_echo_mode(0)
