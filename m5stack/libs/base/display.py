# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class AtomicDisplayBase:
    """Initialize the Atomic Display Base.

    :param int width: The logical width of the Atomic Display Base. Default is 1280px.
    :param int height: The logical height of the Atomic Display Base. Default is 720px.
    :param int refresh_rate: The refresh rate of the Atomic Display Base. Default is 60Hz.
    :param int output_width: The width of the output of the Atomic Display Base. Default is 1280px.
    :param int output_height: The height of the output of the Atomic Display Base. Default is 720px.
    :param int scale_w: The scale width of the Atomic Display Base. Default is 1.
    :param int scale_h: The scale height of the Atomic Display Base. Default is 1.
    :param int pixel_clock: The pixel clock of the Atomic Display Base. Default is 74250000.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomicDisplayBase
            atom_display = AtomicDisplayBase(1280, 720, 60, 1280, 720, 1, 1, 74250000)
    """

    def __new__(
        cls,
        width: int = 1280,
        height: int = 720,
        refresh_rate: int = 60,
        output_width: int = 1280,
        output_height: int = 720,
        scale_w: int = 1,
        scale_h: int = 1,
        pixel_clock: int = 74250000,
    ) -> None:
        return M5.addDisplay(
            None,
            0,
            {
                "atom_display": {
                    "enabled": True,
                    # see to M5AtomDisplay::config_t
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
