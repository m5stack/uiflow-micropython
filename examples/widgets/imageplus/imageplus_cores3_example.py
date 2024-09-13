# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from image_plus import ImagePlus


title0 = None
image_plus0 = None


def setup():
    global title0, image_plus0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Image+ CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    image_plus0 = ImagePlus(
        "https://static-cdn.m5stack.com/resource/public/assets/aboutus/m5logo2022.png",
        43,
        51,
        True,
        3000,
        default_img="res/img/default.png",
    )

    image_plus0.setVisible(True)
    image_plus0.set_update_period(5000)
    image_plus0.set_update_enable(True)


def loop():
    global title0, image_plus0
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
