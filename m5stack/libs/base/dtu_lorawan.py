# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.asr650x import LoRaWAN_470
import machine
import sys

if sys.platform != "esp32":
    from typing import Literal


class AtomDTULoRaWANBase(LoRaWAN_470):
    """Create an AtomDTULoRaWANBase object

    :param int id: The UART ID to use (0, 1, or 2). Default is 2.
    :param port: A list or tuple containing the TX and RX pin numbers.
    :type port: list | tuple

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTULoRaWANBase

            dtu_lorawan = AtomDTULoRaWANBase(0, (6, 5))
    """

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None):
        self._uart = machine.UART(
            id, tx=port[0], rx=port[1], baudrate=115200, bits=8, parity=None, stop=1
        )
        super(LoRaWAN_470, self).__init__(self._uart)

    def deinit(self):
        pass
