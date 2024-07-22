# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import CardKBHat
from hardware import *


label0 = None
i2c0 = None
hat_cardkb_0 = None


def hat_cardkb_0_pressed_event(kb):
    global label0, i2c0, hat_cardkb_0
    label0.setText(str(hat_cardkb_0.get_string()))


def setup():
    global label0, i2c0, hat_cardkb_0

    M5.begin()
    label0 = Widgets.Label("label0", 39, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_cardkb_0 = CardKBHat(i2c0, 0x5F)
    hat_cardkb_0.set_callback(hat_cardkb_0_pressed_event)


def loop():
    global label0, i2c0, hat_cardkb_0
    M5.update()
    hat_cardkb_0.tick()


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
