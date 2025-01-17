# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from hat import DAC2Hat


i2c0 = None
hat_dac2_0 = None


def setup():
    global i2c0, hat_dac2_0

    M5.begin()
    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_dac2_0 = DAC2Hat(i2c0, 0x59)
    hat_dac2_0.set_dacoutput_voltage_range(hat_dac2_0.RANGE_10V)
    hat_dac2_0.set_voltage(5, channel=hat_dac2_0.CHANNEL_0)


def loop():
    global i2c0, hat_dac2_0
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
