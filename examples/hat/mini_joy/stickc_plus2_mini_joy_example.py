# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import MiniJoyHat


circle0 = None
circle1 = None
label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
hat_minijoyc_0 = None


x = None
value = None
in_min = None
in_max = None
out_min = None
out_range = None
y = None
last_x = None
last_y = None


# Describe this function...
def map_to_range(value, in_min, in_max, out_min, out_range):
    global \
        x, \
        y, \
        last_x, \
        last_y, \
        circle0, \
        circle1, \
        label0, \
        label1, \
        label2, \
        label3, \
        i2c0, \
        hat_minijoyc_0
    return int((value - in_min) * out_range / (in_max - in_min) + out_min)


def setup():
    global \
        circle0, \
        circle1, \
        label0, \
        label1, \
        label2, \
        label3, \
        i2c0, \
        hat_minijoyc_0, \
        x, \
        out_range, \
        out_min, \
        y, \
        value, \
        in_min, \
        in_max, \
        last_x, \
        last_y

    M5.begin()
    circle0 = Widgets.Circle(67, 120, 50, 0xFFFFFF, 0x000000)
    circle1 = Widgets.Circle(67, 120, 4, 0xFFFFFF, 0xFFFFFF)
    label0 = Widgets.Label("X:", 6, 185, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Y:", 6, 212, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("0", 25, 185, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("0", 21, 212, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_minijoyc_0 = MiniJoyHat(i2c0, 0x54)
    hat_minijoyc_0.swap_y(True)
    last_x = 67
    last_y = 120


def loop():
    global \
        circle0, \
        circle1, \
        label0, \
        label1, \
        label2, \
        label3, \
        i2c0, \
        hat_minijoyc_0, \
        x, \
        out_range, \
        out_min, \
        y, \
        value, \
        in_min, \
        in_max, \
        last_x, \
        last_y
    M5.update()
    x = last_x + map_to_range(hat_minijoyc_0.get_x(), -128, 127, -43, 86)
    y = last_y + map_to_range(hat_minijoyc_0.get_y(), -128, 127, -43, 86)
    circle1.setCursor(x=x, y=y)
    if hat_minijoyc_0.get_button_status():
        circle1.setColor(color=0xFF0000, fill_c=0xFF0000)
    else:
        circle1.setColor(color=0xFFFFFF, fill_c=0x6600CC)
    label2.setText(str(hat_minijoyc_0.get_x()))
    label3.setText(str(hat_minijoyc_0.get_y()))


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
