# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import FingerHat


label0 = None
hat_finger_0 = None


def setup():
    global label0, hat_finger_0

    M5.begin()
    label0 = Widgets.Label("label0", 4, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    hat_finger_0 = FingerHat(1, (26, 0))


def loop():
    global label0, hat_finger_0
    M5.update()
    label0.setText(str(hat_finger_0.get_user_list()))


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
