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

    def __new__(
        cls,
        port: tuple = (36, 26),
        width: int = 1280,
        height: int = 720,
        refresh_rate: int = 60,
        output_width: int = 1280,
        output_height: int = 720,
        scale_w: int = 1,
        scale_h: int = 1,
        pixel_clock: int = 74250000,
    ) -> None:
        """! Initialize the Module Display

        @param port The port to which the Module Display is connected. port[0]: not used, port[1]: dac pin.
        @param width The width of the Module Display.
        @param height The height of the Module Display.
        @param refresh_rate The refresh rate of the Module Display.
        @param output_width The width of the output of the Module Display.
        @param output_height The height of the output of the Module Display.
        @param scale_w The scale width of the Module Display.
        @param scale_h The scale height of the Module Display.
        @param pixel_clock The pixel clock of the Module Display.

        """
        return M5.addDisplay(
            None,
            0,
            {
                "module_display": {
                    "enabled": True,
                    # see to M5ModuleDisplay::config_t
                    "width": width,
                    "height": height,
                    "refresh_rate": refresh_rate,
                    "output_width": output_width,
                    "output_height": output_height,
                    "scale_w": scale_w,
                    "scale_h": scale_h,
                    "pixel_clock": pixel_clock,
                }
            },
        )
