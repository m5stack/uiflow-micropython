# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class RCAModule:
    """Initialize the RCA Module.

    :param int pin: The dac pin to which the RCA Module is connected.
    :param int width: The width of the RCA display.
    :param int height: The height of the RCA display.
    :param int output_width: The width of the output of the RCA display.
    :param int output_height: The height of the output of the RCA display.
    :param int signal_type: The signal type of the RCA display. NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4.
    :param int use_psram: The use of psram of the RCA display.
    :param int output_level: The output level of the RCA display.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import RCAModule
            module_rca = RCAModule(26, width=216, height=144, output_width=0, output_height=0, signal_type=RCAModule.NTSC, use_psram=0, output_level=0)
    """

    NTSC = 0
    """signal type. National Television System Committee."""

    NTSC_J = 1
    """signal type. National Television System Committee Japan."""

    PAL = 2
    """signal type. Phase Alternating Line."""

    PAL_M = 3
    """signal type. Phase Alternating Line M."""

    PAL_N = 4
    """signal type. Phase Alternating Line N."""

    def __new__(
        cls,
        pin: int = 26,
        width: int = 216,
        height: int = 144,
        output_width: int = 216,
        output_height: int = 144,
        signal_type: int = NTSC,
        use_psram: int = 0,
        output_level: int = 0,
    ) -> None:
        return M5.addDisplay(
            None,
            0,
            {
                "module_rca": {
                    "enabled": True,
                    # see to M5ModuleRCA::config_t
                    "width": width,
                    "height": height,
                    "output_width": output_width,
                    "output_height": output_height,
                    "signal_type": signal_type,
                    "use_psram": use_psram,
                    "pin_dac": pin,
                    "output_level": output_level,
                }
            },
        )
