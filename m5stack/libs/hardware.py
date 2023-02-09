# -*- encoding: utf-8 -*-
# hardware.py
import M5
from neopixel.ws2812 import WS2812


class RGB:
    _instance = None
    pin = None
    n = 0

    def __new__(cls, **kwargs):
        if len(kwargs) > 0:
            try:
                cls.pin = kwargs["pin"]
                cls.n = kwargs["n"]
            except KeyError:
                raise KeyError("expect 'pin=' and 'n=' as K-V parameter")

        # If provided the specified pin, we don't care board type
        if (cls.pin is not None) and (cls.n > 0):
            return WS2812(pin=cls.pin, n=cls.n)

        if cls._instance == None:
            # According to board type, initialize the built-in rgb
            if M5.BOARD.M5AtomS3 == M5.getBoard():
                pass
            elif M5.BOARD.M5AtomS3Lite == M5.getBoard():
                cls._instance = WS2812(pin=35, n=1)
                return cls._instance
            else:
                pass
        else:
            return cls._instance
