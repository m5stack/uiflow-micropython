# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5


class StampF12:
    """Resolve Stamp FPC12 signal positions for the current Stamp host."""

    SW = 3
    IRQ = 4
    BUSY = 5
    RST = 6
    MISO = 8
    MOSI = 9
    CS = 10
    CLK = 12

    _PIN_MAPS = {
        M5.BOARD.M5StampC5: (None, None, 23, 0, 24, 25, None, 26, 27, 11, None, 12),
        M5.BOARD.M5StampC6: (None, None, 8, 0, 18, 19, None, 20, 21, 22, None, 23),
        M5.BOARD.M5StampS3Mini: (
            None,
            None,
            38,
            21,
            39,
            40,
            None,
            41,
            42,
            43,
            None,
            44,
        ),
    }

    def __init__(self):
        self._pins = self._PIN_MAPS.get(M5.getBoard())
        if self._pins is None:
            raise NotImplementedError("Stamp FPC12 is not supported on this board")

    def pin(self, position):
        """Return the GPIO number at a one-based FPC12 signal position."""
        if not 1 <= position <= len(self._pins):
            raise ValueError("position must be in range 1-12")
        pin = self._pins[position - 1]
        if pin is None:
            raise ValueError("position %d is not a GPIO signal" % position)
        return pin
