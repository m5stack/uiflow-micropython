# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin


label0 = None
label1 = None
i2c0 = None
minioled_0 = None


def setup():
    global label0, label1, i2c0, minioled_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    minioled_0 = M5.addDisplay(i2c0, 0x3C, {"unit_mini_oled": True})
    label1 = Widgets.Label(
        "Mini", 15, 9, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, minioled_0
    )


def loop():
    global label0, label1, i2c0, minioled_0
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
