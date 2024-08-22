# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
import time


title0 = None
label0 = None
label1 = None
pin6 = None
pin7 = None


def setup():
    global title0, label0, label1, pin6, pin7

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Pin example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Pin 6 State:", 1, 83, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Pin 7 State:", 1, 132, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pin6 = Pin(6, mode=Pin.OUT)
    pin7 = Pin(7, mode=Pin.IN)


def loop():
    global title0, label0, label1, pin6, pin7
    M5.update()
    pin6.value(1)
    label0.setText(str((str("Pin 6 State:") + str((pin6.value())))))
    time.sleep(1)
    pin6.value(0)
    label0.setText(str((str("Pin 6 State:") + str((pin6.value())))))
    time.sleep(1)
    label1.setText(str((str("Pin 7 State:") + str((pin7.value())))))


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
