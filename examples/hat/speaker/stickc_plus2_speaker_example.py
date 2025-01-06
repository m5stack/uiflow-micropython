# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import SpeakerHat


hat_spk_0 = None


def setup():
    global hat_spk_0

    M5.begin()
    hat_spk_0 = SpeakerHat((26, 0))
    hat_spk_0.setVolumePercentage(1)
    hat_spk_0.tone(2000, 100)
    hat_spk_0.playWavFile("/flash/res/audio/poweron_2_5s.wav")


def loop():
    global hat_spk_0
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
