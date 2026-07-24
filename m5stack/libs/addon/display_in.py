# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lt6911


class DisplayIn:
    """Capture HDMI input from the Display In Add-on (U220) as JPEG images.

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
        """Initialize the Display In Add-on (U220) HDMI input.

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                display_in = DisplayIn()
        """
        lt6911.init()

    def capture(self, path: str, quality: int = 75, timeout_ms: int = 1000) -> int:
        """Capture one HDMI frame and save it as a JPEG file.

        :param str path: Destination JPEG file path.
        :param int quality: JPEG quality from ``1`` to ``100``. Default is ``75``.
        :param int timeout_ms: Maximum frame wait time in milliseconds. Default is ``1000``.
        :returns: Number of bytes written to ``path``.
        :rtype: int

        UiFlow2 Code Block:

            |capture.png|

        MicroPython Code Block:

            .. code-block:: python

                size = display_in.capture("/flash/capture.jpg", quality=75)
        """
        return lt6911.capture(path, quality=quality, timeout_ms=timeout_ms)

    def deinit(self) -> None:
        """Release the Display In Add-on (U220) HDMI input resources.

        UiFlow2 Code Block:

            |deinit.png|

        MicroPython Code Block:

            .. code-block:: python

                display_in.deinit()
        """
        lt6911.deinit()
