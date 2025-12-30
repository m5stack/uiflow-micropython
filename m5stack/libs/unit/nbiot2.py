# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7028 import SIM7028
import sys

if sys.platform != "esp32":
    from typing import Literal
    from typing import Union


class NBIOT2Unit(SIM7028):
    """Create an NBIOT2Unit object.

    :param int id: The UART ID.
    :param port: A list or tuple containing the RX and TX pin numbers.
    :type port: list | tuple
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import NBIOT2Unit

            # Using UART ID 1 and pins (rx=16, tx=17)
            nbiot2 = NBIOT2Unit(1, port=(16, 17))
    """

    def __init__(
        self,
        id: "Literal[0, 1, 2]" = 1,
        port: "Union[list, tuple, None]" = None,
        verbose=False,
    ) -> None:
        if port is None:
            raise ValueError("The 'port' argument must be a list or tuple of (rx, tx) pins.")
        self.uart = machine.UART(
            id, tx=port[1], rx=port[0], baudrate=115200, bits=8, parity=None, stop=1, rxbuf=1024
        )
        super().__init__(uart=self.uart, verbose=verbose)
