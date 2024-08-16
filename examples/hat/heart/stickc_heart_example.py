# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import HeartHat


Heart = None
SPO2 = None
label0 = None
label1 = None
i2c0 = None
hat_heart_0 = None


def setup():
    global Heart, SPO2, label0, label1, i2c0, hat_heart_0

    M5.begin()
    Heart = Widgets.Label("Heart", 1, 2, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    SPO2 = Widgets.Label("SPO2", 3, 122, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("0", 5, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)
    label1 = Widgets.Label("0", 7, 169, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_heart_0 = HeartHat(i2c0, 0x57)
    hat_heart_0.start()


def loop():
    global Heart, SPO2, label0, label1, i2c0, hat_heart_0
    M5.update()
    label0.setText(str(hat_heart_0.get_heart_rate()))
    label1.setText(str(hat_heart_0.get_spo2()))


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
