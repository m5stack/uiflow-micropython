# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import BLDCDriverUnit
import time


title0 = None
label0 = None
label_speed = None
i2c0 = None
bldcdriver_0 = None
speed = None


def setup():
    global title0, label0, label_speed, i2c0, bldcdriver_0, speed
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("BLDCDriver Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Speed: ", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_speed = Widgets.Label("0", 115, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    bldcdriver_0 = BLDCDriverUnit(i2c0, 0x65)
    bldcdriver_0.set_mode(0)
    bldcdriver_0.set_open_loop_pwm(500)
    bldcdriver_0.set_rpm_int(0)
    speed = 0


def loop():
    global title0, label0, label_speed, i2c0, bldcdriver_0, speed
    M5.update()
    if speed < 300:
        speed = speed + 5
        label_speed.setText(str(speed))
        bldcdriver_0.set_rpm_int(speed)
        time.sleep_ms(100)
    else:
        bldcdriver_0.set_mode(1)
        label_speed.setText(str("0"))
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
