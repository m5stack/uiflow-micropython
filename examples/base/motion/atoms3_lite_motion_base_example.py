# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from base import Motion


i2c0 = None
motion = None


def setup():
    global i2c0, motion

    M5.begin()
    i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
    motion = Motion(i2c0, 0x38)
    motion.set_servo_angle(1, 70)
    motion.set_motor_speed(1, 46)
    print(motion.get_servo_angle(1))


def loop():
    global i2c0, motion
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
