# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time


circle0 = None
title0 = None


import random


def setup():
    global circle0, title0

    M5.begin()
    Widgets.fillScreen(0x222222)
    circle0 = Widgets.Circle(63, 111, 15, 0xFFFFFF, 0xFFFFFF)
    title0 = Widgets.Title("Circle Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    circle0.setVisible(True)


def loop():
    global circle0, title0
    M5.update()
    circle0.setRadius(r=(random.randint(1, 30)))
    circle0.setColor(
        color=0x000000,
        fill_c=(random.randint(0, 255) << 16)
        | (random.randint(0, 255) << 8)
        | random.randint(0, 255),
    )
    circle0.setCursor(x=(random.randint(1, 320)), y=(random.randint(1, 240)))
    time.sleep(0.5)


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
