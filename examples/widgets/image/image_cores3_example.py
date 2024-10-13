# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *


image0 = None
title0 = None


def setup():
    global image0, title0

    M5.begin()
    Widgets.fillScreen(0x222222)
    image0 = Widgets.Image("res/img/SCR-20240902-itcy.png", 71, 64)
    title0 = Widgets.Title("Image CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    image0.setImage("res/img/default.png")
    image0.setImage("res/img/SCR-20240902-itcy.png")
    image0.setCursor(x=0, y=0)
    image0.setVisible(True)


def loop():
    global image0, title0
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
