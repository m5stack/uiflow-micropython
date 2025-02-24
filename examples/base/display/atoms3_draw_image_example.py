# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicDisplayBase


image0 = None
image1 = None
base_display = None


def setup():
    global image0, image1, base_display

    M5.begin()
    image0 = Widgets.Image("res/img/default.jpg", 51, 51, scale_x=1, scale_y=1)

    base_display = AtomicDisplayBase(
        width=1280,
        height=720,
        refresh_rate=60,
        output_width=1280,
        output_height=720,
        scale_w=1,
        scale_h=1,
        pixel_clock=74250000,
    )
    image1 = Widgets.Image(
        "res/img/default.jpg", 443, 213, scale_x=10, scale_y=10, parent=base_display
    )
    image0.setImage("res/img/default.jpg")
    image1.setImage("res/img/default.jpg")


def loop():
    global image0, image1, base_display
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
