# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import KMeterISOUnit
import time


i2c0 = None
kmeteriso_0 = None


def setup() -> None:
    global i2c0, kmeteriso_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    kmeteriso_0 = KMeterISOUnit(i2c0, 0x66)


def loop() -> None:
    global i2c0, kmeteriso_0
    if kmeteriso_0.is_ready():
        print(kmeteriso_0.get_thermocouple_temperature(0))
        print(kmeteriso_0.get_internal_temperature(0))
    time.sleep_ms(250)
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
