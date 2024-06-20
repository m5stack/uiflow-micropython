# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class MiniOLEDUnit:
    """! MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.

    @en MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.
    @cn MiniOLED UNIT是一个0.42英寸I2C接口OLED屏单元，分辨率为72*40，单色白色显示。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/MiniOLED%20Unit
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/MiniOLED%20Unit/img-8d9a2ae0-331b-4c02-8e2f-0f9142a4395d.webp
    @category unit

    @example
        from unit import MiniOLEDUnit
                oled = MiniOLEDUnit()
                oled.display.fill(0)

    """

    def __init__(
        self, port: tuple = (33, 32), address: int | list | tuple = 0x3D, freq: int = 400000
    ) -> None:
        """! Initialize the Unit MiniOLED

        @param port The port to which the Unit MiniOLED is connected. port[0]: scl pin, port[1]: sda pin.
        @param address I2C address of the Unit MiniOLED, default is 0x3D.
        @param freq I2C frequency of the Unit MiniOLED.
        """

        self.display = M5.addDisplay(
            {
                "unit_mini_oled": {
                    "enabled": True,
                    "pin_scl": port[0],
                    "pin_sda": port[1],
                    "i2c_addr": address,
                    "i2c_freq": freq,
                }
            }
        )  # Add MiniOLED unit
