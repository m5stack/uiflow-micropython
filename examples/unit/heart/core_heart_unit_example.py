# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import HeartUnit


label0 = None
labelHeart = None
i2c0 = None
heart_0 = None


def setup():
    global label0, labelHeart, i2c0, heart_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Heart Rate", 57, 18, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)
    labelHeart = Widgets.Label("label1", 82, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu56)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    heart_0 = HeartUnit(i2c0, 0x57)
    heart_0.start()


def loop():
    global label0, labelHeart, i2c0, heart_0
    M5.update()
    labelHeart.setText(str(heart_0.get_heart_rate()))


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            heart_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
