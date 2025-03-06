# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import ATOMGPSBase
import time


title0 = None
base_gps = None


def setup():
    global title0, base_gps

    M5.begin()
    title0 = Widgets.Title("GPS Base", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    base_gps = ATOMGPSBase(2, port=(5, 6))
    base_gps.set_time_zone(0)


def loop():
    global title0, base_gps
    M5.update()
    print(base_gps.get_gps_time())
    print(base_gps.get_gps_date())
    print(base_gps.get_gps_date_time())
    print(base_gps.get_timestamp())
    print(base_gps.get_latitude())
    print(base_gps.get_longitude())
    print(base_gps.get_altitude())
    print(base_gps.get_satellite_num())
    print(base_gps.get_pos_quality())
    print(base_gps.get_corse_over_ground())
    print(base_gps.get_speed_over_ground())
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
