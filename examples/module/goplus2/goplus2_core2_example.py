# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import GoPlus2Module
import time


title0 = None
label0 = None
label1 = None
goplus20 = None


def setup():
    global title0, label0, label1, goplus20

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("GoPlus2 Module Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Motor Speed:", 2, 72, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Servo Angle:", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    goplus20 = GoPlus2Module(0x38)
    goplus20.set_digital_output(1, 1)
    goplus20.set_digital_output(2, 1)
    goplus20.set_digital_output(3, 1)


def loop():
    global title0, label0, label1, goplus20
    M5.update()
    label0.setText(str((str("Motor Speed:") + str("180"))))
    label1.setText(str((str("Servo Angle:") + str("-127"))))
    goplus20.set_servo_angle(1, 180)
    goplus20.set_servo_angle(2, 180)
    goplus20.set_servo_angle(3, 180)
    goplus20.set_servo_angle(4, 180)
    goplus20.set_motor_speed(1, -127)
    goplus20.set_motor_speed(2, -127)
    time.sleep(4)
    label0.setText(str((str("Motor Speed:") + str("-180"))))
    label1.setText(str((str("Servo Angle:") + str("127"))))
    goplus20.set_servo_angle(1, 0)
    goplus20.set_servo_angle(2, 0)
    goplus20.set_servo_angle(3, 0)
    goplus20.set_servo_angle(4, 127)
    goplus20.set_motor_speed(1, 127)
    time.sleep(4)


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
