# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5
from .pahub import PAHUBUnit
from machine import I2C
import sys

if sys.platform != "esp32":
    from typing import Union


class GlassUnit:
    """Initialize the Glass Unit.

    :param i2c: The I2C bus the Glass Unit is connected to.
    :type i2c: I2C | PAHUBUnit
    :param int address: The I2C address of the Glass Unit, default is 0x3D.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import GlassUnit
            glass_0 = GlassUnit(i2c0, 0x3d)
    """

    def __new__(cls, i2c: Union[I2C, PAHUBUnit], address: int | list | tuple = 0x3D):
        return M5.addDisplay(i2c, address, {"unit_glass": True})  # Add Glass unit
