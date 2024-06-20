# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import ENVHat


label0 = None
label1 = None
label2 = None
i2c0 = None
hat_env3_0 = None


def setup():
    global label0, label1, label2, i2c0, hat_env3_0

    M5.begin()
    label0 = Widgets.Label("label0", 9, 15, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 9, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 9, 72, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_env3_0 = ENVHat(i2c0, type=3)


def loop():
    global label0, label1, label2, i2c0, hat_env3_0
    M5.update()
    label0.setText(str(hat_env3_0.read_temperature()))
    label1.setText(str(hat_env3_0.read_pressure()))
    label2.setText(str(hat_env3_0.read_humidity()))


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
