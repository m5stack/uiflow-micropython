# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *


label0 = None


def setup():
    global label0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 38, 47, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    label0.setText(str("Label"))
    label0.setFont(Widgets.FONTS.DejaVu12)


def loop():
    global label0
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
