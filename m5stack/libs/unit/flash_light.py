# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   flash.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import Pin
import utime


class FlashLightUnit:
    """! FlashLight UNIT is an I/O Unit with built-in flash, including AW3641 driver and a white LED, with a color temperature of 5000-5700K.

    @en FlashLight UNIT is an I/O Unit with built-in flash, including AW3641 driver and a white LED, with a color temperature of 5000-5700K. There is a mode selection switch on the board, which can set the flash mode and the constant lighting mode. The communication interface is GPIO. This Unit can be used as a flash or lighting applications.
    @cn FlashLight UNIT是一个带有内置闪光灯的I/O单元，包括AW3641驱动器和一个白色LED，色温为5000-5700K。 板上有一个模式选择开关，可以设置闪光模式和恒定照明模式。 通信接口为GPIO。 该单元可用于闪光或照明应用。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/FlashLight
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/FlashLight/img-ded1dc49-1697-43d2-857e-551bbb664eda.webp
    @category unit

    @example
        from unit import FlashLightUnit
        flash = FlashLightUnit((33,32))
        flash.flash(FlashLightUnit.BRIGHTNESS_100, FlashLightUnit.TIME_220MS, True)

    """

    BRIGHTNESS_100 = 1
    BRIGHTNESS_90 = 2
    BRIGHTNESS_80 = 3
    BRIGHTNESS_70 = 4
    BRIGHTNESS_60 = 5
    BRIGHTNESS_50 = 6
    BRIGHTNESS_40 = 7
    BRIGHTNESS_30 = 8
    TIME_220MS = 1
    TIME_1300MS = 2

    def __init__(self, port: tuple) -> None:
        """! Initialize the FlashLightUnit.

        @param port The port to which the FlashLightUnit is connected. port[0]: adc pin, port[1]: pump pin.
        """
        self._en = Pin(port[1])
        self._en.init(mode=self._en.OUT)
        self._en.value(0)

    def flash(self, brightness: int, time: int, turn_off=False) -> None:
        """! Flash the light.

        @en %1 Flash with brightness %2 and time %3. turn off after flash: %4
        @cn %1 闪光，亮度%2，时间%3。闪光后关闭：%4

        @param brightness [field_dropdown] The brightness of the light.
            @options {
                [100%, FlashLightUnit.BRIGHTNESS_100]
                [90%, FlashLightUnit.BRIGHTNESS_90]
                [80%, FlashLightUnit.BRIGHTNESS_80]
                [70%, FlashLightUnit.BRIGHTNESS_70]
                [60%, FlashLightUnit.BRIGHTNESS_60]
                [50%, FlashLightUnit.BRIGHTNESS_50]
                [40%, FlashLightUnit.BRIGHTNESS_40]
                [30%, FlashLightUnit.BRIGHTNESS_30]
            }
        @param time [field_dropdown] The time of the light.
            @options {
                    [220ms, FlashLightUnit.TIME_220MS]
                    [1300ms, FlashLightUnit.TIME_1300MS]
            }
        @param turn_off [field_switch] Turn off the light after flash.
        """

        if brightness <= 0:
            self._en.value(0)
            return

        if brightness > 8:
            brightness = 8
        if time != 1:
            time = 2

        pulse = brightness * time
        for p in range(pulse):
            self._en.value(0)
            utime.sleep_us(2)
            self._en.value(1)
            utime.sleep_us(2)

        if turn_off:
            if time == 1:
                utime.sleep_ms(220)
            else:
                utime.sleep_ms(1300)
            self._en.value(0)
