# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class RCAUnit:
    """! Unit RCA is a female jack terminal block for transmitting composite video.

    @en Unit RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).
    @cn Unit RCA是一个1.3英寸RCA扩展屏单元。采用SH1107驱动，分辨率为128*64，单色显示。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/RCA
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/RCA/img-9420bb3d-22b8-4f80-b7fe-e708088f1e51.webp
    @category unit

    @example
                from unit import RCAUnit
                rca = RCAUnit()
                rca.display.fill(0)

    """

    def __init__(
        self,
        port: tuple = (36, 26),
        width: int = 216,
        height: int = 144,
        signal_type: int = 0,
        output_level: int = 0,
        use_psram: int = 0,
    ) -> None:
        """! Initialize the Unit RCA

        @param port The port to which the Unit RCA is connected. port[0]: not used, port[1]: dac pin.
        @param width The width of the RCA display.
        @param height The height of the RCA display.
        @param signal_type The signal type of the RCA display. NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4.
        @param output_level The output level of the RCA display.
        @param use_psram The use of psram of the RCA display.

        """

        self.display = M5.addDisplay(
            None,
            0,
            {
                "unit_rca": {
                    "enabled": True,
                    "width": width,
                    "height": height,
                    "output_width": 0,
                    "output_height": 0,
                    "signal_type": signal_type,  # NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4
                    "use_psram": use_psram,
                    "pin_dac": port[1],
                    "output_level": output_level,
                }
            },
        )  # Add RCA unit
