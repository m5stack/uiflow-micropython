# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import BPSUnit
import time


label0 = None
label1 = None
label2 = None
i2c0 = None
bps_0 = None


def setup():
    global label0, label1, label2, i2c0, bps_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 43, 33, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 43, 65, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 44, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    bps_0 = BPSUnit(i2c0)


def loop():
    global label0, label1, label2, i2c0, bps_0
    M5.update()
    print((str("Temperature: ") + str((bps_0.get_temperature()))))
    print((str("Pressure: ") + str((bps_0.get_pressure()))))
    print((str("Altitude: ") + str((bps_0.get_altitude()))))
    time.sleep(0.5)


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
