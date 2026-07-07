# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time
from stamplc import StamPLC


title0 = None
label_relay1_state = None
label_relay2_state = None
label_relay3_state = None
stamplc_0 = None


last_time = None
state1 = None
laste_state1 = None
state2 = None
last_state2 = None
state3 = None
last_state3 = None


def setup():
    global \
        title0, \
        label_relay1_state, \
        label_relay2_state, \
        label_relay3_state, \
        stamplc_0, \
        last_time, \
        state1, \
        laste_state1, \
        state2, \
        last_state2, \
        state3, \
        last_state3

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title(
        "Input control relay", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat24
    )
    label_relay1_state = Widgets.Label(
        "Relay1: OFF", 10, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_relay2_state = Widgets.Label(
        "Relay2: OFF", 10, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_relay3_state = Widgets.Label(
        "Relay3: OFF", 10, 95, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    stamplc_0 = StamPLC()
    stamplc_0.led.red.value(1)


def loop():
    global \
        title0, \
        label_relay1_state, \
        label_relay2_state, \
        label_relay3_state, \
        stamplc_0, \
        last_time, \
        state1, \
        laste_state1, \
        state2, \
        last_state2, \
        state3, \
        last_state3
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        state1 = stamplc_0.input[1].value()
        if state1 != laste_state1:
            laste_state1 = state1
            if state1:
                stamplc_0.relay[1].value(1)
                label_relay1_state.setText(str("Relay1: ON"))
                label_relay1_state.setColor(0x009900, 0x000000)
            else:
                stamplc_0.relay[1].value(0)
                label_relay1_state.setText(str("Relay1: OFF"))
                label_relay1_state.setColor(0xFFFFFF, 0x000000)
        state2 = stamplc_0.input[2].value()
        if state2 != last_state2:
            last_state2 = state2
            if state2:
                stamplc_0.relay[2].value(1)
                label_relay2_state.setText(str("Relay2: ON"))
                label_relay2_state.setColor(0x009900, 0x000000)
            else:
                stamplc_0.relay[2].value(0)
                label_relay2_state.setText(str("Relay2: OFF"))
                label_relay2_state.setColor(0xFFFFFF, 0x000000)
        state3 = stamplc_0.input[3].value()
        if state3 != last_state3:
            last_state3 = last_state3
            if state3:
                stamplc_0.relay[3].value(1)
                label_relay3_state.setText(str("Relay3: ON"))
                label_relay3_state.setColor(0x009900, 0x000000)
            else:
                stamplc_0.relay[3].value(0)
                label_relay3_state.setText(str("Relay3: OFF"))
                label_relay3_state.setColor(0xFFFFFF, 0x000000)


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
