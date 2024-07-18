# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import DACHat


label0 = None
i2c0 = None
hat_dac_0 = None


v = None


def btnA_wasClicked_event(state):  # noqa: N802
    global label0, i2c0, hat_dac_0, v
    if v >= 0.1:
        v = v - 0.1
    hat_dac_0.set_voltage(v)


def btnB_wasClicked_event(state):  # noqa: N802
    global label0, i2c0, hat_dac_0, v
    if v < 3.3:
        v = v + 0.1
    hat_dac_0.set_voltage(v)


def btnPWR_wasClicked_event(state):  # noqa: N802
    global label0, i2c0, hat_dac_0, v
    v = 0
    hat_dac_0.set_voltage(v)


def setup():
    global label0, i2c0, hat_dac_0, v

    M5.begin()
    label0 = Widgets.Label("label0", 39, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_dac_0 = DACHat(i2c0)
    v = 0


def loop():
    global label0, i2c0, hat_dac_0, v
    M5.update()
    label0.setText(str(hat_dac_0.get_voltage()))


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
