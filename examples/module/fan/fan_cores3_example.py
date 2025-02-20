# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import FanModule
import time


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
fan_v11_0 = None


def setup():
    global title0, label0, label1, label2, label3, fan_v11_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "FanModuleV1.1 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 94, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 133, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 0, 168, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    fan_v11_0 = FanModule(address=0x18)
    fan_v11_0.set_fan_state(True)
    fan_v11_0.set_pwm_frequency(0)
    fan_v11_0.set_pwm_duty_cycle(80)


def loop():
    global title0, label0, label1, label2, label3, fan_v11_0
    M5.update()
    label0.setText(str((str("Fan State:") + str((fan_v11_0.get_fan_state())))))
    label1.setText(str((str("Fan PWM Freq:") + str((fan_v11_0.get_single_frequency())))))
    label2.setText(str((str("Fan PWM duty cycle:") + str((fan_v11_0.get_pwm_duty_cycle())))))
    label3.setText(str((str("Fan rpm:") + str((fan_v11_0.get_fan_rpm())))))
    if M5.Touch.getCount():
        fan_v11_0.set_fan_state(not (fan_v11_0.get_fan_state()))
        time.sleep_ms(50)


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
