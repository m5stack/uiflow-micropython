# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DACUnit


label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
dac_0 = None


v = None


def btnA_wasClicked_event(state):  # noqa: N802
    global label0, label1, label2, label3, i2c0, dac_0, v
    if v >= 0.1:
        v = v - 0.1
    dac_0.set_voltage(v)


def btnB_wasClicked_event(state):  # noqa: N802
    global label0, label1, label2, label3, i2c0, dac_0, v
    if v < 3.3:
        v = v + 0.1
    dac_0.set_voltage(v)


def btnC_wasClicked_event(state):  # noqa: N802
    global label0, label1, label2, label3, i2c0, dac_0, v
    v = 0
    dac_0.set_voltage(v)


def setup():
    global label0, label1, label2, label3, i2c0, dac_0, v

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 133, 110, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("-", 60, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label2 = Widgets.Label("+", 143, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label3 = Widgets.Label("reset", 214, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnC_wasClicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    dac_0 = DACUnit(i2c0)
    v = 0


def loop():
    global label0, label1, label2, label3, i2c0, dac_0, v
    M5.update()
    label0.setText(str(dac_0.get_voltage()))


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
