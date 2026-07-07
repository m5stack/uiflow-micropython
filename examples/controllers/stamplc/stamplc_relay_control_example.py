# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from stamplc import StamPLC


title0 = None
label_tip = None
label_state = None
stamplc_0 = None


def btna_was_clicked_event(state):
    global title0, label_tip, label_state, stamplc_0
    stamplc_0.relay[1].toggle()
    if stamplc_0.relay[1].value():
        label_state.setText(str("Realy1: ON"))
        label_state.setCursor(x=55, y=53)
        label_state.setColor(0x009900, 0x000000)
    else:
        label_state.setText(str("Realy1: OFF"))
        label_state.setCursor(x=50, y=53)
        label_state.setColor(0xFFFFFF, 0x000000)


def setup():
    global title0, label_tip, label_state, stamplc_0

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Relay Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat24)
    label_tip = Widgets.Label(
        "BtnA control relay1", 33, 103, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_state = Widgets.Label(
        "Realy1: OFF", 50, 53, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)

    stamplc_0 = StamPLC()
    stamplc_0.led.blue.on()


def loop():
    global title0, label_tip, label_state, stamplc_0
    M5.update()


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
