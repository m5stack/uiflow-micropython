# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoraModule
import time


label9 = None
title0 = None
datasent = None
label0 = None
timestamp = None
lora868_0 = None


x = None


def setup():
    global label9, title0, datasent, label0, timestamp, lora868_0, x

    M5.begin()
    Widgets.fillScreen(0x222222)
    label9 = Widgets.Label("Data sent:", 10, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("LoRa Module Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    datasent = Widgets.Label("label0", 11, 73, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Timestamp:", 10, 127, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    timestamp = Widgets.Label("label1", 14, 176, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    lora868_0 = LoraModule(0, 10, 5, LoraModule.LORA_868, 8, "250", 8, 12, 200)


def loop():
    global label9, title0, datasent, label0, timestamp, lora868_0, x
    M5.update()
    x = (x if isinstance(x, (int, float)) else 0) + 1
    timestamp.setText(str("Label"))
    datasent.setText(str((str("Hello M5! ") + str(x))))
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
