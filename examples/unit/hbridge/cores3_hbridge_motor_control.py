# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import HbridgeUnit
import time


title0 = None
label0 = None
label_speed = None
i2c0 = None
hbridge_0 = None
speed = None
dir2 = None


def setup():
    global title0, label0, label_speed, i2c0, hbridge_0, speed, dir2
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("HBridge Motor Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Speed:", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_speed = Widgets.Label("0", 110, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    hbridge_0 = HbridgeUnit(i2c0, 0x20)
    hbridge_0.set_pwm_freq(1000)
    speed = 0
    hbridge_0.set_direction(0)
    dir2 = True


def loop():
    global title0, label0, label_speed, i2c0, hbridge_0, speed, dir2
    M5.update()
    speed = speed + 1
    label0.setText(str(speed))
    if speed > 99:
        speed = 0
        dir2 = not dir2
        if dir2:
            hbridge_0.set_direction(1)
        else:
            hbridge_0.set_direction(2)
        time.sleep_ms(1000)
    hbridge_0.set_percentage_pwm(speed, 8)
    time.sleep_ms(50)


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
