# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time


page0 = None
textarea0 = None
button0 = None


line = None


def button0_clicked_event(event_struct):
    global page0, textarea0, button0, line

    textarea0.set_text("")
    line = 1


def button0_event_handler(event_struct):
    global page0, textarea0, button0, line
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button0_clicked_event(event_struct)
    return


def setup():
    global page0, textarea0, button0, line

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="",
        placeholder="Placeholder...",
        x=19,
        y=26,
        w=266,
        h=124,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="clear text",
        x=22,
        y=172,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    line = 1


def loop():
    global page0, textarea0, button0, line
    M5.update()
    textarea0.add_text(str((str("line") + str(line))))
    time.sleep(1)
    line = (line if isinstance(line, (int, float)) else 0) + 1


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
