# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import UltrasoundI2CUnit


label0 = None
i2c0 = None
ultrasonic_0 = None


def setup():
    global label0, i2c0, ultrasonic_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    ultrasonic_0 = UltrasoundI2CUnit(i2c0)


def loop():
    global label0, i2c0, ultrasonic_0
    M5.update()
    label0.setText(str(ultrasonic_0.get_target_distance(1)))


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
