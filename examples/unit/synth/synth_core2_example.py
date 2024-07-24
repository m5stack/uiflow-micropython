# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import SynthUnit
import time


synth_0 = None


def setup():
    global synth_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    Power.setExtOutput(True)
    Widgets.setBrightness(255)
    Widgets.fillScreen(0xFF6600)
    synth_0 = SynthUnit(port=(13, 14), id=1)
    synth_0.set_channel_volume(0, 127)
    synth_0.set_instrument(0, 9, 112)


def loop():
    global synth_0
    M5.update()
    synth_0.set_note_on(9, 0, 61)
    synth_0.set_note_on(9, 36, 127)
    time.sleep_ms(300)
    synth_0.set_note_on(9, 48, 124)
    synth_0.set_note_on(9, 60, 124)


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
