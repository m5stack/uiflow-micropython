# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import PDMUnit
import time


label0 = None
title0 = None
pdm_0 = None


rec_data = None


def setup():
    global label0, title0, pdm_0, rec_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 128, 114, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("PDMUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    pdm_0 = PDMUnit((1, 2), i2s_port=2, sample_rate=44100)
    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.end()
    pdm_0.begin()
    rec_data = bytearray(44100 * 10)
    label0.setText(str("rec..."))
    pdm_0.record(rec_data, _, False)
    time.sleep_ms(100)
    while pdm_0.isRecording():
        label0.setText(str("rec..."))
        time.sleep_ms(100)
    pdm_0.end()
    Speaker.begin()
    label0.setText(str("play..."))
    Speaker.playRaw(rec_data, 44100 * 2)
    while Speaker.isPlaying():
        time.sleep_ms(100)
    label0.setText(str("done"))


def loop():
    global label0, title0, pdm_0, rec_data
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
