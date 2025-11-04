# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB


rgb = None
led1_state = None
led2_state = None


def btna_was_clicked_event(state):
    global rgb, led1_state, led2_state
    print("clicke left")
    led1_state = not led1_state
    if led1_state:
        rgb.set_color(0, 0x009900)
    else:
        rgb.set_color(0, 0x000000)


def btnb_was_clicked_event(state):
    global rgb, led1_state, led2_state
    print("click right")
    led2_state = not led2_state
    if led2_state:
        rgb.set_color(1, 0x009900)
    else:
        rgb.set_color(1, 0x000000)


def setup():
    global rgb, led1_state, led2_state

    M5.begin()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    rgb = RGB()
    rgb.set_color(0, 0x33CCFF)
    rgb.set_color(1, 0x33CCFF)


def loop():
    global rgb, led1_state, led2_state
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
