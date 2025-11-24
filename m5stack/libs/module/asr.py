# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from unit.asr import ASRUnit


class ASRModule(ASRUnit):
    """Voice recognition hardware module.

    :param int id: UART port ID for communication. Default is 1.
    :param list|tuple port: Tuple containing TX and RX pin numbers.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import ASRUnit

            # Initialize with UART1, TX on pin 2, RX on pin 1
            asr = ASRUnit(id=1, port=(1, 2))
    """

    def __init__(self, id: Literal[0, 1, 2] = 1, tx=-1, rx=-1, verbose: bool = False):
        super().__init__(id, port=(rx, tx), verbose=verbose)
