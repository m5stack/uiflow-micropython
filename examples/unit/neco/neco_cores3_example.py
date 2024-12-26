# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import NECOUnit


title0 = None
i2c0 = None
neco_0 = None


def setup():
    global title0, i2c0, neco_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "NECOUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    neco_0 = NECOUnit((1, 2), 70, True)
    neco_0.set_brightness(3)


def loop():
    global title0, i2c0, neco_0
    M5.update()
    neco_0.set_random_color_random_led_from(0, 70)


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
