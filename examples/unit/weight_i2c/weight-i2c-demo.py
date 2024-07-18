# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import WeightI2CUnit
import time


i2c0 = None
weight_i2c_0 = None


def setup():
    global i2c0, weight_i2c_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    weight_i2c_0 = WeightI2CUnit(i2c0, 0x26)
    M5.begin()


def loop():
    global i2c0, weight_i2c_0
    M5.update()
    print(weight_i2c_0.get_adc_raw)
    print(weight_i2c_0.get_weight_float)
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
