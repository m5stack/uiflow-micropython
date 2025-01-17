# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DDSUnit


i2c0 = None
dds_0 = None


def setup():
    global i2c0, dds_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    dds_0 = DDSUnit(i2c0, 0x31)
    dds_0.set_mode(dds_0.WAVE_SQUARE)
    dds_0.set_freq(0, 1000)


def loop():
    global i2c0, dds_0
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
