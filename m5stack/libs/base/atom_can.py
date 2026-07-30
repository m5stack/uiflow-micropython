# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import m5can
import sys

if sys.platform != "esp32":
    from typing import Literal


class ATOMCANBase(m5can.CAN):
    """Create an ATOMCANBase object

    :param int id: The CAN ID to use, Default is 0.
    :param port: A list or tuple containing the TX and RX pin numbers.
    :type port: list | tuple
    :param int mode: The CAN mode to use(NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY), Default is NORMAL.
    :param int baudrate: The baudrate to use, Default is 1000000.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import ATOMCANBase

            base_can = ATOMCANBase(0, (6, 5), ATOMCANBase.NORMAL, baudrate=1000000)
    """

    def __init__(
        self,
        id: Literal[0, 1],
        port: list | tuple = None,
        mode: int = m5can.CAN.NORMAL,
        prescaler: int = 0,
        sjw: int = 0,
        bs1: int = 0,
        bs2: int = 0,
        triple_sampling: bool = False,
        quantum_resolution_hz: int = 0,
        baudrate: int = 0,
    ):
        super().__init__(
            id,
            mode,
            port[1],
            port[0],
            quantum_resolution_hz,
            brp=prescaler,
            sjw=sjw,
            tseg_1=bs1,
            tseg_2=bs2,
            triple_sampling=triple_sampling,
            baudrate=baudrate // 1000,
        )
