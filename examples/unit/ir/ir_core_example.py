import os, sys, io
import M5
from M5 import *
from unit import IRUnit
import time


ir_0 = None


def setup():
    global ir_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    ir_0 = IRUnit((36, 26))


def loop():
    global ir_0
    M5.update()
    ir_0.tx(0, 0)
    time.sleep(1)


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
