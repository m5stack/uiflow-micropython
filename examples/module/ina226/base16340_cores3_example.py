# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import Module16340
import time


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
module16340_0 = None


def setup():
    global title0, label0, label1, label2, label3, module16340_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Base16340 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label("label0", 2, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label1 = Widgets.Label("label1", 2, 94, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label2 = Widgets.Label("label2", 2, 138, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label3 = Widgets.Label("label3", 2, 176, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    module16340_0 = Module16340(address=0x45)


def loop():
    global title0, label0, label1, label2, label3, module16340_0
    M5.update()
    time.sleep(1)
    label0.setText(str((str("Shunt Voltage:") + str((module16340_0.read_shunt_voltage())))))
    label1.setText(str((str("Bus Voltage:") + str((module16340_0.read_bus_voltage())))))
    label2.setText(str((str("Current:") + str((module16340_0.read_current())))))
    label3.setText(str((str("Power:") + str((module16340_0.read_power())))))


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
