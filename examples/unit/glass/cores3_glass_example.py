# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import GlassUnit


label0 = None
label1 = None
i2c0 = None
glass_0 = None


def setup():
    global label0, label1, i2c0, glass_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 138, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    glass_0 = GlassUnit(i2c0, 0x3D)
    label1 = Widgets.Label(
        "GLASS", 32, 21, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, glass_0
    )


def loop():
    global label0, label1, i2c0, glass_0
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
