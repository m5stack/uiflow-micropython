# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CatchUnit
import time


catch_0 = None


import random


def setup():
    global catch_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    catch_0 = CatchUnit((8, 9))


def loop():
    global catch_0
    M5.update()
    catch_0.set_clamp_percent(random.randint(1, 100))
    time.sleep_ms(100)


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
