# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.ina226 import INA226 as _INA226
from module.mbus import i2c1


class Module16340(_INA226):
    """Create an Module16340 object.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import Module16340

            module16340 = Module16340()
    """

    def __init__(self, address=0x45):
        self.shunt_resistor = 0.02  # ohm
        self._cal_value = 0x0832
        super().__init__(i2c1, address, shunt_resistor=self.shunt_resistor)
        self.configure(
            avg=self.CFG_AVGMODE_16SAMPLES,
            vbus_conv_time=self.CFG_VBUSCT_8244us,
            vshunt_conv_time=self.CFG_VSHUNTCT_8244us,
            mode=self.CFG_MODE_SANDBVOLT_CONTINUOUS,
        )
        self.calibrate(cal_value=self._cal_value)

