# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from esp32 import NVS
import time


label0 = None
title0 = None
label1 = None
label2 = None
label3 = None
nvs_0 = None


count = None


def setup():
    global label0, title0, label1, label2, label3, nvs_0, count

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Key", 4, 25, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("NVS Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Value", 73, 25, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("count", 4, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Value", 75, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    nvs_0 = NVS("db")
    count = 0
    nvs_0.set_i32("count", count)


def loop():
    global label0, title0, label1, label2, label3, nvs_0, count
    M5.update()
    count = nvs_0.get_i32("count")
    Speaker.tone(2000, 50)
    label3.setText(str(count))
    label3.setColor(0x33CCFF, 0x000000)
    count = (count if isinstance(count, (int, float)) else 0) + 1
    time.sleep(1)
    nvs_0.set_i32("count", count)
    Speaker.tone(3222, 50)
    label3.setColor(0xFF6600, 0x000000)
    time.sleep(1)


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
