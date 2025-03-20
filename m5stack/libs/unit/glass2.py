# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5
from .pahub import PAHUBUnit
from machine import I2C
import sys

if sys.platform != "esp32":
    from typing import Union


class Glass2Unit:
    """Initialize the Glass2 Unit.

    :param i2c: The I2C bus the Glass2 Unit is connected to.
    :type i2c: I2C | PAHUBUnit
    :param int address: The I2C address of the Glass2 Unit, default is 0x3C.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import Glass2Unit
            glass2_0 = Glass2Unit(i2c0, 0x3c)
    """

    def __new__(cls, i2c: Union[I2C, PAHUBUnit], address: int | list | tuple = 0x3C) -> None:
        return M5.addDisplay(i2c, address, {"unit_glass2": True})  # Add Glass2 unit
