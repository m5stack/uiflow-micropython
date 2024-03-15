# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from label_plus import LabelPlus
import time


label_plus0 = None
label0 = None
label1 = None


def setup():
    global label_plus0, label0, label1

    M5.begin()
    label_plus0 = LabelPlus(
        "Text",
        2,
        2,
        1.0,
        0xFFFFFF,
        0x222222,
        Widgets.FONTS.DejaVu18,
        "http://192.168.2.48:3000/posts/1",
        3000,
        True,
        "title",
        "error",
        0xFF0000,
    )
    label0 = Widgets.Label("Text", 2, 74, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 2, 101, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    time.sleep(5)
    label_plus0.set_update_enable(False)
    time.sleep(5)
    label_plus0.set_update_enable(True)
    time.sleep(5)
    label_plus0.set_update_period(1000)
    time.sleep(10)
    label_plus0.setCursor(x=0, y=0)
    time.sleep(10)
    label_plus0.setColor(0x00FF00)
    time.sleep(10)
    label_plus0.setSize(1.5)
    time.sleep(10)
    label_plus0.setText(str("Label"))
    time.sleep(10)
    label_plus0.setFont(Widgets.FONTS.DejaVu9)
    time.sleep(10)
    label_plus0.setVisible(False)
    time.sleep(10)
    label_plus0.setVisible(True)


def loop():
    global label_plus0, label0, label1
    M5.update()
    label0.setText(str((label_plus0.get_data())))
    label1.setText(str((label_plus0.is_valid_data())))


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
