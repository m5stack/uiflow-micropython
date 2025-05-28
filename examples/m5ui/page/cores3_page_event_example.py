# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None


def page0_pressed_event(event_struct):
    global page0

    page0.set_bg_color(0x000000, 255, 0)


def page0_released_event(event_struct):
    global page0

    page0.set_bg_color(0xFFFFFF, 255, 0)


def page0_clicked_event(event_struct):
    global page0

    page0.set_bg_color(0x000000, 255, 0)


def page0_long_pressed_event(event_struct):
    global page0

    page0.set_bg_color(0x000000, 255, 0)


def page0_event_handler(event_struct):
    global page0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        page0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        page0_released_event(event_struct)
    if event == lv.EVENT.CLICKED and True:
        page0_clicked_event(event_struct)
    if event == lv.EVENT.LONG_PRESSED and True:
        page0_long_pressed_event(event_struct)
    return


def setup():
    global page0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Screen(bg_c=0xFFFFFF)

    page0.add_event_cb(page0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0
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
