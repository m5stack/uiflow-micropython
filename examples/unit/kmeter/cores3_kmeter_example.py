# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import KMeterUnit
import time


i2c0 = None
kmeter_0 = None


def setup():
    global i2c0, kmeter_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    kmeter_0 = KMeterUnit(i2c0, 0x66)
    print(kmeter_0.get_firmware_version())


def loop():
    global i2c0, kmeter_0
    M5.update()
    print(kmeter_0.get_thermocouple_temperature(kmeter_0.CELSIUS))
    print(kmeter_0.get_internal_temperature(kmeter_0.CELSIUS))
    time.sleep_ms(250)


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
