# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicStepmotorBase
import time


title0 = None
label0 = None
label_vol = None
base_stepmotor = None
step_per_rev = None
microstep = None
rotate_circle = None
total_steps = None


def setup():
    global \
        title0, \
        label0, \
        label_vol, \
        base_stepmotor, \
        step_per_rev, \
        microstep, \
        rotate_circle, \
        total_steps
    M5.begin()
    title0 = Widgets.Title("Steps Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("vol:", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("12.0V", 43, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    step_per_rev = 200
    microstep = 1 / 2
    rotate_circle = 5
    total_steps = (step_per_rev / microstep) * rotate_circle
    base_stepmotor = AtomicStepmotorBase(5, 7, 6, 38, 39, 8)
    label_vol.setText(str((str((base_stepmotor.get_voltage())) + str("V"))))


def loop():
    global \
        title0, \
        label0, \
        label_vol, \
        base_stepmotor, \
        step_per_rev, \
        microstep, \
        rotate_circle, \
        total_steps
    M5.update()
    print(base_stepmotor.get_voltage())
    base_stepmotor.rotate(total_steps, 1, True)
    time.sleep_ms(100)
    base_stepmotor.rotate(total_steps, 1, False)
    time.sleep_ms(100)
    label_vol.setText(str((str((base_stepmotor.get_voltage())) + str("V"))))
    time.sleep_ms(2000)


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
