# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver.atgm336h import ATGM336H
import sys

if sys.platform != "esp32":
    from typing import Literal


class AtomicGPSV2Base(ATGM336H):
    """Create an AtomicGPSV2Base object.

    :param int id: The UART ID for communication with the GPS module. It can be 1, or 2.
    :param port: A list or tuple containing the TX and RX pins for UART communication.
    :type port: list | tuple
    :param bool verbose: Whether to print verbose output.

    UIFlow Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base.gpsv2 import AtomicGPSV2Base

            gps_0 = AtomicGPSV2Base(id=1, tx=5, rx=6)
    """

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, verbose: bool = False):
        """
        note:
            en: Initialize the GPSUnit with a specific UART id and port for communication.

        params:
            id:
                note: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
            port:
                note: A list or tuple containing the TX and RX pins for UART communication.
            verbose:
                note: Whether to print verbose output.
        """
        super().__init__(id, port[1], port[0], verbose=verbose)
