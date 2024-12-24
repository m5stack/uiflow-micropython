# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DAC2Unit


i2c0 = None
dac2_0 = None


def setup():
    global i2c0, dac2_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    dac2_0 = DAC2Unit(i2c0, 0x59)
    dac2_0.set_dacoutput_voltage_range(dac2_0.RANGE_10V)
    dac2_0.set_voltage(7.5, channel=dac2_0.CHANNEL_0)


def loop():
    global i2c0, dac2_0
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
