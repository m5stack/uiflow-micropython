# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
dropdown0 = None
dropdown1 = None
dropdown2 = None
dropdown3 = None


def setup():
    global page0, dropdown0, dropdown1, dropdown2, dropdown3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    dropdown0 = m5ui.M5Dropdown(
        x=110,
        y=0,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.BOTTOM,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown1 = m5ui.M5Dropdown(
        x=111,
        y=212,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.TOP,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown2 = m5ui.M5Dropdown(
        x=220,
        y=106,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.LEFT,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown3 = m5ui.M5Dropdown(
        x=0,
        y=106,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.RIGHT,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    dropdown0.set_selected_highlight(True)
    dropdown1.set_selected_highlight(True)
    dropdown2.set_selected_highlight(True)
    dropdown3.set_selected_highlight(True)


def loop():
    global page0, dropdown0, dropdown1, dropdown2, dropdown3
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
