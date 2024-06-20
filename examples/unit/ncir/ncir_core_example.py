# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import NCIRUnit


i2c0 = None
ncir_0 = None


def setup():
    global i2c0, ncir_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    ncir_0 = NCIRUnit(i2c0)
    print(ncir_0.get_ambient_temperature())
    print(ncir_0.get_object_temperature())


def loop():
    global i2c0, ncir_0
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
