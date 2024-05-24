# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   neoflash.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from driver.neopixel.sk6812 import SK6812


class NeoFlashHat(SK6812):
    """! NeoFlash HAT is specifically designed for M5StickC, it is an RGB LED matrix.

    @en NeoFlash HAT is specifically designed for M5StickC, it is an RGB LED matrix. Space on PCB board is 58x23.5mm and total include 126 RGB LEDs. Every single RGB LED is programmable, which allows you setting the colors and brightness, plus on the 7*18 matrix layout, you will have a nice experience on either display digital numbers or colorful light effect.
    @cn NeoFlash HAT是专为M5StickC设计的，它是一个RGB LED矩阵。 PCB板上的空间为58x23.5mm，总共包括126个RGB LED。 每个RGB LED都是可编程的，这允许您设置颜色和亮度，再加上7*18的矩阵布局，您将在数字显示或彩色灯效方面获得良好体验。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/hat/hat-neoflash
    @image https://static-cdn.m5stack.com/resource/docs/products/hat/hat-neoflash/hat-neoflash_01.webp
    @category hat

    @attr WIDTH The width of the NeoFlashHat.
    @attr HEIGHT The height of the NeoFlashHat.

    @example
        from hardware import *
        from hat import NeoFlashHat
        neoflash = NeoFlashHat((26, 0))
        neoflash.set_pixel(0, 0, 0xFF0000)
        neoflash.set_pixel(1, 0, 0x00FF00)


    """

    WIDTH = 18
    HEIGHT = 7

    def __init__(self, port: tuple) -> None:
        """! Initialize the NeoFlashHat.

        @param port The port to which the NeoFlashHat is connected. port[0]: LEDs pin.
        """
        super().__init__(port[1], self.HEIGHT * self.WIDTH)
        self.set_brightness(10)

    def set_pixel(self, x: int, y: int, color: int) -> None:
        """! Set the color of the pixel.

        @en %1 Set the color of the pixel at position (%2, %3) to %4.
        @cn %1 将位置（%2，%3）的像素的颜色设置为%4。

        @param x The x coordinate of the pixel.
        @param y The y coordinate of the pixel.
        @param color The color of the pixel.
        """
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return

        if y % 2 == 0:
            index = y * self.WIDTH + x
        else:
            index = y * self.WIDTH + self.WIDTH - x - 1
        self.set_color(index, color)

    def set_pixels(self, data: list) -> None:
        """! Set the color of the pixels.

        @en %1 Set the color of the pixels to %2, each element is [x, y, color].
        @cn %1 设置像素的颜色为%2，每个元素为[x，y，color]。

        @param data The list of the pixel position and color, [x, y, color].
        """
        for x, y, color in data:
            self.set_pixel(x, y, color)
