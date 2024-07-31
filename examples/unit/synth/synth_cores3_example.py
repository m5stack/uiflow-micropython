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

    synth_0 = SynthUnit(1, port=(1, 2))
    synth_0.set_channel_volume(0, 64)
    synth_0.set_instrument(0, 0, 112)


def loop():
    global synth_0
    M5.update()
    synth_0.set_note_on(0, 0, 61)
    synth_0.set_note_on(0, 36, 127)
    time.sleep_ms(300)
    synth_0.set_note_on(0, 48, 124)
    synth_0.set_note_on(0, 60, 124)


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
