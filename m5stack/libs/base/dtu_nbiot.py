# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.simcom.sim7020 import SIM7020


class AtomDTUNBIoT(SIM7020):
    """Create an AtomDTUNBIoT object.

    :param machine.UART uart: The UART object to use.
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |nbiot_init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTUNBIoT
            from hardware import UART

            uart0 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=19)
            dtu_nbiot = AtomDTUNBIoT(uart0, verbose=False)
    """

    def __init__(self, uart, verbose=False):
        super().__init__(uart=uart, verbose=verbose)
