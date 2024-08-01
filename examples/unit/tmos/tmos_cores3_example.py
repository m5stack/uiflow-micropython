# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import TMOSUnit
from hardware import *


title0 = None
label0 = None
title1 = None
title2 = None
TMOSTest = None
label1 = None
label2 = None
label3 = None
i2c0 = None
tmos_0 = None


def tmos_0_presence_detect_event(arg):
    global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
    label1.setText(str((str("Prescence Flag:") + str((tmos_0.get_presence_state())))))
    label0.setText(str((str("Prescence:") + str((tmos_0.get_presence_value())))))


def tmos_0_motion_detect_event(arg):
    global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
    label3.setText(str((str("Motion Flag:") + str((tmos_0.get_motion_state())))))
    label2.setText(str((str("Motion:") + str((tmos_0.get_motion_value())))))


def tmos_0_presence_not_detected_event(arg):
    global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
    label1.setText(str((str("Prescence Flag:") + str((tmos_0.get_presence_state())))))


def tmos_0_motion_not_detected_event(arg):
    global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
    label3.setText(str((str("Motion Flag:") + str((tmos_0.get_motion_state())))))


def setup():
    global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Prescence:", 2, 65, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title1 = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    title2 = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    TMOSTest = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label(
        "Prescence Flag", 2, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Motion:", 2, 130, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Motion Flag:", 2, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    title0.setText("TMOS Test")
    tmos_0 = TMOSUnit(i2c0, 0x5A)
    tmos_0.set_callback(tmos_0_presence_detect_event, tmos_0.PRESENCE_DETECT)
    tmos_0.set_callback(tmos_0_motion_detect_event, tmos_0.MOTION_DETECT)
    tmos_0.set_callback(tmos_0_presence_not_detected_event, tmos_0.PRESENCE_NOT_DETECTED)
    tmos_0.set_callback(tmos_0_motion_not_detected_event, tmos_0.MOTION_NOT_DETECTED)
    label0.setText(str("Prescence:"))
    label1.setText(str("Prescence Flag:"))
    label2.setText(str("Motion:"))
    label3.setText(str("Motion Flag:"))
    print(tmos_0.get_gain_mode())


def loop():
    global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
    M5.update()
    tmos_0.tick_callback()


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
