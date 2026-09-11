# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import DoF10Unit
import time


title = None
live = None
pressure_caption = None
label_pressure = None
pressure_unit = None
altitude_caption = None
label_altitude = None
altitude_unit = None
temperature_caption = None
label_temperature = None
temperature_unit = None
sea_level_caption = None
i2c0 = None
dof10_0 = None


UPDATE_DURATION_MS = None
last_time = None


def setup():
    global \
        title, \
        live, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        sea_level_caption, \
        i2c0, \
        dof10_0, \
        UPDATE_DURATION_MS, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label(
        "DoF10 / Barometer", 12, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    live = Widgets.Label("Live", 272, 11, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    pressure_caption = Widgets.Label(
        "Pressure", 12, 44, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_pressure = Widgets.Label(
        "----.--", 12, 62, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat40
    )
    pressure_unit = Widgets.Label(
        "hPa", 170, 84, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    altitude_caption = Widgets.Label(
        "Altitude", 12, 132, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_altitude = Widgets.Label(
        "---.-", 12, 151, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24
    )
    altitude_unit = Widgets.Label(
        "m", 116, 158, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat18
    )
    temperature_caption = Widgets.Label(
        "SPL06 Temp", 170, 132, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_temperature = Widgets.Label(
        "--.-", 170, 151, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat24
    )
    temperature_unit = Widgets.Label(
        "DEG C", 244, 158, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    sea_level_caption = Widgets.Label(
        "SEA LEVEL  1013.25 hPa", 12, 211, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof10_0 = DoF10Unit(i2c0, addr=0x68)
    dof10_0.set_sea_level_pressure(1013.25)
    UPDATE_DURATION_MS = 100
    last_time = time.ticks_ms()


def loop():
    global \
        title, \
        live, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        sea_level_caption, \
        i2c0, \
        dof10_0, \
        UPDATE_DURATION_MS, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        label_pressure.setText(str(round(dof10_0.get_pressure(), 2)))
        label_altitude.setText(str(round(dof10_0.get_altitude(), 1)))
        label_temperature.setText(str(round(dof10_0.get_temperature("pressure"), 1)))


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
