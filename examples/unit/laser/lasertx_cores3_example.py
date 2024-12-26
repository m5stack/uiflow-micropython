# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LaserTXUnit
import time


title1 = None
label0 = None
laser_tx_0 = None


def setup():
    global title1, label0, laser_tx_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title1 = Widgets.Title(
        "LaserTXUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    laser_tx_0 = LaserTXUnit((1, 2), mode=2, id=1)
    laser_tx_0.init_uart(9600, 8, None, 1)


def loop():
    global title1, label0, laser_tx_0
    M5.update()
    if M5.Touch.getCount():
        laser_tx_0.write("Hello")
        label0.setText(str("Write Message"))
        time.sleep(1)
    else:
        label0.setText(str("Wait to write Message"))


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
