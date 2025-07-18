# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
line0 = None


def setup():
    global page0, line0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    line0 = m5ui.M5Line(
        points=[5, 5, 70, 70, 120, 10, 180, 60, 190, 70, 200, 80, 210, 90, 220, 100],
        width=7,
        color=0x2196F3,
        rounded=True,
        parent=page0,
    )

    page0.screen_load()


def loop():
    global page0, line0
    M5.update()
    if M5.Touch.getCount():
        line0.add_point(M5.Touch.getX(), M5.Touch.getY())


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
