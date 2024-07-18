# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ExtEncoderUnit


label0 = None
i2c0 = None
extencoder_0 = None


def setup():
    global label0, i2c0, extencoder_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    extencoder_0 = ExtEncoderUnit(i2c0, 0x59)


def loop():
    global label0, i2c0, extencoder_0
    M5.update()
    if extencoder_0.get_rotary_status():
        label0.setText(str(extencoder_0.get_rotary_value()))


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
