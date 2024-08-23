# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import RS232Module
import time


rs232_0 = None


def setup():
    global rs232_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    rs232_0 = RS232Module(
        1,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=(0),
        rx=(10),
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )


def loop():
    global rs232_0
    M5.update()
    if rs232_0.any():
        print(rs232_0.readline())
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
