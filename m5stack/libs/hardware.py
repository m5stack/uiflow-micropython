# -*- encoding: utf-8 -*-
# hardware.py
import M5
from neopixel.ws2812 import WS2812


class RGB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            if M5.BOARD.M5AtomS3 == M5.getBoard():
                cls._instance = None
            elif M5.BOARD.M5AtomS3Lite == M5.getBoard():
                cls._instance = WS2812(pin=35, n=1)
                return cls._instance
            else:
                pass
        else:
            return cls._instance

    def __init__(self) -> None:
        pass
