import os, sys, io
import time

import M5
from M5 import *
from unit import SimpleDualButtonUnit


blue = None
red = None


def setup():
    global blue, red

    M5.begin()
    Widgets.fillScreen(0x222222)

    blue, red = SimpleDualButtonUnit((36, 26))


def loop():
    global blue, red
    M5.update()
    blue.update()
    red.update()

    if blue.was_pressed():
        print("blue pressed, pin value:", blue.value())
    if blue.was_released():
        print("blue released, active:", blue.is_active())

    if red.was_pressed():
        print("red pressed, pin value:", red.value())
    if red.was_released():
        print("red released, active:", red.is_active())

    time.sleep_ms(10)


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
