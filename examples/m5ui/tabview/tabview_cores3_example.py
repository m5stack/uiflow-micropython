# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
tabview0 = None
Tab1 = None
Tab2 = None
label1 = None
label2 = None
label3 = None


def setup():
    global page0, tabview0, Tab1, Tab2, label1, label2, label3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    tabview0 = m5ui.M5TabView(
        x=0, y=-2, w=320, h=240, bar_size=60, bar_pos=lv.DIR.TOP, parent=page0
    )
    Tab1 = tabview0.add_tab("Tab1")
    Tab2 = tabview0.add_tab("Tab2")
    label1 = m5ui.M5Label("This is label1", x=0, y=0, parent=Tab1)

    page0.screen_load()
    label2 = m5ui.M5Label(
        "Hello World",
        x=0,
        y=0,
        text_c=0xFFCC00,
        bg_c=0x99FF99,
        bg_opa=255,
        font=lv.font_montserrat_24,
        parent=Tab1,
    )
    label3 = m5ui.M5Label("hello M5", x=0, y=0, parent=Tab2)
    label3.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
    label3.set_text_color(0x6600CC, 255, 0)
    label3.set_bg_color(0x33FF33, 255, 0)


def loop():
    global page0, tabview0, Tab1, Tab2, label1, label2, label3
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
