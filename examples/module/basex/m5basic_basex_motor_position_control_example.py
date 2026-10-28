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
label_encoder = None
label_btn1 = None
label_btn2 = None
label_btn3 = None
basex_0 = None


position_target = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    position_target = 720
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, position_target)
    label_target.setText(str((str("target pos: ") + str(position_target))))


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    position_target = -720
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, position_target)
    label_target.setText(str((str("target pos: ") + str(position_target))))


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    position_target = 0
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, position_target)
    label_target.setText(str((str("target pos: ") + str(position_target))))


def setup():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Position Control", 16, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_mode = Widgets.Label(
        "control mode: position", 20, 65, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_target = Widgets.Label(
        "target pos: 0", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_encoder = Widgets.Label(
        "encoder: 0", 20, 145, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label(
        "+720", 45, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn2 = Widgets.Label(
        "-720", 136, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn3 = Widgets.Label(
        "Reset", 220, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    position_target = 0
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(1, 0)
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, 0)
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    label_target.setText(str("target pos: 0"))
    label_encoder.setText(str("encoder: 0"))


def loop():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    M5.update()
    label_encoder.setText(str((str("encoder: ") + str((basex_0.get_motor_encoder(1))))))
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
