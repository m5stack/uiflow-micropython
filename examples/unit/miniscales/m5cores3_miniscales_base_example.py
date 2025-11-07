# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import MiniScaleUnit
import time


page0 = None
label_title = None
label_weight = None
i2c0 = None
miniscales_0 = None
last_time = None
weight = None


def setup():
    global page0, label_title, label_weight, i2c0, miniscales_0, last_time, weight

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label_title = m5ui.M5Label(
        "MiniScales",
        x=94,
        y=5,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_weight = m5ui.M5Label(
        "Weights: -- g",
        x=81,
        y=90,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    miniscales_0 = MiniScaleUnit(i2c0)
    miniscales_0.set_average_filter_level(10)
    page0.screen_load()


def loop():
    global page0, label_title, label_weight, i2c0, miniscales_0, last_time, weight
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        weight = int(miniscales_0.weight)
        label_weight.set_text(str((str("Weight: ") + str((str(weight) + str(" g"))))))


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
