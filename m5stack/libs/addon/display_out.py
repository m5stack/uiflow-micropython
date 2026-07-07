# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5


class DisplayOut:
    """Create an HDMI display output for Unit PoE-P4.

    ``DisplayOut`` registers the Unit PoE-P4 HDMI output as an M5 display and
    returns the display object created by ``M5.addDisplay``. The display can
    then be used by the standard M5 display APIs.

    :param int width: The logical width of the HDMI output. Default is ``1280``.
    :param int height: The logical height of the HDMI output. Default is ``720``.
    :param int refresh_rate: The refresh rate of the HDMI output in Hz. Default is ``60``.
    :returns: The display object registered by ``M5.addDisplay``.
    :rtype: object

    .. note::

        Unit PoE-P4 HDMI output supports ``1280x720@60Hz`` and
        ``1920x1080@30Hz`` timings.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from addon import DisplayOut

            display = DisplayOut(1280, 720, 60)
    """

    def __new__(
        cls,
        width: int = 1280,
        height: int = 720,
        refresh_rate: int = 60,
    ) -> object:
        return M5.addDisplay(
            None,
            0,
            {
                "unit_poep4_hdmi": {
                    "enabled": True,
                    # Keep these keys aligned with unit_poep4_hdmi::config_t.
                    "width": width,
                    "height": height,
                    "refresh_rate": refresh_rate,
                }
            },
        )
