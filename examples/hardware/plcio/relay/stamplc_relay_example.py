# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Relay


label0 = None
relay_0 = None


def btnA_wasClicked_event(state):  #  noqa: N802
    global label0, relay_0
    relay_0.on()


def btnB_wasClicked_event(state):  #  noqa: N802
    global label0, relay_0
    relay_0.off()


def btnC_wasClicked_event(state):  #  noqa: N802
    global label0, relay_0
    relay_0.set_status(not (relay_0.get_status()))


def setup():
    global label0, relay_0

    M5.begin()
    label0 = Widgets.Label("label0", 75, 28, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnC_wasClicked_event)

    relay_0 = Relay(1)


def loop():
    global label0, relay_0
    M5.update()
    label0.setText(str(relay_0.value()))


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
