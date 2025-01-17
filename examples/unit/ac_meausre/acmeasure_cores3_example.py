# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ACMeasureUnit


label0 = None
title0 = None
label1 = None
i2c0 = None
ac_measure_0 = None


def setup():
    global label0, title0, label1, i2c0, ac_measure_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 1, 81, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "ACMeasureUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label("label1", 1, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ac_measure_0 = ACMeasureUnit(i2c0, 0x42)


def loop():
    global label0, title0, label1, i2c0, ac_measure_0
    M5.update()
    label0.setText(str((str("Voltage:") + str((ac_measure_0.get_voltage_str())))))
    label1.setText(str((str("Current:") + str((ac_measure_0.get_current_str())))))
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
