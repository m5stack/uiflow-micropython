# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from audio import Recorder
from audio import Player


recorder = None
player = None


def setup():
    global recorder, player

    M5.begin()
    Widgets.fillScreen(0x222222)

    recorder = Recorder(8000, 16, True)
    recorder.record("file://flash/res/audio/test.amr", 5, True)
    player = Player(None)
    player.play("file://flash/res/audio/test.amr", pos=0, volume=100, sync=True)


def loop():
    global recorder, player
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
