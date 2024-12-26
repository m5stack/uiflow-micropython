# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Encoder8Unit


label0 = None
title0 = None
label1 = None
label2 = None
i2c0 = None
encoder8_0 = None


def setup():
    global label0, title0, label1, label2, i2c0, encoder8_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 2, 72, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "8EncoderUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label("label1", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 2, 161, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    encoder8_0 = Encoder8Unit(i2c0, 0x41)
    encoder8_0.set_led_rgb_from(1, 8, 0x33FF33)
    encoder8_0.set_counter_value(1, 0)


def loop():
    global label0, title0, label1, label2, i2c0, encoder8_0
    M5.update()
    label0.setText(str((str("CH1 Counter Value:") + str((encoder8_0.get_counter_value(1))))))
    label1.setText(str((str("CH1 Button State:") + str((encoder8_0.get_button_status(1))))))
    label2.setText(str((str("Switch State:") + str((encoder8_0.get_switch_status())))))


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
