# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Relay4Unit
import time


i2c0 = None
relay4_0 = None


def setup():
    global i2c0, relay4_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    relay4_0 = Relay4Unit(i2c0, 0x26)


def loop():
    global i2c0, relay4_0
    M5.update()
    relay4_0.set_relay_all(1)
    time.sleep(1)
    relay4_0.set_relay_all(0)
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
