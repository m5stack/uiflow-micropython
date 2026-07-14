# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import HAT18650CHat
from hardware import Pin
from hardware import I2C
import time


label_title = None
label_voltage = None
label_current = None
label_iset = None
label_ctrl = None
i2c0 = None
hat_18650c_v11_0 = None


iset = None
last_time = None
bat_voltage = None
bat_current = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_iset, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        iset, \
        last_time, \
        bat_voltage, \
        bat_current
    if hat_18650c_v11_0.get_charge_enable():
        hat_18650c_v11_0.set_charge_enable(False)
        label_ctrl.setText(str("Chg: OFF"))
    else:
        hat_18650c_v11_0.set_charge_enable(True)
        label_ctrl.setText(str("Chg: ON"))


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_iset, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        iset, \
        last_time, \
        bat_voltage, \
        bat_current
    iset = iset + 500
    if iset > 2500:
        iset = 500
    hat_18650c_v11_0.set_charge_current(iset)
    label_iset.setText(str((str("ISET: ") + str((str(iset) + str(" mA"))))))


def setup():
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_iset, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        iset, \
        last_time, \
        bat_voltage, \
        bat_current

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Charge", 22, 5, 1.0, 0x17EE6A, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_voltage = Widgets.Label(
        "Vol:", 7, 45, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_current = Widgets.Label(
        "Cur:", 3, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_iset = Widgets.Label(
        "ISET: 500mA", 3, 179, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_ctrl = Widgets.Label(
        "CHG: ON", 26, 214, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(0), sda=Pin(8), freq=100000)
    hat_18650c_v11_0 = HAT18650CHat(i2c0)
    hat_18650c_v11_0.set_charge_enable(True)
    iset = 500
    hat_18650c_v11_0.set_charge_voltage(4.2)


def loop():
    global \
        label_title, \
        label_voltage, \
        label_current, \
        label_iset, \
        label_ctrl, \
        i2c0, \
        hat_18650c_v11_0, \
        iset, \
        last_time, \
        bat_voltage, \
        bat_current
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        bat_voltage = hat_18650c_v11_0.get_battery_voltage()
        bat_current = hat_18650c_v11_0.get_battery_current()
        print(hat_18650c_v11_0.get_battery_power())
        label_voltage.setText(str((str("Vol: ") + str((str(bat_voltage) + str("V"))))))
        label_current.setText(str((str("Cur: ") + str((str(bat_current) + str("A"))))))
        if hat_18650c_v11_0.is_charging():
            label_voltage.setColor(0x009900, 0x000000)
            label_current.setColor(0x009900, 0x000000)
        else:
            label_voltage.setColor(0xFFFFFF, 0x000000)
            label_current.setColor(0xFFFFFF, 0x000000)


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
