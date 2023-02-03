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
            elif M5.BOARD.unknown == M5.getBoard():  # temporary for AtomS3-Lite
                cls._instance = WS2812(35, 1)
                return cls._instance
        else:
            return cls._instance

    def __init__(self) -> None:
        pass
