# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from stamp import StampTimerPower2
import time


label_title = None
label_description = None
label_note = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
i2c0 = None
stp2 = None


last_time = None
value1 = None
adc1 = None
value2 = None
adc2 = None


def setup():
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        i2c0, \
        stp2, \
        last_time, \
        value1, \
        adc1, \
        value2, \
        adc2

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "ADC Input", 111, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "G1 / G2 analog input", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_note = Widgets.Label(
        "Input: 0..Vref; never connect 5V",
        12,
        54,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "ADC1 / G1  (Raw)", 12, 78, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "ADC2 / G2  (Raw)", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    adc1 = stp2.ADC(1)
    adc2 = stp2.ADC(2)
    last_time = time.ticks_ms()


def loop():
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        i2c0, \
        stp2, \
        last_time, \
        value1, \
        adc1, \
        value2, \
        adc2
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        value1 = stp2.read_adc_raw(1)
        value2 = stp2.read_adc_raw(2)
        label_value1.setText(str(str(value1)))
        label_value2.setText(str(str(value2)))
        print((str((str((str("ADC G1: ") + str(value1))) + str(" G2: "))) + str(value2)))


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
