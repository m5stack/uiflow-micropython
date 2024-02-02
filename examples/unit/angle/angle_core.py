import os, sys, io
import M5
from M5 import *
from unit import AngleUnit


angle_0 = None


def setup():
    global angle_0

    angle_0 = AngleUnit((36, 26))
    M5.begin()
    Widgets.fillScreen(0x222222)


def loop():
    global angle_0
    M5.update()
    print(angle_0.get_voltage())
    print(angle_0.get_value())


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
