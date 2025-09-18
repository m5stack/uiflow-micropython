# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from label_plus import LabelPlus


label_plus0 = None


en = None


def btnPWR_wasClicked_event(state):  # noqa: N802
    global label_plus0, en
    en = not en
    if en:
        label_plus0.set_update_enable(True)
    else:
        label_plus0.set_update_enable(False)


def setup():
    global label_plus0, en

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label_plus0 = LabelPlus(
        "label_plus0",
        24,
        31,
        1.0,
        0xFFFFFF,
        0x222222,
        Widgets.FONTS.DejaVu18,
        "http://192.168.8.200:8000/data",
        3000,
        True,
        "data",
        "error",
        0xFF0000,
    )

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)

    en = True


def loop():
    global label_plus0, en
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
