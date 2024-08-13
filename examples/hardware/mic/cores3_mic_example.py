# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time


label0 = None


rec_data = None


def setup():
    global label0, rec_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 123, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.end()
    Mic.begin()
    rec_data = bytearray(8000 * 5)
    label0.setText(str("rec..."))
    Mic.record(rec_data, 8000, False)
    while Mic.isRecording():
        time.sleep_ms(500)
    Mic.end()
    Speaker.begin()
    label0.setText(str("play..."))
    Speaker.playRaw(rec_data, 8000)
    while Speaker.isPlaying():
        time.sleep_ms(500)
    label0.setText(str("done"))


def loop():
    global label0, rec_data
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
