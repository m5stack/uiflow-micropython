# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import DCMotorModule
import time


title0 = None
label_speed = None
label_speed_val = None
label_encoder = None
label_encoder_value = None
module_dcmotor_0 = None
last_time = None
direction = None
speed = None
encoder_value = None


def setup():
    global \
        title0, \
        label_speed, \
        label_speed_val, \
        label_encoder, \
        label_encoder_value, \
        module_dcmotor_0, \
        last_time, \
        direction, \
        speed, \
        encoder_value

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("DCMotor Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_speed = Widgets.Label("Speed:", 5, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_speed_val = Widgets.Label("0", 105, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_encoder = Widgets.Label(
        "Encoder Value:", 5, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_encoder_value = Widgets.Label(
        "0", 203, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    module_dcmotor_0 = DCMotorModule()
    module_dcmotor_0.clear_encoder(1)
    direction = True
    speed = 0


def loop():
    global \
        title0, \
        label_speed, \
        label_speed_val, \
        label_encoder, \
        label_encoder_value, \
        module_dcmotor_0, \
        last_time, \
        direction, \
        speed, \
        encoder_value
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 100:
        last_time = time.ticks_ms()
        if direction:
            speed = speed + 5
            if speed >= 255:
                direction = False
        else:
            speed = speed - 5
            if speed <= -255:
                direction = True
        module_dcmotor_0.set_motor_speed(1, speed)
        label_speed_val.setText(str(speed))
        encoder_value = module_dcmotor_0.get_encoder(1)
        label_encoder_value.setText(str(encoder_value))
        module_dcmotor_0.clear_encoder(1)


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
