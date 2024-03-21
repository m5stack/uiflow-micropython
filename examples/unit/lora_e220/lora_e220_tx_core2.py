# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LoRaE220JPUnit
import time


lorae220_0 = None


def setup():
    global lorae220_0

    lorae220_0 = LoRaE220JPUnit((33, 32))
    M5.begin()
    Widgets.fillScreen(0x222222)


def loop():
    global lorae220_0
    M5.update()
    lorae220_0.send(0xFFFF, 0, bytes([0x68, 0x65, 0x6C, 0x6C, 0x6F]))
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
