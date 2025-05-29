# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.vl53l0x import VL53L0X as ToFUnit


class ToF90Unit(ToFUnit):
    """Create an VL53L0X object.

    :param I2C i2c: The I2C bus the VL53L0X is connected to.
    :param int address: The I2C address of VL53L0X. Default is 0x29.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import ToF90Unit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            tof_0 = ToF90Unit(i2c0)
    """

    def __init__(self, i2c, address=0x29):
        super().__init__(i2c, address=address)
