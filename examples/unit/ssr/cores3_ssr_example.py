# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import SSRUnit
import time


ssr_0 = None


def setup():
    global ssr_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    ssr_0 = SSRUnit((8, 9))


def loop():
    global ssr_0
    M5.update()
    ssr_0.set_state(1)
    time.sleep(1)
    ssr_0.off()
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
