# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Angle8Unit
import m5utils
import time


title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
angle8_0 = None


import math

map_value = None


def setup():
    global title0, label0, label1, label2, i2c0, angle8_0, map_value

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "8AngleUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    angle8_0 = Angle8Unit(i2c0, 0x43)
    angle8_0.set_led_rgb_from(1, 9, 0x33FF33, 100, 0)
    map_value = 0


def loop():
    global title0, label0, label1, label2, i2c0, angle8_0, map_value
    M5.update()
    map_value = round(m5utils.remap(angle8_0.get_adc8_raw(8), 0, 255, 0, 100))
    label0.setText(str((str("Switch:") + str((angle8_0.get_switch_status())))))
    label1.setText(str((str("CH1 8bit:") + str((angle8_0.get_adc8_raw(1))))))
    label2.setText(str((str("CH8 map value:") + str(map_value))))
    angle8_0.set_led_rgb_from(1, 9, 0x33FF33, map_value, 0)
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
