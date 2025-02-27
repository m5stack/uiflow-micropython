# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import DigitalInput


label0 = None
digitalinput_0 = None


def digitalinput_0_falling_event(args):
    global label0, digitalinput_0
    label0.setText(str(digitalinput_0.value()))


def digitalinput_0_rising_event(args):
    global label0, digitalinput_0
    label0.setText(str(digitalinput_0.value()))


def setup():
    global label0, digitalinput_0

    M5.begin()
    label0 = Widgets.Label("label0", 112, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    digitalinput_0 = DigitalInput(1)
    digitalinput_0.irq(digitalinput_0_falling_event, digitalinput_0.IRQ_FALLING)
    digitalinput_0.irq(digitalinput_0_rising_event, digitalinput_0.IRQ_RISING)
    label0.setText(str(digitalinput_0.value()))


def loop():
    global label0, digitalinput_0
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
