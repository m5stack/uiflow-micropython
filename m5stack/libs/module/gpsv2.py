# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.atgm336h import ATGM336H

import sys

if sys.platform != "esp32":
    from typing import Literal


class GPSV2Module(ATGM336H):
    def __init__(self, id: Literal[0, 1, 2] = 1, rx: int = None, tx: int = None, pps: int = -1):
        """
        note:
            en: Initialize the GPSModule with a specific UART id and port for communication.

        params:
            id:
                note: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
            tx:
                note: The TX pin for UART communication.
            rx:
                note: The RX pin for UART communication.
            pps:
                note: The PPS (Pulse Per Second) pin, used for high-precision time synchronization.
        """
        super().__init__(id, tx, rx, pps)
