# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   watering.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import Pin, ADC


class WateringUnit:
    """! Watering is a capacitive soil moisture detection and adjustment unit.

    @en Watering is a capacitive soil moisture detection and adjustment unit. The product integrates water pump and measuring plates for soil moisture detection and pump water control. It can be used for intelligent plant breeding scenarios and can easily achieve humidity detection and Irrigation control. The measurement electrode plate uses the capacitive design, which can effectively avoid the corrosion problem of the electrode plate in actual use compared with the resistive electrode plate.
    @cn Watering是一个电容式土壤湿度检测和调节单元。 该产品集成了水泵和用于土壤湿度检测和泵水控制的测量板。 它可用于智能植物培育场景，并可以轻松实现湿度检测和灌溉控制。 测量电极板采用电容设计，与电阻性电极板相比，可以有效避免实际使用中电极板的腐蚀问题。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/watering
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/watering/watering_01.webp
    @category unit

    @example
                import time
        from unit import WateringUnit
        water = WateringUnit((33,32)) # for core2
        water.on()
        time.sleep(1)
        water.off()
        print(water.get_voltage())
        print(water.get_raw())

    """

    def __init__(self, port: tuple) -> None:
        """! Initialize the Fader.

        @param port The port to which the Fader is connected. port[0]: adc pin, port[1]: pump pin.
        """
        self._pump = Pin(port[1])
        self._pump.init(mode=self._pump.OUT)
        self._adc = ADC(Pin(port[0]), atten=ADC.ATTN_11DB)

    def get_voltage(self) -> float:
        """! Get the voltage of the sensor.

        @en %1 Get the voltage of the sensor.
        @cn %1 获取sensor的电压。
        @return: float, The voltage of the sensor.

        """
        return self._adc.read_uv() / 1000 / 1000

    def get_raw(self) -> int:
        """! Read the raw value of the ADC.

        @en %1 Read the raw value of the ADC.
        @cn %1 读取ADC的原始值。
        @return: int from 0 to 65535

        """
        return self._adc.read_u16()

    def on(self) -> None:
        """! Turn on the pump.

        @en %1 Turn on the pump.
        @cn %1 打开泵。

        """
        self._pump.value(1)

    def off(self) -> None:
        """! Turn off the pump.

        @en %1 Turn off the pump.
        @cn %1 关闭泵。

        """
        self._pump.value(0)

    def set_pump(self, state: int) -> None:
        """! Set the state of the pump.

        @en %1 Set the state of the pump to %2.
        @cn %1 将泵的状态设置为%2。

        @param state [field_switch] The state of the pump.
        """
        self._pump.value(state)
