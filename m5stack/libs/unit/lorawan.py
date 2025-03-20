# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.asr650x import LoRaWAN_470
import machine
import sys

if sys.platform != "esp32":
    from typing import Literal


class LoRaWANUnit(LoRaWAN_470):
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None):
        self._uart = machine.UART(
            id, tx=port[0], rx=port[1], baudrate=115200, bits=8, parity=None, stop=1
        )
        super(LoRaWAN_470, self).__init__(self._uart)

    def deinit(self):
        pass
