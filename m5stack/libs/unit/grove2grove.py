# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   grove2grove.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import Pin, ADC


class Grove2GroveUnit:
    """! UNIT-GROVE2GROVE is a Grove expansion Unit with On/Off Control + Current Meter functions.

    @en UNIT-GROVE2GROVE is a Grove expansion Unit with On/Off Control + Current Meter functions. On/Off control adopts switch value, Current meter is 0 - 3.3V analog signal.
    @cn UNIT-GROVE2GROVE是一个带有开关控制+电流表功能的Grove扩展单元。 开/关控制采用开关值，电流表是0 - 3.3V模拟信号。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/unit_grove2grove
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/unit_grove2grove/unit_grove2grove_01.webp
    @category unit

    @example
        import time
        from unit import Grove2GroveUnit
        grove2grove = Grove2GroveUnit((33,32)) # for core2
        grove2grove.on()


    """

    def __init__(self, port: tuple) -> None:
        """! Initialize the Grove2GroveUnit.

        @param port The port to which the Grove2GroveUnit is connected. port[0]: adc pin, port[1]: grove pin.
        """
        self._en = Pin(port[1])
        self._en.init(mode=self._en.OUT)
        self._adc = ADC(Pin(port[0]), atten=ADC.ATTN_11DB)
        self._update_vref()

    def _update_vref(self) -> float:
        """! Update the reference voltage of the sensor.

        @en %1 Update the reference voltage of the sensor.
        @cn %1 更新sensor的参考电压。
        @return: float, The reference voltage of the sensor.

        """
        self.vref = self._get_voltage()
        return self.vref

    def _get_voltage(self) -> float:
        """! Get the voltage of the sensor.

        @en %1 Get the voltage of the sensor.
        @cn %1 获取sensor的电压。
        @return: float, The voltage of the sensor.

        """
        avg = 0
        for i in range(64):
            avg += self._adc.read()
        avg /= 64
        return round(((avg * 3.30) / 4095.0), 3)

    def get_current(self):
        """! Get the current of the sensor.

        @en %1 Get the current of the sensor in A.
        @cn %1 获取sensor的电流，单位为A。

        @return: float, The current of the sensor.

        """

        return round(((self._get_voltage() - self.vref) / 50.0 / 0.02), 3)

    def on(self) -> None:
        """! Turn on the grove.

        @en %1 Turn on the grove.
        @cn %1 打开Grove。

        """
        self._en.value(1)

    def off(self) -> None:
        """! Turn off the grove.

        @en %1 Turn off the grove.
        @cn %1 关闭Grove。

        """
        self._en.value(0)

    def set_en(self, state: int) -> None:
        """! Set the state of the grove.

        @en %1 Set the state of the grove to %2.
        @cn %1 将Grove的状态设置为%2。

        @param state [field_switch] The state of the grove.
        """
        self._en.value(state)
