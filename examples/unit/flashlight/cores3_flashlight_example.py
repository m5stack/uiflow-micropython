# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import FlashLightUnit
import time


flashlight_0 = None


def setup():
    global flashlight_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    flashlight_0 = FlashLightUnit((8, 9))


def loop():
    global flashlight_0
    M5.update()
    flashlight_0.flash(flashlight_0.BRIGHTNESS_100, flashlight_0.TIME_220MS, True)
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
