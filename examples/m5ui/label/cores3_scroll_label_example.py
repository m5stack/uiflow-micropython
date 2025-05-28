# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
label0 = None


def setup():
    global page0, label0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Screen(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "It is a circularly scrolling text. ",
        x=60,
        y=110,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    label0.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
    label0.set_width(150)
    label0.align_to(page0, lv.ALIGN.CENTER, 0, 0)


def loop():
    global page0, label0
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
