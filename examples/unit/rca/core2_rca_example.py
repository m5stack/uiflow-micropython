# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import RCAUnit


label0 = None
label1 = None
rca_0 = None


def setup():
    global label0, label1, rca_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Core2", 133, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    rca_0 = RCAUnit(
        (36, 26),
        216,
        144,
        output_width=0,
        output_height=0,
        signal_type=RCAUnit.NTSC,
        use_psram=0,
        output_level=0,
    )
    label1 = Widgets.Label("RCA", 88, 61, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, rca_0)


def loop():
    global label0, label1, rca_0
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
