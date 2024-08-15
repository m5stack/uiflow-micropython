# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import PLUSModule


title0 = None
label2 = None
label0 = None
label1 = None
plus_0 = None


btn_state = None
last_btn_state = None


def setup():
    global title0, label2, label0, label1, plus_0, btn_state, last_btn_state

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("PLUS Core2 Test", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Btn rotray:", 1, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Rotary:", 1, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Rotary Inc:", 1, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    plus_0 = PLUSModule(address=0x62)
    plus_0.set_rotary_value(0)


def loop():
    global title0, label2, label0, label1, plus_0, btn_state, last_btn_state
    M5.update()
    btn_state = plus_0.get_button_status()
    label0.setText(str((str("Rotary:") + str((plus_0.get_rotary_value())))))
    label2.setText(str((str("Btn rotray:") + str(btn_state))))
    if btn_state and btn_state != last_btn_state:
        label1.setText(str((str("Rotary Inc:") + str((plus_0.get_rotary_increments())))))
    last_btn_state = btn_state


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
