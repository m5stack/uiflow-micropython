# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import random


label_title = None
label_freq = None
label_tip = None
freq_hz = None


def btna_click_event_cb(state):
    global label_title, label_freq, label_tip, freq_hz
    print("tone")
    Speaker.tone(freq_hz, 200)
    freq_hz = random.randint(600, 1600)
    label_freq.setText(str((str("Freq: ") + str((str(freq_hz) + str("Hz"))))))


def setup():
    global label_title, label_freq, label_tip, freq_hz
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Speaker", 28, 5, 1.0, 0x1EC8E3, 0x000000, Widgets.FONTS.DejaVu18)
    label_freq = Widgets.Label(
        "Freq:600Hz", 5, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tip = Widgets.Label(
        "BtnA Tone", 19, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    Speaker.begin()
    Speaker.setVolumePercentage(0.9)
    freq_hz = 600
    label_freq.setText(str((str("Freq: ") + str((str(freq_hz) + str("Hz"))))))


def loop():
    global label_title, label_freq, label_tip, freq_hz
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
