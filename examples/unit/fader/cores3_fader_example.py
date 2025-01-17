# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import FaderUnit


label0 = None
label1 = None
label2 = None
label3 = None
fader_0 = None


def setup():
    global label0, label1, label2, label3, fader_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Voltage:", 50, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ADC:", 50, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 160, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 160, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    fader_0 = FaderUnit((8, 9))


def loop():
    global label0, label1, label2, label3, fader_0
    M5.update()
    fader_0.update_color()
    label2.setText(str(fader_0.get_voltage()))
    label3.setText(str(fader_0.get_raw()))


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
