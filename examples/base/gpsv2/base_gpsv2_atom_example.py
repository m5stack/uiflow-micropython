# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from base import AtomicGPSV2Base
import time


rgb = None
base_gpsv2 = None


def setup():
    global rgb, base_gpsv2

    M5.begin()
    rgb = RGB()
    rgb.set_screen([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rgb.set_brightness(20)
    rgb.fill_color(0x33FF33)
    base_gpsv2 = AtomicGPSV2Base(2, port=(22, 19))
    base_gpsv2.set_work_mode(7)
    base_gpsv2.set_time_zone(0)


def loop():
    global rgb, base_gpsv2
    M5.update()
    print((str("longitude:") + str((base_gpsv2.get_longitude()))))
    print((str("altitude:") + str((base_gpsv2.get_altitude()))))
    print((str("latitude:") + str((base_gpsv2.get_latitude()))))
    time.sleep(1)


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
