# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
window0 = None
btn_lav = None
title_fmk = None
btn_nzk = None
btn_dkc = None
label_wgy = None


def btn_lav_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    label_wgy.set_text(str("Left Btn was clicked"))


def btn_nzk_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    label_wgy.set_text(str("Right Btn was clicked"))


def btn_dkc_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    window0.set_flag(lv.obj.FLAG.HIDDEN, True)


def btn_lav_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_lav_clicked_event(event_struct)
    return


def btn_nzk_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_nzk_clicked_event(event_struct)
    return


def btn_dkc_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_dkc_clicked_event(event_struct)
    return


def setup():
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    window0 = m5ui.M5Win(x=0, y=0, w=320, h=240, parent=page0)
    btn_lav = window0.add_button(icon=lv.SYMBOL.LEFT, w=40)
    title_fmk = window0.add_title("This is a window")
    btn_nzk = window0.add_button(icon=lv.SYMBOL.RIGHT, w=40)
    btn_dkc = window0.add_button(icon=lv.SYMBOL.CLOSE, w=60)
    label_wgy = window0.add_text("This is label_wgy", x=0, y=0)

    btn_lav.add_event_cb(btn_lav_event_handler, lv.EVENT.ALL, None)
    btn_nzk.add_event_cb(btn_nzk_event_handler, lv.EVENT.ALL, None)
    btn_dkc.add_event_cb(btn_dkc_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
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
