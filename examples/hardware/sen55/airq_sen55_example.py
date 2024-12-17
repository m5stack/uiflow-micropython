# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
import time


sen55 = None


def setup():
    global sen55

    M5.begin()
    Widgets.fillScreen(0xFFFFFF)

    sen55 = SEN55()
    sen55.set_power_state(True)
    sen55.set_work_mode(1)
    time.sleep(1)


def loop():
    global sen55
    M5.update()
    if sen55.get_data_ready_flag():
        print(sen55.get_pm1_0())
        print(sen55.get_pm2_5())
        print(sen55.get_pm4_0())
        print(sen55.get_pm10_0())
        print(sen55.get_humidity())
        print(sen55.get_temperature())
        print(sen55.get_voc())
        print(sen55.get_nox())
    time.sleep_ms(100)


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
