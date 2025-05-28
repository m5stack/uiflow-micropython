# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
button0 = None
label0 = None


def button0_pressed_event(event_struct):
    global page0, button0, label0

    label0.set_text(str("pressed"))


def button0_released_event(event_struct):
    global page0, button0, label0

    label0.set_text(str("released"))


def button0_event_handler(event_struct):
    global page0, button0, label0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        button0_released_event(event_struct)
    return


def setup():
    global page0, button0, label0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Screen(bg_c=0xFFFFFF)
    button0 = m5ui.M5Button(
        text="click me",
        x=117,
        y=102,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=136,
        y=33,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, button0, label0
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
