# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import ToF90Unit


title0 = None
label0 = None
label1 = None
i2c0 = None
minitof90_0 = None


def setup():
    global title0, label0, label1, i2c0, minitof90_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Core2 Mini ToF-90  Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 2, 110, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", -85, 149, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    minitof90_0 = ToF90Unit(i2c0, 0x29)
    minitof90_0.start_continuous()


def loop():
    global title0, label0, label1, i2c0, minitof90_0
    M5.update()
    if minitof90_0.get_data_ready():
        label0.setText(str((str("Distance:") + str((str((minitof90_0.get_range())) + str("mm"))))))


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
