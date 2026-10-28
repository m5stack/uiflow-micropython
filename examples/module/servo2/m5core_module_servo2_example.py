# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import Servo2Module


title = None
label_angle = None
servo2_0 = None
angle = None


def btna_was_clicked_event(state):
    global title, label_angle, servo2_0, angle
    angle = 0
    label_angle.setText(str((str("Angle: ") + str(angle))))
    servo2_0.position(1, degrees=angle)
    servo2_0.position(2, degrees=angle)


def btnb_was_clicked_event(state):
    global title, label_angle, servo2_0, angle
    angle = 45
    label_angle.setText(str((str("Angle: ") + str(angle))))
    servo2_0.position(1, degrees=angle)
    servo2_0.position(2, degrees=angle)


def btnc_was_clicked_event(state):
    global title, label_angle, servo2_0, angle
    angle = 90
    label_angle.setText(str((str("Angle: ") + str(angle))))
    servo2_0.position(1, degrees=angle)
    servo2_0.position(2, degrees=angle)


def setup():
    global title, label_angle, servo2_0, angle

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title("Module Servo2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_angle = Widgets.Label("Angle: ", 46, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    servo2_0 = Servo2Module(0x40, 50, 400, 2350, 180)
    angle = 0
    label_angle.setText(str((str("Angle: ") + str(angle))))
    servo2_0.position(1, degrees=angle)
    servo2_0.position(2, degrees=angle)
    servo2_0.release(0)


def loop():
    global title, label_angle, servo2_0, angle
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
