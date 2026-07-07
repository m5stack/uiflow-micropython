# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from addon import DisplayOut


title = None
circle0 = None
rect0 = None
label0 = None
line0 = None
triangle0 = None
addon_display_out_0 = None


def setup():
    global title, circle0, rect0, label0, line0, triangle0, addon_display_out_0

    M5.begin()
    addon_display_out_0 = DisplayOut(1280, 720, 60)
    Widgets.fillScreen(0x000000, addon_display_out_0)
    title = Widgets.Title(
        "addon Display Out For PoE-P4 Example",
        3,
        0xFFFFFF,
        0x0000FF,
        Widgets.FONTS.Montserrat18,
        addon_display_out_0,
    )
    circle0 = Widgets.Circle(118, 182, 68, 0xFFFFFF, 0xFFFFFF, addon_display_out_0)
    rect0 = Widgets.Rectangle(885, 338, 217, 217, 0xFFFFFF, 0xFFFFFF, addon_display_out_0)
    label0 = Widgets.Label(
        "label0",
        556,
        149,
        1.0,
        0xFFFFFF,
        0x222222,
        Widgets.FONTS.Montserrat18,
        addon_display_out_0,
    )
    line0 = Widgets.Line(398, 446, 448, 446, 0xFFFFFF, addon_display_out_0)
    triangle0 = Widgets.Triangle(
        765, 346, 735, 376, 794, 376, 0xFFFFFF, 0xFFFFFF, addon_display_out_0
    )


def loop():
    global title, circle0, rect0, label0, line0, triangle0, addon_display_out_0
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
