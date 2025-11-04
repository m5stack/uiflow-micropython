# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from hardware import dualkey
import time


rgb = None
sw_status = None
battery_voltage = None


def setup():
    global rgb, sw_status, battery_voltage
    M5.begin()
    rgb = RGB()
    rgb.set_color(0, 0x000000)
    rgb.set_color(1, 0x000000)


def loop():
    global rgb, sw_status, battery_voltage
    M5.update()
    sw_status = dualkey.get_switch_position()
    if sw_status == 0:
        print("Left")
        rgb.set_color(0, 0x009900)
        rgb.set_color(1, 0x000000)
    elif sw_status == 1:
        print("Middle")
        rgb.set_color(0, 0x000000)
        rgb.set_color(1, 0x000000)
    elif sw_status == 2:
        rgb.set_color(0, 0x000000)
        rgb.set_color(1, 0x009900)
        print("Right")
    battery_voltage = dualkey.get_battery_voltage()
    print((str((str("Battery voltage: ") + str(battery_voltage))) + str("mV")))
    time.sleep_ms(500)


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
