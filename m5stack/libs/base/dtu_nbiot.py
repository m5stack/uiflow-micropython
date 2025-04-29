# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7020 import SIM7020
from driver.simcom.common import Modem
import sys

if sys.platform != "esp32":
    from typing import Literal


class AtomDTUNBIoT(SIM7020, Modem):
    """Create an AtomDTUNBIoT object

    :param int id: The UART ID to use (0, 1, or 2). Default is 2.
    :param port: A list or tuple containing the TX and RX pin numbers.
    :type port: list | tuple

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTUNBIoT

            dtu_nbiot = AtomDTUNBIoT(0, (22, 19))
    """

    def __init__(self, uart, verbose=False):
        self.uart = uart
        self.verbose = verbose
        Modem.__init__(self, uart=self.uart, verbose=verbose)
        SIM7020.__init__(self, uart=self.uart, verbose=verbose)

        if not self.check_modem_is_ready():
            raise Exception("NBIoT Base not found in bus")
