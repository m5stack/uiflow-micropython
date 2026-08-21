import os, sys, io
import M5
from M5 import *
from unit import SimpleDualButtonUnit
import time


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

    if blue.is_active():
        print("blue held down")
    if blue.was_pressed():
        print("blue just pressed")
    if blue.was_released():
        print("blue just released")

    if red.is_active():
        print("red held down")
    if red.was_pressed():
        print("red just pressed")
    if red.was_released():
        print("red just released")

    time.sleep(0.05)


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
