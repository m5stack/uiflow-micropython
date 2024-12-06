# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LIMITUnit


title0 = None
label1 = None
label0 = None
limit_0 = None


def setup():
    global title0, label1, label0, limit_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LimitUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Button State:", 395, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Limit Counter Value:", 1, 102, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    limit_0 = LIMITUnit((33, 32), True, type=2)
    limit_0.count_reset()


def loop():
    global title0, label1, label0, limit_0
    M5.update()
    label0.setText(str((str("Limit Counter Value:") + str((limit_0.count_value)))))


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
