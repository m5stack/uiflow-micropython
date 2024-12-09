# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import TVOCUnit
import time


label3 = None
title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
tvoc_0 = None


def setup():
    global label3, title0, label0, label1, label2, i2c0, tvoc_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label3 = Widgets.Label("label3", 0, 193, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "TVOCUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    tvoc_0 = TVOCUnit(i2c0)


def loop():
    global label3, title0, label0, label1, label2, i2c0, tvoc_0
    M5.update()
    label0.setText(str((str("TVOC:") + str((tvoc_0.tvoc())))))
    label1.setText(str((str("CO2:") + str((tvoc_0.co2eq())))))
    label2.setText(str((str("Ethanol:") + str((tvoc_0.raw_ethanol())))))
    label3.setText(str((str("H2:") + str((tvoc_0.raw_h2())))))
    time.sleep(1)


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
