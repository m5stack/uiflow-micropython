# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import IDUnit

i2c0 = None
id_0 = None


def setup():
    global i2c0, id_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    id_0 = IDUnit(i2c0)
    print(id_0.get_sha256_hash("Hello M5", 1))
    print(id_0.get_generate_key(0, False))
    print(id_0.randrange(500, 1000, 5))


def loop():
    global i2c0, id_0
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
