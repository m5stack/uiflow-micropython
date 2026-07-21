# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lt6911


class DisplayIn:
    """Capture the Unit PoE-P4 HDMI input as JPEG images.

    ``DisplayIn`` initializes the LT6911 HDMI receiver. Call :meth:`capture`
    to save one captured frame, then call :meth:`deinit` when capture is no
    longer needed.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from addon import DisplayIn

            display_in = DisplayIn()
            size = display_in.capture("/flash/capture.jpg", quality=75)
            display_in.deinit()
    """

    def __init__(self) -> None:
        """Initialize the Unit PoE-P4 HDMI input."""
        lt6911.init()

    def capture(self, path: str, quality: int = 75, timeout_ms: int = 1000) -> int:
        """Capture one HDMI frame and save it as a JPEG file.

        :param str path: Destination JPEG file path.
        :param int quality: JPEG quality from ``1`` to ``100``. Default is ``75``.
        :param int timeout_ms: Maximum frame wait time in milliseconds. Default is ``1000``.
        :returns: Number of bytes written to ``path``.
        :rtype: int
        """
        return lt6911.capture(path, quality=quality, timeout_ms=timeout_ms)

    def deinit(self) -> None:
        """Release the Unit PoE-P4 HDMI input resources."""
        lt6911.deinit()
