# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ColorUnit


title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
color_0 = None


def setup():
    global title0, label0, label1, label2, i2c0, color_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ColorUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("lux:", 2, 59, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("color:", 2, 114, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("saturation:", 2, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    color_0 = ColorUnit(i2c0)


def loop():
    global title0, label0, label1, label2, i2c0, color_0
    M5.update()
    label0.setText(str((str("Iux:") + str((color_0.get_lux())))))
    label1.setText(str((str("color:") + str((color_0.get_color_rgb_bytes())))))
    label2.setText(str((str("saturation:") + str((color_0.get_color_s())))))


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
