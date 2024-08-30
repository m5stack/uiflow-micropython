# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import MIDIUnit
import time


title0 = None
label0 = None
midi_0 = None


def setup():
    global title0, label0, midi_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Unit MIDI Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("PLaying", 124, 101, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    Power.setExtOutput(True)
    midi_0 = MIDIUnit(id=1, port=(18, 17))
    midi_0.set_channel_volume(0, 111)
    Widgets.fillScreen(0xFFCC66)
    midi_0.set_instrument(0, 0, 112)


def loop():
    global title0, label0, midi_0
    M5.update()
    midi_0.set_note_on(0, 0, 127)
    midi_0.set_note_on(0, 36, 127)
    time.sleep_ms(300)
    midi_0.set_note_on(0, 48, 127)
    midi_0.set_note_on(0, 60, 127)


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
