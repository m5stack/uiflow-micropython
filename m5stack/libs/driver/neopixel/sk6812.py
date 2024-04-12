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

    def set_screen(self, color_list: int) -> None:
        for i in range(len(color_list)):
            offset = i * self.bpp
            v = None
            if self.bpp == 3:
                v = self.color_to_rgb(color_list[i])
            elif self.bpp == 4:
                v = self.color_to_wrgb(color_list[i])
            for i in range(self.bpp):
                self.buf[offset + self.ORDER[i]] = v[i]
        self.write()
