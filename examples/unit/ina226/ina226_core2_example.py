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
import time
from unit import INA226Unit


page0 = None
label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
ina226_0 = None


def setup():
    global page0, label0, label1, label2, label3, i2c0, ina226_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "Bus Voltage:",
        x=0,
        y=56,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "Current:",
        x=0,
        y=88,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "Power:",
        x=0,
        y=124,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label3 = m5ui.M5Label(
        "Shunt Voltage:",
        x=0,
        y=161,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    ina226_0 = INA226Unit(i2c0, 0x41, type="1A")
    page0.screen_load()


def loop():
    global page0, label0, label1, label2, label3, i2c0, ina226_0
    M5.update()
    time.sleep_ms(500)
    label0.set_text(
        str((str("Bus Voltage:") + str((str((ina226_0.read_bus_voltage())) + str("V")))))
    )
    label1.set_text(str((str("Current:") + str((str((ina226_0.read_current())) + str("A"))))))
    label2.set_text(str((str("Power:") + str((str((ina226_0.read_power())) + str("W"))))))
    label3.set_text(
        str((str("Shunt Voltage:") + str((str((ina226_0.read_shunt_voltage())) + str("V")))))
    )


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
