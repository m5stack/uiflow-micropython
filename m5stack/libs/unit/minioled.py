# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5
from .pahub import PAHUBUnit
import machine
import sys

if sys.platform != "esp32":
    from typing import Union


class MiniOLEDUnit:
    """Initialize the Mini OLED Unit.

    :param i2c: The I2C bus the Mini OLED Unit is connected to.
    :type i2c: I2C | PAHUBUnit
    :param int address: The I2C address of the Mini OLED Unit, default is 0x3C.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import MiniOLEDUnit
            minioled_0 = MiniOLEDUnit(i2c0, 0x3c)
    """

    def __new__(
        cls, i2c: Union[machine.I2C, PAHUBUnit], address: int | list | tuple = 0x3C
    ) -> None:
        return M5.addDisplay(i2c, address, {"unit_mini_oled": True})  # Add MiniOLED unit
