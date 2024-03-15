# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# SK6812 dreiver
from . import NeoPixel
from machine import Pin


class SK6812(NeoPixel):
    # G R B W
    ORDER = (1, 0, 2, 3)

    def __init__(self, io: int, n: int, bpp: int = 3, timing: int = 1) -> None:
        pin = Pin(io)
        self.br = 1.0
        super().__init__(pin=pin, n=n, bpp=bpp, timing=timing)
