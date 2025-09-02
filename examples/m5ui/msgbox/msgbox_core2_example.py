# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
msgbox0 = None
label_sfu = None
btn_apply = None
btn_cancel = None


import random


def btn_apply_clicked_event(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    label_sfu.set_text(str((str("Hello ") + str((random.randint(1, 100))))))


def btn_cancel_clicked_event(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    btn_apply.toggle_flag(lv.obj.FLAG.HIDDEN)


def btn_apply_event_handler(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_apply_clicked_event(event_struct)
    return


def btn_cancel_event_handler(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_cancel_clicked_event(event_struct)
    return


def setup():
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    msgbox0 = m5ui.M5Msgbox(title="Message Box", x=0, y=0, w=320, h=240, parent=page0)
    label_sfu = msgbox0.add_text("This is label_sfu")
    btn_apply = msgbox0.add_button(text="Apply", option="footer")
    btn_cancel = msgbox0.add_button(text="Cancel", option="footer")
    msgbox0.add_close_button()

    btn_apply.add_event_cb(btn_apply_event_handler, lv.EVENT.ALL, None)
    btn_cancel.add_event_cb(btn_cancel_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
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
