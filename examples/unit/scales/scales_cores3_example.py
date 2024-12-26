# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ScalesUnit


title1 = None
label0 = None
label1 = None
i2c0 = None
scales_0 = None


def setup():
    global title1, label0, label1, i2c0, scales_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title1 = Widgets.Title(
        "ScaleUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 89, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 3, 132, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    scales_0 = ScalesUnit(i2c0, 0x26)
    scales_0.set_rgb_led(0x6600CC)


def loop():
    global title1, label0, label1, i2c0, scales_0
    M5.update()
    if not (scales_0.get_button_status(2)):
        scales_0.set_current_raw_offset()
        label0.setText(str("Reset to zero"))
    else:
        label0.setText(str("Press Btn to reset"))
    label1.setText(
        str((str("Current weight:") + str((str((scales_0.get_scale_value(1))) + str("g")))))
    )


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
