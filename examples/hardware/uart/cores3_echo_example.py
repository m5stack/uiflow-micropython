# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import UART
import time


label0 = None
uart1 = None


i = None


def setup():
    global label0, uart1, i

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 102, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart1 = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10)
    i = 0


def loop():
    global label0, uart1, i
    M5.update()
    uart1.write(i)
    if uart1.any():
        label0.setText(str(uart1.read()))
    i = (i if isinstance(i, (int, float)) else 0) + 1
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
