# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ENVPROUnit
import time


title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
envpro_0 = None
co2_0 = None


def setup():
    global title0, label0, label1, label2, i2c0, envpro_0, co2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ENVProUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    envpro_0 = ENVPROUnit(i2c0)


def loop():
    global title0, label0, label1, label2, i2c0, envpro_0, co2_0
    M5.update()
    label0.setText(str((str("Pressure:") + str((envpro_0.get_pressure())))))
    label1.setText(str((str("Humidity:") + str((envpro_0.get_humidity())))))
    label2.setText(str((str("Temperature:") + str((envpro_0.get_temperature())))))
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
