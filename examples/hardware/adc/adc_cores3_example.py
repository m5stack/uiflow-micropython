# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *


title0 = None
label0 = None
adc6 = None


def setup():
    global title0, label0, adc6

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("CoreS3 ADC Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Read GPIO6 ADC Value:", 4, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    adc6 = ADC(Pin(6), atten=ADC.ATTN_11DB)


def loop():
    global title0, label0, adc6
    M5.update()
    label0.setText(str((str("ADC Value:") + str((adc6.read())))))


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
