# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicTFCardBase
import time


title0 = None
base_tfcard = None


def setup():
    global title0, base_tfcard

    M5.begin()
    title0 = Widgets.Title("TFCard e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    base_tfcard = AtomicTFCardBase(slot=3, width=1, sck=7, miso=8, mosi=6, freq=1000000)
    os.chdir("/sd")
    print((str("Current dir:") + str((os.getcwd()))))
    print((str("list /sd/dir: ") + str((os.listdir("/sd/")))))
    if not ("sdcard_test" in os.listdir("/sd/")):  # noqa: E713
        print("Try create 'sdcard_test' directory in /sd/")
        os.mkdir("/sd/sdcard_test")
    print((str("'sdcard_test' is directory?:") + str((os.stat("/sd/sdcard_test")[0] == 0x4000))))
    print((str("'sdcard_test' is file?:") + str((os.stat("/sd/sdcard_test")[0] == 0x8000))))
    print("Delay 1s to delete 'sdcard_test' directory")
    time.sleep(1)
    os.rmdir("/sd/sdcard_test")
    if not ("sdcard_test" in os.listdir("/sd/")):  # noqa: E713
        print("Directory 'sdcard_test' deleted successfully")


def loop():
    global title0, base_tfcard
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
