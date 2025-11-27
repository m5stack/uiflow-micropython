# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from stamplc import ACStamPLC



title0 = None
label0 = None
label1 = None
stamplc_ac_0 = None
relay_state = None


def btnA_wasClicked_event(state):
    global title0, label0, label1, stamplc_ac_0, relay_state
    relay_state = not relay_state
    stamplc_ac_0.set_relay(relay_state)
    if relay_state:
        stamplc_ac_0.set_red_led(True)
    else:
        stamplc_ac_0.set_red_led(False)

def setup():
    global title0, label0, label1, stamplc_ac_0, relay_state

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("StamPLC AC Ctrl", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Press button A toggle", 5, 35, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("relay state", 5, 60, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    stamplc_ac_0 = ACStamPLC()
    relay_state = False
    stamplc_ac_0.set_red_led(False)
    stamplc_ac_0.set_green_led(False)
    stamplc_ac_0.set_blue_led(False)


def loop():
    global title0, label0, label1, stamplc_ac_0, relay_state
    M5.update()


if __name__ == '__main__':
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
