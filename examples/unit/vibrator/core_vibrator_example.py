# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import VibratorUnit


label0 = None
vibrator_0 = None


def btnB_wasClicked_event(state):  # noqa: N802
    global label0, vibrator_0
    vibrator_0.once(freq=1000, duty=15, duration=50)


def setup():
    global label0, vibrator_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("play", 127, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)

    vibrator_0 = VibratorUnit((36, 26))


def loop():
    global label0, vibrator_0
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
