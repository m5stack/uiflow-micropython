# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5
from .pahub import PAHUBUnit
from machine import I2C


class GlassUnit:
    """! Unit Glass is a 1.51-inch transparent OLED expansion screen unit.

    @en Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display, transparent area is 128*56.
    @cn Unit Glass是一个1.51英寸透明OLED扩展屏单元。采用STM32+SSD1309驱动方案，分辨率为128*64，单色显示，透明区域为128*56。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/Glass%20Unit
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/Glass%20Unit/img-4384183e-b663-4dfc-bc3f-5070166c6e2b.webp
    @category unit

    @example
        from unit import GlassUnit
                glass = GlassUnit()
                glass.display.fill(0)

    """

    def __new__(
        cls, i2c: I2C | PAHUBUnit, address: int | list | tuple = 0x3D, freq: int = 400000
    ) -> None:
        """! Initialize the Unit Glass

        @param port The port to which the Unit Glass is connected. port[0]: scl pin, port[1]: sda pin.
        @param address I2C address of the Unit Glass, default is 0x3D.
        @param freq I2C frequency of the Unit Glass.
        """
        return M5.addDisplay(i2c, address, {"unit_glass": True})  # Add Glass unit
