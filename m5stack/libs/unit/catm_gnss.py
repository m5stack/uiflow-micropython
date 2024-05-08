# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import UART
from driver.simcom.sim7080 import SIM7080
from collections import namedtuple
from .unit_helper import UnitError
import sys

if sys.platform != "esp32":
    from typing import Literal

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class CATMGNSSUnit(SIM7080):
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None) -> None:
        self.uart = UART(id, tx=port[1], rx=port[0])
        super().__init__(uart=self.uart)
        if not self.check_modem_is_ready():
            raise UnitError("CATM+GNSS unit not found in Grove")
        self.set_command_echo_mode(0)
