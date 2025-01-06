# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import SpeakerBase
from hardware import sdcard


base_spk = None


def setup():
    global base_spk

    M5.begin()
    base_spk = SpeakerBase(1, 5, 39, 38)
    sdcard.SDCard(slot=3, width=1, sck=7, miso=8, mosi=6, cs=None, freq=20000000)
    base_spk.playWavFile("/flash/res/audio/66.wav")
    base_spk.playWavFile("/sd/66.wav")


def loop():
    global base_spk
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
