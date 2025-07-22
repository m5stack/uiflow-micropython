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
from unit import ENVPROUnit
import time


page0 = None
bar0 = None
label0 = None
i2c0 = None
envpro_0 = None


def setup():
    global page0, bar0, label0, i2c0, envpro_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    bar0 = m5ui.M5Bar(
        x=148,
        y=21,
        w=20,
        h=200,
        min_value=0,
        max_value=50,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=181,
        y=112,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    envpro_0 = ENVPROUnit(i2c0)
    page0.screen_load()
    bar0.set_bg_grad_color(
        0xFF0000, 255, 0x0000FF, 255, lv.GRAD_DIR.VER, lv.PART.INDICATOR | lv.STATE.DEFAULT
    )


def loop():
    global page0, bar0, label0, i2c0, envpro_0
    M5.update()
    bar0.set_value(int(envpro_0.get_temperature()), True)
    label0.set_text(str(envpro_0.get_temperature()))
    time.sleep(1)


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
