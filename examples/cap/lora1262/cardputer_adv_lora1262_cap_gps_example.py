# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from cap import GPSCap


label0 = None
label1 = None
label2 = None
cap_lora1262 = None


def setup():
    global label0, label1, label2, cap_lora1262

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("label0", 11, 16, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 11, 46, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 10, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    cap_lora1262 = GPSCap(id=2)


def loop():
    global label0, label1, label2, cap_lora1262
    M5.update()
    label0.setText(str(cap_lora1262.get_latitude()))
    label1.setText(str(cap_lora1262.get_longitude()))
    label2.setText(str(cap_lora1262.get_gps_time()))


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
