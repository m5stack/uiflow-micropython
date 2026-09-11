# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import DoF9Unit
import time


title = None
live = None
heading_caption = None
label_heading = None
degree_unit = None
compensation_caption = None
sensor_caption = None
i2c0 = None
dof9_0 = None


last_time = None
UPDATE_DURATION_MS = None


def setup():
    global \
        title, \
        live, \
        heading_caption, \
        label_heading, \
        degree_unit, \
        compensation_caption, \
        sensor_caption, \
        i2c0, \
        dof9_0, \
        last_time, \
        UPDATE_DURATION_MS

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label(
        "DoF9 / Compass", 12, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    live = Widgets.Label("Live", 272, 11, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    heading_caption = Widgets.Label(
        "Magnetic Heading", 12, 48, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_heading = Widgets.Label(
        "---.-", 12, 70, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat40
    )
    degree_unit = Widgets.Label(
        "DEG", 174, 91, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat18
    )
    compensation_caption = Widgets.Label(
        "TILT COMPENSATED", 12, 153, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    sensor_caption = Widgets.Label(
        "BMI270 + BMM350", 12, 207, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof9_0 = DoF9Unit(i2c0, addr=0x68)
    UPDATE_DURATION_MS = 100
    last_time = time.ticks_ms()


def loop():
    global \
        title, \
        live, \
        heading_caption, \
        label_heading, \
        degree_unit, \
        compensation_caption, \
        sensor_caption, \
        i2c0, \
        dof9_0, \
        last_time, \
        UPDATE_DURATION_MS
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        label_heading.setText(str(round(dof9_0.get_heading(), 1)))


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
