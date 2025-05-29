# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import TubePressureUnit


title0 = None
label2 = None
label0 = None
label1 = None
tubepressure_0 = None


def setup():
    global title0, label2, label0, label1, tubepressure_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "TubePressureUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("label2", 1, 159, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 1, 73, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    tubepressure_0 = TubePressureUnit((36, 26))


def loop():
    global title0, label2, label0, label1, tubepressure_0
    M5.update()
    label0.setText(str((str("Pressure:") + str((tubepressure_0.get_pressure())))))
    label1.setText(str((str("ADC 12Bits Value:") + str((tubepressure_0.get_analog_value(12))))))
    label2.setText(str((str("Voltage:") + str((tubepressure_0.get_voltage())))))


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
