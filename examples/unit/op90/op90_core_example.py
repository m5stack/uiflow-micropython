# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import OPUnit
import time


op90_0 = None


def setup():
    global op90_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    op90_0 = OPUnit((36, 26), False, type=1)
    print(op90_0.count_value)
    time.sleep(1)
    op90_0.count_reset()
    time.sleep(1)


def loop():
    global op90_0
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
