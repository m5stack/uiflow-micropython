# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from image_plus import ImagePlus


image_plus0 = None


def setup():
    global image_plus0

    M5.begin()
    Widgets.fillScreen(0x222222)
    image_plus0 = ImagePlus(
        "https://community.m5stack.com/assets/uploads/profile/38444-profileavatar.jpeg",
        16,
        10,
        True,
        5000,
    )


def loop():
    global image_plus0
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
