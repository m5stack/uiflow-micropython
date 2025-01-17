# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time


label0 = None
label1 = None
label2 = None
label3 = None


def setup():
    global label0, label1, label2, label3

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("GMT-0 time:", 2, 20, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 2, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("GMT-2 time:", 2, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 2, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    time.timezone("GMT0")
    label1.setText(str(time.localtime()))
    time.timezone("GMT-8")
    label3.setText(str(time.localtime()))


def loop():
    global label0, label1, label2, label3
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
