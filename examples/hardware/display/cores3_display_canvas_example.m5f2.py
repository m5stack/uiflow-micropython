# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *


title0 = None


def setup():
    global title0
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Display canvas example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    canvas_rmy = M5.Lcd.newCanvas(100, 100, 2, True)
    canvas_rmy.drawCircle(30, 30, 20, 0xFFFFFF)
    canvas_rmy.drawCircle(30, 50, 20, 0xFFFFFF)
    canvas_rmy.drawCircle(50, 40, 20, 0xFFFFFF)
    canvas_rmy.push(50, 30)
    print((str("colro depth: ") + str((canvas_rmy.getColorDepth()))))


def loop():
    global title0
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
