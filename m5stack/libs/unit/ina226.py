# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.ina226 import INA226


class INA226Unit(INA226):
    """Create an INA226Unit object.

    :param I2C i2c: The I2C bus the Accel Unit is connected to.
    :param int address: The I2C address of the device. Default is 0x41.
    :param str type: The type of INA226. Default is "10A". Options are "1A" and "10A".

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C
            from unit import INA226Unit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            ina226_0 = INA226Unit(i2c0, address=0x41, type="10A")
    """

    def __init__(self, i2c, address=0x41, type="10A"):
        if type == "1A":
            self.shunt_resistor = 0.08
            self._cal_value = 0x0800
        elif type == "10A":
            self.shunt_resistor = 0.005
            self._cal_value = 0x0C80
        super().__init__(i2c, address, shunt_resistor=self.shunt_resistor)
        self.configure(
            avg=self.CFG_AVGMODE_16SAMPLES,
            vbus_conv_time=self.CFG_VBUSCT_8244us,
            vshunt_conv_time=self.CFG_VSHUNTCT_8244us,
            mode=self.CFG_MODE_SANDBVOLT_CONTINUOUS,
        )  # 10A: 0x0C80, 1A:0x811
        self.calibrate(cal_value=self._cal_value)
