# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class OLEDUnit:
    """! Unit OLED is a 1.3-inch OLED expansion screen unit.

    @en Unit OLED is a 1.3-inch OLED expansion screen unit. Driveing by SH1107, and the resolution is 128*64, monochrome display.
    @cn Unit OLED是一个1.3英寸OLED扩展屏单元。采用SH1107驱动，分辨率为128*64，单色显示。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/oled
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/oled/oled_01.webp
    @category unit

    @example
        from unit import OLEDUnit
                oled = OLEDUnit()
                oled.display.fill(0)

    """

    def __init__(
        self, port: tuple = (33, 32), address: int | list | tuple = 0x3D, freq: int = 400000
    ) -> None:
        """! Initialize the Unit OLED

        @param port The port to which the Unit OLED is connected. port[0]: scl pin, port[1]: sda pin.
        @param address I2C address of the Unit OLED, default is 0x3D.
        @param freq I2C frequency of the Unit OLED.
        """

        self.display = M5.addDisplay(
            {
                "unit_oled": {
                    "enabled": True,
                    "pin_scl": port[0],
                    "pin_sda": port[1],
                    "i2c_addr": address,
                    "i2c_freq": freq,
                }
            }
        )  # Add OLED unit
