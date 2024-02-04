import os, sys, io
import M5
from M5 import *
from unit import RGBUnit


rgb_0 = None


def setup():
    global rgb_0

    rgb_0 = RGBUnit((36, 26), 3)
    M5.begin()
    Widgets.fillScreen(0x222222)

    rgb_0.set_brightness(80)
    rgb_0.fill_color(0xFF0000)
    rgb_0.set_color(0, 0x33FF33)


def loop():
    global rgb_0
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
