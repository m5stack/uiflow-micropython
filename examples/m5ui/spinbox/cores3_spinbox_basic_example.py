# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
spinbox0 = None
label0 = None


def spinbox0_value_changed_event(event_struct):
    global page0, spinbox0, label0
    label0.set_text(str(spinbox0.get_value()))


def spinbox0_event_handler(event_struct):
    global page0, spinbox0, label0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        spinbox0_value_changed_event(event_struct)
    return


def setup():
    global page0, spinbox0, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    spinbox0 = m5ui.M5Spinbox(
        x=60,
        y=100,
        w=200,
        h=40,
        value=50,
        min_value=0,
        max_value=100,
        digit_count=5,
        prec=2,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=138,
        y=166,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    spinbox0.add_event_cb(spinbox0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    spinbox0.set_border_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def loop():
    global page0, spinbox0, label0
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
