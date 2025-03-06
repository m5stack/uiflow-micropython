# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicHDriverBase
import time


title0 = None
label0 = None
label1 = None
label_vol = None
label_speed = None
base_hdriver = None
i = None
speed = None


def setup():
    global title0, label0, label1, label_vol, label_speed, base_hdriver, speed, i
    M5.begin()
    title0 = Widgets.Title("Speed Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("speed:", 5, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("vol:", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("12.0V", 45, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_speed = Widgets.Label("0", 70, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    base_hdriver = AtomicHDriverBase(6, 7, 5, 8, 1000)
    label_vol.setText(str((str((base_hdriver.get_voltage())) + str("V"))))
    speed = 0


def loop():
    global title0, label0, label1, label_vol, label_speed, base_hdriver, speed, i
    M5.update()
    for i in range(50):
        speed = i
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)
    for i in range(50):
        speed = 50 - i
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)
    for i in range(50):
        speed = 1 - i
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)
    for i in range(50):
        speed = i - 50
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)


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
