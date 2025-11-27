# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from unit.asr import ASRUnit


class ASRModule(ASRUnit):
    """Voice recognition hardware module.

    :param int id: UART port ID for communication. Default is 2.
    :param int tx: TX pin number.
    :param int rx: RX pin number.
    :param bool verbose: Enable verbose output. Default is False.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import ASRUnit

            # Initialize with UART1, TX on pin 2, RX on pin 1
            asr = ASRModule(id=2, tx=2, rx=1)
    """

    def __init__(self, id=1, tx=-1, rx=-1, verbose: bool = False):
        super().__init__(id, port=(rx, tx), verbose=verbose)
