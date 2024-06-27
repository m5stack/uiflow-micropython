# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class Glass2Unit:
    """! Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.

    @en Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.
    @cn Glass2 Unit是一个1.51英寸透明OLED显示单元，采用SSD1309驱动方案。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/Glass2%20Unit
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/Glass2%20Unit/img-d882d0b7-dce0-4202-9b76-b9f25e7ad829.webp
    @category unit

    @example
        from unit import Glass2Unit
                glass = Glass2Unit()
                glass.display.fill(0)

    """

    def __init__(
        self, port: tuple = (33, 32), address: int | list | tuple = 0x3D, freq: int = 400000
    ) -> None:
        """! Initialize the Unit Glass2

        @param port The port to which the Unit Glass2 is connected. port[0]: scl pin, port[1]: sda pin.
        @param address I2C address of the Unit Glass2, default is 0x3D.
        @param freq I2C frequency of the Unit Glass2.
        """

        self.display = M5.addDisplay(
            {
                "unit_glass2": {
                    "enabled": True,
                    "pin_scl": port[0],
                    "pin_sda": port[1],
                    "i2c_addr": address,
                    "i2c_freq": freq,
                }
            }
        )  # Add Glass2 unit
