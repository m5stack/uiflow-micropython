# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
from driver.sht4x import SHT4x as sht4x
from machine import I2C, Pin


class SHT4X(sht4x):
    """Create an onboard SHT4X sensor object.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import SHT4X

            sht4x = SHT4X()
    """

    def __init__(self):
        """Initialize the onboard SHT4X sensor using the current board profile."""
        self._board = M5.getBoard()
        if self._board == M5.BOARD.M5PaperColor:
            in_i2c = I2C(1, scl=Pin(2), sda=Pin(3))
            super().__init__(i2c=in_i2c)
        else:
            raise RuntimeError("SHT4X is not supported on this board")
