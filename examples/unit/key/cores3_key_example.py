# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import KeyUnit


label0 = None
key_0 = None


def key_0_wasPressed_event(state):  # noqa: N802
    global label0, key_0
    key_0.set_color(0x6600CC)
    label0.setText(str("pressed"))


def key_0_wasReleased_event(state):  # noqa: N802
    global label0, key_0
    key_0.set_color(0x33CC00)
    label0.setText(str("released"))


def setup():
    global label0, key_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 108, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    key_0 = KeyUnit((8, 9))
    key_0.setCallback(type=key_0.CB_TYPE.WAS_PRESSED, cb=key_0_wasPressed_event)
    key_0.setCallback(type=key_0.CB_TYPE.WAS_RELEASED, cb=key_0_wasReleased_event)


def loop():
    global label0, key_0
    M5.update()
    key_0.tick(None)


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
