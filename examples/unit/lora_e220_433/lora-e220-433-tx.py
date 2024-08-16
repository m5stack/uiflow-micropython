# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LoRaE220433Unit


lorae220433_0 = None


def setup():
    global lorae220433_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    lorae220433_0 = LoRaE220433Unit(1, port=(18, 17))


def loop():
    global lorae220433_0
    M5.update()
    lorae220433_0.send(0x9999, 0, "Hello M5")


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
