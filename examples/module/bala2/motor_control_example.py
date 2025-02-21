# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import Bala2Module
import time


title0 = None
module_bala2_0 = None
i = None


def setup():
    global title0, module_bala2_0, i
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Bala2 Motor Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)

    module_bala2_0 = Bala2Module(0)
    for i in range(1, 1001):
        module_bala2_0.set_motor_speed(i, i)
        time.sleep_ms(10)
    for i in range(1, 1001):
        module_bala2_0.set_motor_speed(1000 - i, 1000 - i)
        time.sleep_ms(10)
    for i in range(1, 1001):
        module_bala2_0.set_motor_speed(0 - i, 0 - i)
        time.sleep_ms(10)
    for i in range(-1000, 1):
        module_bala2_0.set_motor_speed(i, i)
        time.sleep_ms(10)
    module_bala2_0.set_motor_speed(0, 0)


def loop():
    global title0, module_bala2_0, i
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
