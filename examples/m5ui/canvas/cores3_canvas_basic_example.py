# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
canvas0 = None


def setup():
    global page0, canvas0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    canvas0 = m5ui.M5Canvas(
        x=83,
        y=53,
        w=150,
        h=70,
        color_format=lv.COLOR_FORMAT.ARGB8888,
        bg_c=0xC9C9C9,
        bg_opa=255,
        parent=page0,
    )

    page0.screen_load()
    canvas0.draw_arc(0, 0, 10, color=0x6600CC, opa=255, width=2, start_angle=0, end_angle=90)
    canvas0.draw_rect(
        0,
        0,
        20,
        20,
        0,
        bg_c=0xFF0000,
        bg_opa=255,
        border_c=0xFF0000,
        border_opa=255,
        border_w=0,
        border_side=lv.BORDER_SIDE.FULL,
        outline_c=0x6600CC,
        outline_opa=255,
        outline_w=0,
        outline_pad=0,
        shadow_c=0x6600CC,
        shadow_opa=255,
        shadow_w=0,
        shadow_offset_x=0,
        shadow_offset_y=0,
        shadow_spread=0,
    )
    canvas0.draw_line(0, 0, 50, 50, color=0x6600CC, opa=255, width=1)


def loop():
    global page0, canvas0
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
