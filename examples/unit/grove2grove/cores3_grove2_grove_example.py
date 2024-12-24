# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import Grove2GroveUnit


label0 = None
label1 = None
grove2grove_0 = None


def setup():
    global label0, label1, grove2grove_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("current:", 50, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 150, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    grove2grove_0 = Grove2GroveUnit((8, 9))
    grove2grove_0.on()


def loop():
    global label0, label1, grove2grove_0
    M5.update()
    label1.setText(str(grove2grove_0.get_current()))


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
