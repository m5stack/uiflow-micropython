# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   key.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import Pin
from driver.neopixel.sk6812 import SK6812


class KeyUnit(SK6812):
    """! Unit Key is a single mechanical key input unit with built-in RGB LED.

    @en Unit Key is a single mechanical key input unit with built-in RGB LED. The key shaft adopts Blue switch with tactile bump and audible click features. Embedded with one programable RGB LED - SK6812, supports 256 level brightness. Two digital IOs are available for key status and LED control key status and lighting control. Suitable for multiple HMI applications.
    @cn Unit Key是一个带有内置RGB LED的单个机械按键输入单元。按键轴采用具有触觉颠簸和可听到的单击特性的蓝色开关。内置一个可编程RGB LED - SK6812，支持256级亮度。两个数字IO可用于按键状态和LED控制按键状态和照明控制。适用于多种HMI应用。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/key
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/key/key_01.webp
    @category unit

    @example
        from unit import KeyUnit
        key = KeyUnit((33,32)) # for core2
        key.set_color(0x00FF00)
        key.set_brightness(10)
        key.get_key_state()

    """

    def __init__(self, port: tuple):
        """! Initialize the KeyUnit.

        @param port The port to which the KeyUnit is connected. port[0]: key pin, port[1]: LEDs pin.
        """
        super().__init__(port[1], 1)
        self._key = Pin(port[0])
        self._key.init(mode=self._key.IN)
        self.set_brightness(10)

    def get_key_state(self) -> int:
        """! Get the state of the key.

        @en %1 Get the state of the key.
        @cn %1 获取按键的状态。
        @return: int, The state of the key, 0: pressed, 1: released.
        """
        return self._key.value()

    def set_color(self, color: int) -> None:
        """! Set the color of the LED.

        @en %1 Set the color of the LED to %2.
        @cn %1 将LED的颜色设置为%2。
        @param color The color of the LED.
        """
        super().set_color(0, color)

    def set_brightness(self, br: int) -> None:
        """! Set the brightness of the LED.

        @en %1 Set the brightness of the LED to %2.
        @cn %1 将LED的亮度设置为%2。
        @param br The brightness of the LED, range from 0 to 100.
        """
        super().set_brightness(br)
