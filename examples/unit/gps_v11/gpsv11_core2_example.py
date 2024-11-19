# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import GPSV11Unit
import time


label0 = None
title0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
gpsv11_0 = None


power_on_time = None


def setup():
    global label0, title0, label1, label2, label3, label4, label5, label6, gpsv11_0, power_on_time

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Power On:", 1, 33, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "GPSV11Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Satellite Num:", 1, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Timestamp:", 1, 202, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("GPS Data:", -6, 526, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Latitude:", 1, 104, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Longitude:", 1, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("Altitude:", 1, 170, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    gpsv11_0 = GPSV11Unit(2, port=(33, 32))
    gpsv11_0.set_work_mode(7)
    power_on_time = time.time()


def loop():
    global label0, title0, label1, label2, label3, label4, label5, label6, gpsv11_0, power_on_time
    M5.update()
    label0.setText(str((str("Power On:") + str(((time.time()) - power_on_time)))))
    label1.setText(str((str("Satellite Num:") + str((gpsv11_0.get_satellite_num())))))
    label2.setText(str((str("Timestamp:") + str((gpsv11_0.get_timestamp())))))
    label4.setText(str((str("Latitude:") + str((gpsv11_0.get_latitude())))))
    label5.setText(str((str("Longitude:") + str((gpsv11_0.get_longitude())))))
    label6.setText(str((str("Altitude:") + str((gpsv11_0.get_altitude())))))
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
