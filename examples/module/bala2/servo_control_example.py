# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import Bala2Module
import time


title0 = None
label_servo1 = None
label_servo1_val = None
module_bala2_0 = None
t_dir = None
last_time = None
angle = None


def setup():
    global title0, label_servo1, label_servo1_val, module_bala2_0, t_dir, last_time, angle
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Bala2 Servo Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_servo1 = Widgets.Label("Angle:", 54, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_servo1_val = Widgets.Label("0", 125, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    module_bala2_0 = Bala2Module(0)
    t_dir = True
    angle = 0
    last_time = time.ticks_ms()


def loop():
    global title0, label_servo1, label_servo1_val, module_bala2_0, t_dir, last_time, angle
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 10:
        last_time = time.ticks_ms()
        angle = angle + 1
        if angle > 180:
            angle = 0
            t_dir = not t_dir
        if t_dir:
            module_bala2_0.set_servo_angle(1, angle)
        else:
            module_bala2_0.set_servo_angle(1, 180 - angle)
        label_servo1_val.setText(str(angle))


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
