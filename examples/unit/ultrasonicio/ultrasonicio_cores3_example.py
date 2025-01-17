# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import UltrasoundIOUnit


title1 = None
label0 = None
i2c0 = None
sonic_io_0 = None


def setup():
    global title1, label0, i2c0, sonic_io_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title1 = Widgets.Title(
        "UltrasoundUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    sonic_io_0 = UltrasoundIOUnit(port=(8, 9))


def loop():
    global title1, label0, i2c0, sonic_io_0
    M5.update()
    label0.setText(str((str("Distance:") + str((sonic_io_0.get_target_distance(1))))))


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
