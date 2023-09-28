# -*- encoding: utf-8 -*-
import M5
from driver.neopixel import NeoPixel
from driver.neopixel.ws2812 import WS2812
from driver.neopixel.sk6812 import SK6812


class RGB:
    _instance = None
    _io = None
    _n = 0
    _type = ""

    def __new__(cls, **kwargs) -> NeoPixel:
        if len(kwargs) > 0:
            try:
                cls._io = kwargs["io"]
                cls._n = kwargs["n"]
                cls._type = kwargs["type"]
            except KeyError:
                raise KeyError("expect 'io=', 'n=' and 'type=' K-V parameter")

        # If provided the specified io, we don't care board type
        if (cls._io is not None) and (cls._n > 0):
            if "sk6812" in cls._type.lower():
                return SK6812(io=cls._io, n=cls._n)
            else:
                return WS2812(io=cls._io, n=cls._n)  # default

        # If not provided any io, according to board type, initialize the built-in rgb
        board_id = M5.getBoard()
        if cls._instance == None:
            if M5.BOARD.M5AtomS3 == board_id:
                pass
            elif board_id in (M5.BOARD.M5AtomS3Lite, M5.BOARD.M5AtomS3U):
                cls._instance = WS2812(io=35, n=1)
                return cls._instance
            elif board_id in (M5.BOARD.M5StampS3, M5.BOARD.M5Capsule):
                cls._instance = WS2812(io=21, n=1)
                return cls._instance
            else:
                pass
        else:
            return cls._instance
