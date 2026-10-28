# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX
import time


label_title = None
label_encoder1 = None
label_encoder2 = None
label_encoder3 = None
label_encoder4 = None
label_btn2 = None
basex_0 = None


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_encoder1, \
        label_encoder2, \
        label_encoder3, \
        label_encoder4, \
        label_btn2, \
        basex_0
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_encoder(2, 0)
    basex_0.set_motor_encoder(3, 0)
    basex_0.set_motor_encoder(4, 0)


def setup():
    global \
        label_title, \
        label_encoder1, \
        label_encoder2, \
        label_encoder3, \
        label_encoder4, \
        label_btn2, \
        basex_0

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Encoder", 58, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_encoder1 = Widgets.Label(
        "M1 encoder: --", 20, 45, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_encoder2 = Widgets.Label(
        "M2 encoder: --", 20, 75, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_encoder3 = Widgets.Label(
        "M3 encoder: --", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_encoder4 = Widgets.Label(
        "M4 encoder: --", 20, 135, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn2 = Widgets.Label(
        "B: Clear All", 108, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    basex_0 = ModuleBaseX()
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(1, 0)
    basex_0.set_motor_mode(2, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(2, 0)
    basex_0.set_motor_mode(3, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(3, 0)
    basex_0.set_motor_mode(4, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(4, 0)
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_encoder(2, 0)
    basex_0.set_motor_encoder(3, 0)
    basex_0.set_motor_encoder(4, 0)


def loop():
    global \
        label_title, \
        label_encoder1, \
        label_encoder2, \
        label_encoder3, \
        label_encoder4, \
        label_btn2, \
        basex_0
    M5.update()
    label_encoder1.setText(str((str("M1 encoder: ") + str((basex_0.get_motor_encoder(1))))))
    label_encoder2.setText(str((str("M2 encoder: ") + str((basex_0.get_motor_encoder(2))))))
    label_encoder3.setText(str((str("M3 encoder: ") + str((basex_0.get_motor_encoder(3))))))
    label_encoder4.setText(str((str("M4 encoder: ") + str((basex_0.get_motor_encoder(4))))))
    time.sleep_ms(200)


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
