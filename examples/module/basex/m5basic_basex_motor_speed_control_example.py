# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX
import time


label_title = None
label_mode = None
label_target = None
label_feedback = None
label_btn1 = None
label_btn2 = None
label_btn3 = None
basex_0 = None
speed_target = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    speed_target = speed_target + 5
    if speed_target > 20:
        speed_target = 20
    basex_0.set_motor_speed_target(1, speed_target)
    label_target.setText(str((str("target speed: ") + str(speed_target))))


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    speed_target = speed_target - 5
    if speed_target < -20:
        speed_target = -20
    basex_0.set_motor_speed_target(1, speed_target)
    label_target.setText(str((str("target speed: ") + str(speed_target))))


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    speed_target = 0
    basex_0.set_motor_speed_target(1, speed_target)
    label_target.setText(str((str("target speed: ") + str(speed_target))))


def setup():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Speed Control", 34, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_mode = Widgets.Label(
        "control mode: speed", 20, 65, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_target = Widgets.Label(
        "target speed: 0", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_feedback = Widgets.Label(
        "speed20ms: --", 20, 145, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label("+5", 55, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)
    label_btn2 = Widgets.Label("-5", 145, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)
    label_btn3 = Widgets.Label("0", 245, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    speed_target = 0
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(1, 0)
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_speed_pid(1, 3, 1, 15)
    basex_0.set_motor_speed_target(1, 0)
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_SPEED)
    label_target.setText(str("target speed: 0"))
    label_feedback.setText(str("speed20ms: --"))


def loop():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    M5.update()
    label_feedback.setText(str((str("speed20ms: ") + str(basex_0.get_motor_speed_20ms(1)))))
    time.sleep_ms(100)


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
