# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *


label_title = None
label_btna_cnt = None
label_btnb_cnt = None
label_tip = None
btna_cnt = None
btnb_cnt = None


def btna_click_event_cb(state):
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    btna_cnt = (btna_cnt if isinstance(btna_cnt, (int, float)) else 0) + 1
    label_btna_cnt.setText(str((str("BtnA: ") + str(btna_cnt))))
    print("button a press")


def btnb_click_event_cb(state):
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    btnb_cnt = (btnb_cnt if isinstance(btnb_cnt, (int, float)) else 0) + 1
    label_btnb_cnt.setText(str((str("BtnB: ") + str(btnb_cnt))))
    print("button b press")


def setup():
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Button", 35, 5, 1.0, 0x1A94DD, 0x000000, Widgets.FONTS.DejaVu18)
    label_btna_cnt = Widgets.Label(
        "BtnA: ", 5, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_btnb_cnt = Widgets.Label("BtnB:", 5, 80, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "Press button", 7, 200, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_click_event_cb)
    btna_cnt = 0
    btnb_cnt = 0


def loop():
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
