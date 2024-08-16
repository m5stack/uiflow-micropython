# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ScrollUnit


label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
scroll_0 = None


def setup():
    global label0, label1, label2, label3, i2c0, scroll_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 73, 75, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu56)
    label1 = Widgets.Label("label1", 135, 138, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label2 = Widgets.Label("label2", 9, 9, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 10, 31, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    scroll_0 = ScrollUnit(i2c0, 0x40)
    label2.setText(str((str("bootloader ver: ") + str((scroll_0.get_bootloader_version())))))
    label3.setText(str((str("firmware ver: ") + str((scroll_0.get_firmware_version())))))
    scroll_0.set_rotary_value(100)


def loop():
    global label0, label1, label2, label3, i2c0, scroll_0
    M5.update()
    if scroll_0.get_rotary_status():
        label0.setText(str(scroll_0.get_rotary_value()))
        label1.setText(str(scroll_0.get_rotary_increments()))
    if scroll_0.get_button_status():
        scroll_0.reset_rotary_value()
        scroll_0.fill_color(0x33CC00)
    else:
        scroll_0.fill_color(0xFF0000)


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
