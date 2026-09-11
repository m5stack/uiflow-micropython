# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import DoF6Unit
import time


title = None
live = None
yaw_caption = None
pitch_caption = None
roll_caption = None
label_yaw = None
label_pitch = None
label_roll = None
orientation_caption = None
degree_unit = None
sensor_caption = None
i2c0 = None
dof6_0 = None


last_time = None
UPDATE_DURATION_MS = None
attitude = None


def setup():
    global \
        title, \
        live, \
        yaw_caption, \
        pitch_caption, \
        roll_caption, \
        label_yaw, \
        label_pitch, \
        label_roll, \
        orientation_caption, \
        degree_unit, \
        sensor_caption, \
        i2c0, \
        dof6_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        attitude

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label(
        "DoF6 / Attitude", 12, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    live = Widgets.Label("Live", 272, 11, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    yaw_caption = Widgets.Label("Yaw", 12, 60, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14)
    pitch_caption = Widgets.Label(
        "Pitch", 113, 60, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    roll_caption = Widgets.Label(
        "Roll", 212, 60, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_yaw = Widgets.Label("---.-", 12, 84, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    label_pitch = Widgets.Label(
        "---.-", 112, 84, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24
    )
    label_roll = Widgets.Label(
        "---.-", 212, 84, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24
    )
    orientation_caption = Widgets.Label(
        "FUSED ORIENTATION", 12, 151, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    degree_unit = Widgets.Label(
        "DEG", 212, 151, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat14
    )
    sensor_caption = Widgets.Label(
        "BMI270  /  6-AXIS", 12, 207, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof6_0 = DoF6Unit(i2c0, addr=0x68)
    UPDATE_DURATION_MS = 20
    last_time = time.ticks_ms()


def loop():
    global \
        title, \
        live, \
        yaw_caption, \
        pitch_caption, \
        roll_caption, \
        label_yaw, \
        label_pitch, \
        label_roll, \
        orientation_caption, \
        degree_unit, \
        sensor_caption, \
        i2c0, \
        dof6_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        attitude
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        attitude = dof6_0.get_attitude()
        label_yaw.setText(str(round(attitude[0], 1)))
        label_pitch.setText(str(round(attitude[1], 1)))
        label_roll.setText(str(round(attitude[2], 1)))


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
