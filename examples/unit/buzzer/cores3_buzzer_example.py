# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import BuzzerUnit


buzzer_0 = None


def setup():
    global buzzer_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    buzzer_0 = BuzzerUnit((8, 9))


def loop():
    global buzzer_0
    M5.update()
    if M5.Touch.getCount():
        buzzer_0.once(freq=4000, duty=50, duration=50)


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
