# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os
import sys
import io
import time

import M5
from M5 import *


label_title = None
label_btn_a = None
label_btn_b = None
label_hint = None

button_a_count = None
button_b_count = None


def btna_was_pressed_event(state):
    global button_a_count

    button_a_count = button_a_count + 1
    label_btn_a.setText(str("Button A: " + str(button_a_count)))


def btnb_was_pressed_event(state):
    global button_b_count

    button_b_count = button_b_count + 1
    label_btn_b.setText(str("Button B: " + str(button_b_count)))


def setup():
    global label_title, label_btn_a, label_btn_b, label_hint
    global button_a_count, button_b_count

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0xFFFFFF)
    label_title = Widgets.Label(
        "PaperDIY Button Counter",
        30,
        40,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat24,
    )
    label_btn_a = Widgets.Label(
        "Button A: 0",
        30,
        240,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat40,
    )
    label_btn_b = Widgets.Label(
        "Button B: 0",
        30,
        400,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat40,
    )
    label_hint = Widgets.Label(
        "Press Button A or Button B",
        30,
        600,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat24,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_PRESSED, cb=btna_was_pressed_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_PRESSED, cb=btnb_was_pressed_event)

    M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)
    button_a_count = 0
    button_b_count = 0


def loop():
    M5.update()
    time.sleep_ms(10)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as error:
        try:
            from utility import print_error_msg

            print_error_msg(error)
        except ImportError:
            print(error)
