# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
textarea0 = None
keyboard0 = None


def textarea0_focused_event(event_struct):
    global page0, textarea0, keyboard0
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)


def textarea0_defocused_event(event_struct):
    global page0, textarea0, keyboard0
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)


def textarea0_event_handler(event_struct):
    global page0, textarea0, keyboard0
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return


def setup():
    global page0, textarea0, keyboard0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=10,
        y=30,
        w=300,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=120,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=textarea0,
        parent=page0,
    )

    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, textarea0, keyboard0
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
