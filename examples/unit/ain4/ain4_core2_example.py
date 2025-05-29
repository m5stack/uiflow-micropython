# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import AIN4_20MAUnit


title0 = None
label0 = None
label1 = None
i2c0 = None
ain4_20ma_0 = None


def setup():
    global title0, label0, label1, i2c0, ain4_20ma_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("AIN 4-20mA Unit Test", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("CH1 Current:", 1, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("CH1 ADC:", 1, 96, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    ain4_20ma_0 = AIN4_20MAUnit(i2c0, 0x55)
    ain4_20ma_0.set_cal_current(20)


def loop():
    global title0, label0, label1, i2c0, ain4_20ma_0
    M5.update()
    label0.setText(str((str("CH1 Current:") + str((ain4_20ma_0.get_current_value())))))
    label1.setText(str((str("CH1 ADC:") + str((ain4_20ma_0.get_adc_raw_value())))))


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
