# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
spinner0 = None


def setup():
    global page0, spinner0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    spinner0 = m5ui.M5Spinner(
        x=71,
        y=81,
        w=100,
        h=100,
        anim_t=10000,
        angle=180,
        bg_c=0xE7E3E7,
        bg_c_indicator=0x2193F3,
        parent=page0,
    )

    page0.screen_load()


def loop():
    global page0, spinner0
    M5.update()


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
