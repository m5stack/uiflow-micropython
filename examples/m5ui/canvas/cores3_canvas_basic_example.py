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


y = None
x = None


def setup():
    global page0, canvas0, x, y

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    canvas0 = m5ui.M5Canvas(
        x=120,
        y=100,
        w=80,
        h=40,
        color_format=lv.COLOR_FORMAT.ARGB8888,
        bg_c=0x4994EC,
        bg_opa=255,
        parent=page0,
    )

    page0.set_bg_color(0xFFCCCC, 255, 0)
    page0.screen_load()
    for y in range(10, 21):
        for x in range(5, 76):
            canvas0.set_px(x, y, 0x4994EC, 50)
    for y in range(20, 31):
        for x in range(5, 76):
            canvas0.set_px(x, y, 0x4994EC, 20)
    for y in range(30, 41):
        for x in range(5, 76):
            canvas0.set_px(x, y, 0x4994EC, 0)


def loop():
    global page0, canvas0, x, y
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
