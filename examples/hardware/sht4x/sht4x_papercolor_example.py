# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import SHT4X
import time


sht4x = None


def setup():
    global sht4x

    M5.begin({"clear_display": False})
    Widgets.setRotation(1)

    M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FASTEST)
    sht4x = SHT4X()


def loop():
    global sht4x
    M5.update()
    print((str("hum:") + str((sht4x.get_humidity()))))
    print((str("temp:") + str((sht4x.get_temperature()))))
    time.sleep(1)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            print(e)
        except ImportError:
            print("please update to latest firmware")
