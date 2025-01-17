# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DigiClockUnit
import time


label0 = None
i2c0 = None
digiclock_0 = None


now = None


def setup():
    global label0, i2c0, digiclock_0, now

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 99, 97, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    digiclock_0 = DigiClockUnit(i2c0, 0x30)
    now = str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))
    digiclock_0.set_string(now)
    label0.setText(str(now))


def loop():
    global label0, i2c0, digiclock_0, now
    M5.update()
    if now != (str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))):
        now = str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))
        label0.setText(str(now))
        digiclock_0.set_string(now)
    digiclock_0.set_raw(1, 2)
    time.sleep(1)
    digiclock_0.set_raw(0, 2)
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
