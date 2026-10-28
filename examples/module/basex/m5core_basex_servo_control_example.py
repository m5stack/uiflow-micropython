# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX


label_title = None
label_angle1 = None
label_angle2 = None
label_btn1 = None
label_btn2 = None
label_btn3 = None
basex_0 = None
angle1 = None
agnle2 = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    angle1 = angle1 + 30
    if angle1 > 180:
        angle1 = 0
    basex_0.set_servo_angle(1, angle1)
    label_angle1.setText(str((str("Servo1 Angle: ") + str(angle1))))


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    agnle2 = agnle2 + 30
    if agnle2 > 180:
        agnle2 = 0
    basex_0.set_servo_angle(2, agnle2)
    label_angle2.setText(str((str("Servo2 Angle: ") + str(agnle2))))


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    angle1 = 0
    agnle2 = 0
    basex_0.set_servo_angle(1, 0)
    basex_0.set_servo_angle(2, 0)
    label_angle1.setText(str("Servo1 Angle:  0"))
    label_angle2.setText(str("Servo2 Angle:  0"))


def setup():
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Servo Control", 36, 1, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_angle1 = Widgets.Label(
        "Servo1 Angle: --", 20, 70, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_angle2 = Widgets.Label(
        "Servo2 Angle: --", 20, 110, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label(
        "Servo1", 38, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn2 = Widgets.Label(
        "Servo2", 124, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn3 = Widgets.Label(
        "Reset", 219, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    angle1 = 0
    agnle2 = 0
    label_angle1.setText(str("Servo1 Angle:  0"))
    label_angle2.setText(str("Servo2 Angle:  0"))


def loop():
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    M5.update()


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
