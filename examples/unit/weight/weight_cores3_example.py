# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import WeightUnit
import time


title0 = None
label0 = None
weight_0 = None


def setup():
    global title0, label0, weight_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "WeightUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "weight value:", 4, 113, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    weight_0 = WeightUnit(port=(8, 9))
    weight_0.set_tare()


def loop():
    global title0, label0, weight_0
    M5.update()
    label0.setText(str((str("weight value:") + str((weight_0.get_scale_weight)))))
    time.sleep_ms(100)


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
