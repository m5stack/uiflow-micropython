# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ENVUnit


i2c0 = None
env_0 = None
env2_0 = None
env3_0 = None


def setup():
    global i2c0, env_0, env2_0, env3_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    env_0 = ENVUnit(i2c=i2c0, type=1)
    env2_0 = ENVUnit(i2c=i2c0, type=2)
    env3_0 = ENVUnit(i2c=i2c0, type=3)
    print(env_0.read_temperature())
    print(env_0.read_humidity())
    print(env_0.read_pressure())


def loop():
    global i2c0, env_0, env2_0, env3_0
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
