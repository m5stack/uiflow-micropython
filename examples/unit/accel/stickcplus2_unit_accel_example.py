# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import AccelUnit


label0 = None
label1 = None
label2 = None
title0 = None
label3 = None
label4 = None
label5 = None
i2c0 = None
accel_0 = None


acc = None


def setup():
    global label0, label1, label2, title0, label3, label4, label5, i2c0, accel_0, acc

    M5.begin()
    label0 = Widgets.Label("x:", 4, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("y:", 4, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("z:", 4, 128, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("ACCEL UNIT", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 24, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("label4", 24, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 24, 128, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    accel_0 = AccelUnit(i2c0, 0x53)


def loop():
    global label0, label1, label2, title0, label3, label4, label5, i2c0, accel_0, acc
    M5.update()
    acc = accel_0.get_accel()
    label3.setText(str(acc[0]))
    label4.setText(str(acc[1]))
    label5.setText(str(acc[2]))


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
