# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *


circle0 = None
label0 = None


x = None
y = None


def setup():
    global circle0, label0, x, y

    M5.begin()
    Widgets.fillScreen(0x222222)
    circle0 = Widgets.Circle(160, 120, 60, 0xFFFFFF, 0xFFFFFF)
    label0 = Widgets.Label("Play", 141, 110, 1.0, 0x222222, 0xFFFFFF, Widgets.FONTS.DejaVu18)

    Speaker.begin()
    Speaker.playWavFile("/flash/res/audio/poweron_2_5s.wav")


def loop():
    global circle0, label0, x, y
    M5.update()
    if M5.Touch.getCount():
        x = M5.Touch.getX()
        y = M5.Touch.getY()
        if x >= 130 and x <= 190 and y >= 90 and y <= 150:
            circle0.setColor(color=0xFF0000, fill_c=0xFF0000)
            label0.setColor(0xFFFFFF, 0xFF0000)
            label0.setText(str("Play..."))
            Speaker.playWavFile("/flash/res/audio/poweron_2_5s.wav")
            label0.setText(str("Play"))
            circle0.setColor(color=0xFFFFFF, fill_c=0xFFFFFF)
            label0.setColor(0x000000, 0xFFFFFF)


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
