# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import *


label0 = None
label1 = None
label2 = None
rtc = None


def setup():
    global label0, label1, label2, rtc

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 17, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 12, 105, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text", 25, 153, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    rtc = RTC()
    rtc.init((2023, 6, 28, 0, 4, 1, 27, 96))
    rtc.timezone("GMT-8")


def loop():
    global label0, label1, label2, rtc
    M5.update()
    label0.setText(str((rtc.datetime())))
    label1.setText(str((rtc.local_datetime())))
    label2.setText(str((rtc.timezone())))


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
