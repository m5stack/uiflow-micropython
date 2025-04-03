# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import RF433TUnit


title0 = None
label0 = None
label_cnt = None
rf433t_0 = None
cnt = None
tx_buf = None


def btnPWR_wasClicked_event(state):
    global title0, label0, label_cnt, rf433t_0, cnt, tx_buf
    cnt = cnt + 1
    tx_buf[-1] = cnt
    rf433t_0.send(tx_buf)
    label_cnt.setText(str((str("Count: ") + str(cnt))))


def setup():
    global title0, label0, label_cnt, rf433t_0, cnt, tx_buf
    M5.begin()
    title0 = Widgets.Title("RF433T Send Data", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label(
        "Press Power Button Send", 41, 54, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_cnt = Widgets.Label("Count", 115, 118, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)
    rf433t_0 = RF433TUnit((8, 9))
    tx_buf = bytearray(3)
    tx_buf[-1] = 0
    tx_buf[0] = 0
    cnt = 0
    tx_buf[-1] = cnt


def loop():
    global title0, label0, label_cnt, rf433t_0, cnt, tx_buf
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
