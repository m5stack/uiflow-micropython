# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from hardware import Pin
from hardware import I2C
import time


label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None


import math

pwm = None
duty = None
FREQUENCY_HZ = None
last_time = None


# Describe this function...
def apply_duty():
    global \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time, \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2
    pwm = stp2.PWM(
        0, freq=FREQUENCY_HZ, duty_u16=math.floor((duty * 65535) / 100), duty_ns=None, invert=False
    )


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    if duty > 0:
        duty = duty + -10
    apply_duty()


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    duty = 0
    apply_duty()


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    if duty < 100:
        duty = duty + 10
    apply_duty()


def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "PWM Output", 98, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "PWM0 / G3 -> oscilloscope or LED",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "PWM0 / G3 Duty", 12, 78, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "Shared Frequency", 12, 134, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Duty -10", 36, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 152, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Zero", 139, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 245, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "Duty +10", 216, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    FREQUENCY_HZ = 1000
    duty = 0
    apply_duty()
    last_time = time.ticks_ms()


def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        label_value1.setText(str((str(duty) + str("%"))))
        label_value2.setText(str((str((stp2.get_pwm_frequency())) + str(" Hz"))))
        print((str("PWM0 duty: ") + str(duty)))


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
