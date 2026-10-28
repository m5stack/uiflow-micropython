# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit
from hardware import Pin
from hardware import I2C


title0 = None
label0 = None
i2c0 = None
cardkb2_0 = None


char = None


def cardkb2_0_i2c_pressed_event(kb):
    global title0, label0, i2c0, cardkb2_0, char
    char = cardkb2_0.get_char()
    label0.setText(str((str(char) + str(" was pressed"))))
    print((str(char) + str(" was pressed")))


def setup():
    global title0, label0, i2c0, cardkb2_0, char

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CardKB2 I2C Mode Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    cardkb2_0 = CardKBUnit(i2c0, mode=CardKBUnit.CardKB_I2C_MODE)
    cardkb2_0.set_callback(cardkb2_0_i2c_pressed_event)
    char = ""


def loop():
    global title0, label0, i2c0, cardkb2_0, char
    M5.update()
    cardkb2_0.tick()


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
