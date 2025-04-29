# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import Servos8Unit
import time


label0 = None
i2c0 = None
servos8_0 = None


def setup():
    global label0, i2c0, servos8_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label(
        "8Servos Unit", 92, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    servos8_0 = Servos8Unit(i2c0, 0x25)
    servos8_0.set_mode(3, 3)
    servos8_0.set_mode(3, 7)


def loop():
    global label0, i2c0, servos8_0
    M5.update()
    servos8_0.set_servo_angle(45, 3)
    servos8_0.set_servo_angle(45, 7)
    time.sleep(1)
    servos8_0.set_servo_angle(150, 3)
    servos8_0.set_servo_angle(150, 7)
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
