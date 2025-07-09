# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
slider0 = None
label0 = None


def slider0_value_changed_event(event_struct):
    global page0, slider0, label0
    label0.set_text(str(slider0.get_value()))


def slider0_event_handler(event_struct):
    global page0, slider0, label0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider0_value_changed_event(event_struct)
    return


def setup():
    global page0, slider0, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    slider0 = m5ui.M5Slider(
        x=60,
        y=110,
        w=200,
        h=19,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "25",
        x=151,
        y=142,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    slider0.add_event_cb(slider0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, slider0, label0
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
