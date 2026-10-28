# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX


label_title = None
label_speed = None
label_btn1 = None
label_btn2 = None
label_mode = None
label_btn3 = None
basex_0 = None
pwm = None
i = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
    pwm = pwm + 20
    if pwm > 120:
        pwm = 0
    for i in range(4):
        basex_0.set_motor_pwm(i + 1, pwm)

    label_speed.setText(str((str("motor pwm: ") + str(pwm))))


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
    pwm = pwm - 20
    if pwm < -120:
        pwm = 0
    for i in range(4):
        basex_0.set_motor_pwm(i + 1, pwm)

    label_speed.setText(str((str("motor pwm: ") + str(pwm))))


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
    pwm = 0
    for i in range(4):
        basex_0.set_motor_pwm(i + 1, 0)

    label_speed.setText(str("motor pwm: "))


def setup():
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Motor Control", 34, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_speed = Widgets.Label(
        "motor pwm: 0", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label("+20", 50, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)
    label_btn2 = Widgets.Label(
        "-20", 140, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_mode = Widgets.Label(
        "control mode: normal", 20, 70, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn3 = Widgets.Label("0", 238, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    pwm = 0
    label_speed.setText(str("motor pwm: 0"))
    for i in range(4):
        basex_0.set_motor_mode(i + 1, ModuleBaseX.MOTOR_MODE_NORMAL)
        basex_0.set_motor_pwm(i + 1, 0)


def loop():
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
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
