# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import TOF4MUnit


title0 = None
label1 = None
i2c1 = None
tof4m_0 = None


distance = None


def setup():
    global title0, label1, i2c1, tof4m_0, distance

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("ToF4MUnit CoreS3 Test", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c1 = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
    tof4m_0 = TOF4MUnit(i2c1, 0x29)
    tof4m_0.set_distance_mode(2)
    tof4m_0.set_measurement_timing_budget(500)
    tof4m_0.set_continuous_start_measurement()


def loop():
    global title0, label1, i2c1, tof4m_0, distance
    M5.update()
    if tof4m_0.get_data_ready:
        label1.setText(str((str("Distance:") + str((str(distance) + str("mm"))))))


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
