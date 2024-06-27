# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class DisplayModule:
    """! Display Module 13.2 is an expansion module for HD audio and video.

    @en Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN GW1NR series FPGA chip to output display signals, and employing the LT8618S chip for signal output conditioning.
    @cn Display Module 13.2是一个高清音视频扩展模块，采用高云GW1NR系列FPGA芯片输出显示信号，采用LT8618S芯片进行信号输出调理。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/Display%20Module%2013.2
    @image https://static-cdn.m5stack.com/resource/docs/products/module/Display%20Module%2013.2/img-cec9dc43-a087-44da-a219-831f70b19314.webp
    @category module

    @example
        from module import DisplayModule
                disp = DisplayModule()
                disp.display.fill(0)

    """

    def __init__(
        self,
        port: tuple = (36, 26),
        width: int = 216,
        height: int = 144,
        refresh_rate: int = 60,
        pixel_clock: int = 74250000,
        scale_w: int = 0,
        scale_h: int = 0,
    ) -> None:
        """! Initialize the Module Display

        @param port The port to which the Module Display is connected. port[0]: not used, port[1]: dac pin.
        @param width The width of the Module Display.
        @param height The height of the Module Display.
        @param refresh_rate The refresh rate of the Module Display.
        @param pixel_clock The pixel clock of the Module Display.
        @param scale_w The scale width of the Module Display.
        @param scale_h The scale height of the Module Display.

        """

        self.display = M5.addDisplay(
            {
                "module_display": {
                    "enabled": True,
                    "width": width,
                    "height": height,
                    "refresh_rate": refresh_rate,
                    "output_width": 0,  # 0 default
                    "output_height": 0,
                    "scale_w": scale_w,  # intger
                    "scale_h": scale_h,
                    "pixel_clock": pixel_clock,
                }
            }
        )
