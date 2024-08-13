# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *


label0 = None
rotary = None


def btnA_wasClicked_event(state):  # noqa: N802
    global label0, rotary
    rotary.reset_rotary_value()
    label0.setText(str(rotary.get_rotary_value()))


def setup():
    global label0, rotary

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("0", 96, 80, 1.0, 0xFFA000, 0x222222, Widgets.FONTS.DejaVu72)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    rotary = Rotary()


def loop():
    global label0, rotary
    M5.update()
    if rotary.get_rotary_status():
        label0.setText(str(rotary.get_rotary_value()))


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
