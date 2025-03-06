# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicDisplayBase


label0 = None
label1 = None
base_display = None


def setup():
    global label0, label1, base_display

    M5.begin()
    label1 = Widgets.Label("M5Stack", 23, 53, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    base_display = AtomicDisplayBase(
        width=1280,
        height=720,
        refresh_rate=60,
        output_width=1280,
        output_height=720,
        scale_w=1,
        scale_h=1,
        pixel_clock=74250000,
    )
    label0 = Widgets.Label(
        "M5STACK", 466, 318, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu72, base_display
    )


def loop():
    global label0, label1, base_display
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
