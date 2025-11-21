# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5

# from .pahub import PAHUBUnit
import machine
import sys

if sys.platform != "esp32":
    from typing import Union


class LCDUnit:
    """Initialize the LCD Unit.

    :param i2c: The I2C bus the LCD Unit is connected to.
    :type i2c: I2C
    :param int address: The I2C address of the LCD Unit, default is 0x3E.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import LCDUnit
            lcd_0 = LCDUnit(i2c0, 0x3e)
    """

    def __new__(cls, i2c: machine.I2C, address: int | list | tuple = 0x3E) -> None:
        return M5.addDisplay(i2c, address, {"unit_lcd": True})  # Add LCD unit
