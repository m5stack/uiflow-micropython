# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
scale0 = None


def setup():
    global page0, scale0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    scale0 = m5ui.M5Scale(
        x=7,
        y=92,
        w=300,
        h=0,
        start_pos=0,
        end_pos=100,
        tick_count=11,
        tick_every=2,
        show_mode=lv.scale.MODE.HORIZONTAL_TOP,
        parent=page0,
    )

    page0.screen_load()
    scale0.set_style_line_width(2, lv.PART.MAIN)
    scale0.set_line_color(0x6600CC, 255, lv.PART.MAIN)
    scale0.set_style_line_width(4, lv.PART.INDICATOR)
    scale0.set_line_color(0xFF9900, 255, lv.PART.INDICATOR)
    scale0.set_style_line_width(6, lv.PART.ITEMS)
    scale0.set_line_color(0x66FF99, 255, lv.PART.ITEMS)


def loop():
    global page0, scale0
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
