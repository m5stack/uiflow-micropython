# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
image0 = None
image1 = None


def setup():
    global page0, image0, image1

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    image0 = m5ui.M5Image("/flash/res/img/uiflow.jpg", x=129, y=54, parent=page0)
    image1 = m5ui.M5Image("/flash/res/img/uiflow.png", x=129, y=118, parent=page0)

    page0.screen_load()
    image0.set_image("/flash/res/img/uiflow.jpg")
    image1.set_image("/flash/res/img/uiflow.png")


def loop():
    global page0, image0, image1
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
