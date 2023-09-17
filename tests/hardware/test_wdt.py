import os, sys, io
import M5
from M5 import *
from hardware import *
import time


label0 = None
wdt = None


count = None


def setup():
    global label0, wdt, count

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 39, 34, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wdt = WDT(timeout=5000)
    count = (count if isinstance(count, (int, float)) else 0) + 0
    label0.setText(str(count))


def loop():
    global label0, wdt, count
    M5.update()
    time.sleep(4)
    wdt.feed()
    count = 1 + count
    label0.setText(str(count))


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
