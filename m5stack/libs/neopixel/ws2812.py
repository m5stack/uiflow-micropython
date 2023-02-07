# WS2812 dreiver
from . import NeoPixel
from machine import Pin


class WS2812(NeoPixel):
    # G R B W
    ORDER = (1, 0, 2, 3)

    def __init__(self, pin, n, bpp=3, timing=1):
        io = Pin(pin)
        self.br = 1.0
        super().__init__(pin=io, n=n, bpp=bpp, timing=timing)
