# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicPWMBase
import time


title0 = None
label0 = None
label1 = None
label_freq = None
label_duty = None
base_pwm = None
i = None


def setup():
    global title0, label0, label1, label_freq, label_duty, base_pwm, i
    M5.begin()
    title0 = Widgets.Title("PWM Control", 0, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("freq:", 1, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("duty:", 2, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_freq = Widgets.Label("1000Hz", 47, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_duty = Widgets.Label("0", 55, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    base_pwm = AtomicPWMBase(5, 1000)
    label_freq.setText(str((str((base_pwm.get_freq())) + str("Hz"))))


def loop():
    global title0, label0, label1, label_freq, label_duty, base_pwm, i
    M5.update()
    for i in range(100):
        base_pwm.set_duty_u16(i * 150)
        label_duty.setText(str(base_pwm.get_duty_u16()))
        time.sleep_ms(40)
    for i in range(100):
        base_pwm.set_duty_u16(15000 - i * 150)
        label_duty.setText(str(base_pwm.get_duty_u16()))
        time.sleep_ms(40)


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
