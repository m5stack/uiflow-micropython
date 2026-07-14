# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from hat import HAT18650CHat
import time


label_title = None
label_voltage = None
label_current = None
label_ctrl = None
i2c0 = None
hat_18650c_v11_0 = None


output = None
last_time = None
bat_voltage = None
bat_current = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        output, \
        last_time, \
        bat_voltage, \
        bat_current
    output = not output
    if output:
        hat_18650c_v11_0.set_boost_enable(True)
        label_ctrl.setText(str("OUT: ON"))
        label_voltage.setColor(0xCC0000, 0x000000)
        label_current.setColor(0xCC0000, 0x000000)
    else:
        hat_18650c_v11_0.set_boost_enable(False)
        label_ctrl.setText(str("OUT: OFF"))
        label_voltage.setColor(0xFFFFFF, 0x000000)
        label_current.setColor(0xFFFFFF, 0x000000)


def setup():
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        output, \
        last_time, \
        bat_voltage, \
        bat_current

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "OUTPUT", 28, 5, 1.0, 0x17EE6A, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_voltage = Widgets.Label(
        "Vol:", 7, 45, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_current = Widgets.Label(
        "Cur:", 3, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_ctrl = Widgets.Label(
        "OUT: OFF", 23, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(0), sda=Pin(8), freq=100000)
    hat_18650c_v11_0 = HAT18650CHat(i2c0)
    output = 0
    output = False
    hat_18650c_v11_0.set_boost_enable(False)


def loop():
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        output, \
        last_time, \
        bat_voltage, \
        bat_current
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        bat_voltage = hat_18650c_v11_0.get_battery_voltage()
        bat_current = hat_18650c_v11_0.get_battery_current()
        label_voltage.setText(str((str("Vol: ") + str(bat_voltage))))
        label_current.setText(str((str("Cur: ") + str(bat_current))))


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
