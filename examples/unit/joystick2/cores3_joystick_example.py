# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Joystick2Unit


rect_neg_x = None
rect_neg_y = None
rect_pos_x = None
rect_pos_y = None
rect0 = None
label0 = None
label1 = None
i2c0 = None
joystick2_0 = None


import math

pos_x = None
pos_y = None
x = None
y = None
last_x = None
last_y = None


def setup():
    global \
        rect_neg_x, \
        rect_neg_y, \
        rect_pos_x, \
        rect_pos_y, \
        rect0, \
        label0, \
        label1, \
        i2c0, \
        joystick2_0, \
        pos_x, \
        pos_y, \
        x, \
        y, \
        last_x, \
        last_y

    M5.begin()
    Widgets.fillScreen(0x222222)
    rect_neg_x = Widgets.Rectangle(145, 105, 30, 30, 0xFFFFFF, 0xFFFFFF)
    rect_neg_y = Widgets.Rectangle(145, 105, 30, 30, 0xFFFFFF, 0xFFFFFF)
    rect_pos_x = Widgets.Rectangle(145, 105, 30, 30, 0xFFFFFF, 0xFFFFFF)
    rect_pos_y = Widgets.Rectangle(145, 105, 30, 30, 0xFFFFFF, 0xFFFFFF)
    rect0 = Widgets.Rectangle(145, 105, 30, 30, 0xFFFFFF, 0xFFFFFF)
    label0 = Widgets.Label("X 0", 11, 13, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Y 0", 13, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    joystick2_0 = Joystick2Unit(i2c0, 0x63)
    joystick2_0.set_deadzone_position(150, 150)


def loop():
    global \
        rect_neg_x, \
        rect_neg_y, \
        rect_pos_x, \
        rect_pos_y, \
        rect0, \
        label0, \
        label1, \
        i2c0, \
        joystick2_0, \
        pos_x, \
        pos_y, \
        x, \
        y, \
        last_x, \
        last_y
    M5.update()
    pos_x = joystick2_0.get_x_position()
    pos_y = joystick2_0.get_y_position()
    x = round(0.0390625 * pos_x)
    y = round(0.029296875 * pos_y)
    if last_x != x:
        last_x = x
        label0.setText(str((str("X: ") + str(pos_x))))
        if x < 0:
            rect_neg_x.setSize(w=(round(math.fabs(x))), h=30)
            rect_neg_x.setCursor(x=(160 - round(math.fabs(x))), y=105)
            rect_pos_x.setSize(w=0, h=30)
        else:
            rect_pos_x.setSize(w=(round(math.fabs(x)) + 30), h=30)
            rect_neg_x.setSize(w=0, h=30)
    if last_y != y:
        last_y = y
        label1.setText(str((str("Y: ") + str(pos_y))))
        if y < 0:
            rect_neg_y.setSize(w=30, h=(round(math.fabs(y))))
            rect_neg_y.setCursor(x=145, y=(120 - round(math.fabs(y))))
            rect_pos_y.setSize(w=0, h=30)
        else:
            rect_pos_y.setSize(w=30, h=(round(math.fabs(y)) + 30))
            rect_neg_y.setSize(w=0, h=30)
    rect0.setVisible(True)


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
