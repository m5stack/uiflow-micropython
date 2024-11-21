# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import GNSSModule


title0 = None
label3 = None
label4 = None
label5 = None
label6 = None
label10 = None
label11 = None
label12 = None
label13 = None
label14 = None
label15 = None
label16 = None
label17 = None
label18 = None
label19 = None
label20 = None
label21 = None
label22 = None
label23 = None
line0 = None
gnss_0 = None


list2 = None


def setup():
    global \
        title0, \
        label3, \
        label4, \
        label5, \
        label6, \
        label10, \
        label11, \
        label12, \
        label13, \
        label14, \
        label15, \
        label16, \
        label17, \
        label18, \
        label19, \
        label20, \
        label21, \
        label22, \
        label23, \
        line0, \
        gnss_0, \
        list2

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "            M135 GNSS Demo", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label("angle:", 2, 23, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label(
        "attitude(yaw):", 1, 73, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label5 = Widgets.Label("temp:", 4, 128, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("pressure:", 2, 180, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("label10", 4, 46, 1.0, 0x3EF815, 0x222222, Widgets.FONTS.DejaVu18)
    label11 = Widgets.Label("label11", 5, 102, 1.0, 0xF60505, 0x222222, Widgets.FONTS.DejaVu18)
    label12 = Widgets.Label("label12", 5, 154, 1.0, 0x3EF815, 0x222222, Widgets.FONTS.DejaVu18)
    label13 = Widgets.Label("label13", 5, 208, 1.0, 0xF60505, 0x222222, Widgets.FONTS.DejaVu18)
    label14 = Widgets.Label("lat:", 158, 51, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label15 = Widgets.Label("long:", 157, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label16 = Widgets.Label("sta:", 158, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label17 = Widgets.Label("date:", 158, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label18 = Widgets.Label("time:", 159, 168, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label19 = Widgets.Label("label19", 159, 138, 1.0, 0x15F0FF, 0x222222, Widgets.FONTS.DejaVu18)
    label20 = Widgets.Label("label20", 159, 197, 1.0, 0xEAFF00, 0x222222, Widgets.FONTS.DejaVu18)
    label21 = Widgets.Label("label21", 205, 25, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label22 = Widgets.Label("label22", 205, 52, 1.0, 0x15F0FF, 0x222222, Widgets.FONTS.DejaVu18)
    label23 = Widgets.Label("label23", 205, 81, 1.0, 0xEAFF00, 0x222222, Widgets.FONTS.DejaVu18)
    line0 = Widgets.Line(142, 27, 142, 232, 0xFFFFFF)

    gnss_0 = GNSSModule(2, 13, 14, 0x69)


def loop():
    global \
        title0, \
        label3, \
        label4, \
        label5, \
        label6, \
        label10, \
        label11, \
        label12, \
        label13, \
        label14, \
        label15, \
        label16, \
        label17, \
        label18, \
        label19, \
        label20, \
        label21, \
        label22, \
        label23, \
        line0, \
        gnss_0, \
        list2
    M5.update()
    label10.setText(str(gnss_0.get_compass()))
    label11.setText(str((gnss_0.get_attitude())[0]))
    label12.setText(str(gnss_0.get_temperature()))
    label13.setText(str(gnss_0.get_pressure()))
    if gnss_0.is_locate_valid():
        label21.setText(str("OK"))
    else:
        label21.setText(str("Failed"))
    label22.setText(str(gnss_0.get_latitude()))
    label23.setText(str(gnss_0.get_longitude()))
    label19.setText(str(gnss_0.get_date()))
    label20.setText(str(gnss_0.get_time()))


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
