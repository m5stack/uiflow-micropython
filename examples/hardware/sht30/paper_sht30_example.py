# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import SHT30


sht30 = None


def setup():
    global sht30

    M5.begin()
    Widgets.fillScreen(0xEEEEEE)

    sht30 = SHT30()


def loop():
    global sht30
    M5.update()
    print((str("Humidity:") + str((sht30.get_humidity()))))
    print((str("Temperature:") + str((sht30.get_temperature()))))


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
