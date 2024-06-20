# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class LCDUnit:
    """! Unit LCD is a 1.14 inch color LCD expansion screen unit.

    @en Unit LCD is a 1.14 inch color LCD expansion screen unit. It adopts ST7789V2 drive scheme, the resolution is 135*240, and it supports RGB666 display (262,144 colors).
    @cn Unit LCD是一个1.14英寸彩色LCD扩展屏单元。采用ST7789V2驱动方案，分辨率为135*240，支持RGB666显示（262,144种颜色）。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/lcd
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/lcd/lcd_01.webp
    @category unit

    @example
        from unit import LCDUnit
                lcd = LCDUnit()
                lcd.display.fill(0)

    """

    def __init__(
        self, port: tuple = (33, 32), address: int | list | tuple = 0x3D, freq: int = 400000
    ) -> None:
        """! Initialize the Unit LCD

        @param port The port to which the Unit LCD is connected. port[0]: scl pin, port[1]: sda pin.
        @param address I2C address of the Unit LCD, default is 0x3D.
        @param freq I2C frequency of the Unit LCD.
        """

        self.display = M5.addDisplay(
            {
                "unit_lcd": {
                    "enabled": True,
                    "pin_scl": port[0],
                    "pin_sda": port[1],
                    "i2c_addr": address,
                    "i2c_freq": freq,
                }
            }
        )  # Add LCD unit
