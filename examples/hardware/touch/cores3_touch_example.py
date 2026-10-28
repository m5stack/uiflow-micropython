# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *


label0 = None
label1 = None


cur_x = None
cur_y = None


def setup():
    global label0, label1, cur_x, cur_y

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("x: 0", 32, 41, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("y: 0", 33, 84, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)


def loop():
    global label0, label1, cur_x, cur_y
    M5.update()
    if M5.Touch.getCount():
        cur_x = M5.Touch.getX()
        cur_y = M5.Touch.getY()
        label0.setText(str((str("x: ") + str(cur_x))))
        label1.setText(str((str("y: ") + str(cur_y))))


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
