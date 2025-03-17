# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import Encoder4MotorModule


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
encoder4_motor_0 = None


def setup():
    global title0, label0, label1, label2, label3, encoder4_motor_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "4EncoderMotor Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 1, 56, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 1, 185, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    encoder4_motor_0 = Encoder4MotorModule(address=0x24)
    encoder4_motor_0.set_all_motors_mode(0x02)
    encoder4_motor_0.set_speed_point_value(0x00, 50)
    encoder4_motor_0.set_speed_point_value(0x01, 50)
    encoder4_motor_0.set_speed_point_value(0x02, 50)
    encoder4_motor_0.set_speed_point_value(0x03, 50)


def loop():
    global title0, label0, label1, label2, label3, encoder4_motor_0
    M5.update()
    label0.setText(
        str((str("Motor1 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x00)))))
    )
    label1.setText(
        str((str("Motor2 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x01)))))
    )
    label2.setText(
        str((str("Motor3 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x02)))))
    )
    label3.setText(
        str((str("Motor4 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x03)))))
    )


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
