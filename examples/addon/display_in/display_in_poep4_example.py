# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from addon import DisplayIn
import time


addon_display_in_0 = None


def setup():
    global addon_display_in_0

    M5.begin()
    addon_display_in_0 = DisplayIn()
    time.sleep(1)
    print(
        (
            str("saved /flash/lt6911_capture.jpg, ")
            + str(
                (str((addon_display_in_0.capture("/flash/capture.jpg", 75, 1000))) + str("bytes"))
            )
        )
    )


def loop():
    global addon_display_in_0
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
