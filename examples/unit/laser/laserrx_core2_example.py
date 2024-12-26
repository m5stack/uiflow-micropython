# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LaserRXUnit


title0 = None
laser_rx_0 = None


def setup():
    global title0, laser_rx_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LaserRXUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )

    laser_rx_0 = LaserRXUnit((33, 32), mode=2, id=1)
    laser_rx_0.init_uart(9600, 8, None, 1)


def loop():
    global title0, laser_rx_0
    M5.update()
    if laser_rx_0.any():
        print(laser_rx_0.read())


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
