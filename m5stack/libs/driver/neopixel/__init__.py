# NeoPixel driver for MicroPython
# MIT license; Copyright (c) 2016 Damien P. George, 2021 Jim Mussared
# Copyright (c) 2024 M5Stack Technology CO LTD

from machine import bitstream, Pin


class NeoPixel:
    # G R B W
    ORDER = (1, 0, 2, 3)

    def __init__(self, pin: Pin, n: int, bpp: int = 3, timing: int = 1) -> None:
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.init(pin.OUT)
        # Timing arg can either be 1 for 800kHz or 0 for 400kHz,
        # or a user-specified timing ns tuple (high_0, low_0, high_1, low_1).
        self.timing = (
            ((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
            if isinstance(timing, int)
            else timing
        )

    def __len__(self) -> int:
        return self.n

    def __setitem__(self, i: int, v: int) -> None:
        offset = i * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = v[i]

    def __getitem__(self, i: int) -> tuple:
        offset = i * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    def fill(self, v: int) -> None:
        b = self.buf
        l = len(self.buf)
        bpp = self.bpp
        for i in range(bpp):
            c = v[i]
            j = self.ORDER[i]
            while j < l:
                b[j] = c
                j += bpp

    def write(self) -> None:
        # BITSTREAM_TYPE_HIGH_LOW = 0
        bitstream(self.pin, 0, self.timing, self.buf)

    def color_to_rgb(self, c: int) -> tuple:
        # color: (R << 16 | G << 8 | B)
        v = []
        v.append(int(((c >> 16) & 0xFF) * self.br))  # R
        v.append(int(((c >> 8) & 0xFF) * self.br))  # G
        v.append(int(((c >> 0) & 0xFF) * self.br))  # B
        return tuple(v)

    def color_to_wrgb(self, c: int) -> tuple:
        # color: (W << 24 | R << 16 | G << 8 | B)
        v = []
        v.append(int(((c >> 16) & 0xFF) * self.br))  # R
        v.append(int(((c >> 8) & 0xFF) * self.br))  # G
        v.append(int(((c >> 0) & 0xFF) * self.br))  # B
        v.append(int(((c >> 24) & 0xFF) * self.br))  # W
        return tuple(v)

    def set_color(self, i, c: int) -> None:
        offset = i * self.bpp
        v = None
        if self.bpp == 3:
            v = self.color_to_rgb(c)
        elif self.bpp == 4:
            v = self.color_to_wrgb(c)
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = v[i]
        self.write()

    def fill_color(self, c: int) -> None:
        v = None
        if self.bpp == 3:
            v = self.color_to_rgb(c)
        elif self.bpp == 4:
            v = self.color_to_wrgb(c)
        self.fill(v)
        self.write()

    def set_brightness(self, br: int) -> None:
        b = self.buf
        self.br = br / 100.0
        for i in range(len(self.buf)):
            self.buf[i] = int(b[i] * self.br)
        self.write()
