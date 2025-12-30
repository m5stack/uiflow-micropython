# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.simcom.sim7028 import SIM7028


class AtomDTUNBIoT2(SIM7028):
    """Create an AtomDTUNBIoT2 object.

    :param machine.UART uart: The UART object to use.
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |nbiot_init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTUNBIoT2
            from hardware import UART

            uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=19)
            base_nbiot2 = AtomDTUNBIoT2(uart2, verbose=False)
    """

    def __init__(self, uart, verbose=False):
        super().__init__(uart=uart, verbose=verbose)
