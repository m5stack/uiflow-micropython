# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *


label0 = None
label1 = None
module_display = None


def setup():
    global label0, label1, module_display

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    module_display = M5.addDisplay(
        None,
        0,
        {
            "module_display": {
                "enabled": True,
                "width": 1280,
                "height": 720,
                "output_width": 1280,
                "output_height": 720,
                "refresh_rate": 60,
                "scale_w": 1,
                "scale_h": 1,
                "pixel_clock": 74250000,
            }
        },
    )
    label1 = Widgets.Label(
        "Display", 506, 318, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu72, module_display
    )


def loop():
    global label0, label1, module_display
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
