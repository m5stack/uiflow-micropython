# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import Speaker2Hat


title1 = None
label0 = None
label1 = None
hat_spk2_0 = None


def setup():
    global title1, label0, label1, hat_spk2_0

    Widgets.setRotation(3)
    M5.begin()
    title1 = Widgets.Title("SPK2 StickcPlus2 e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Press BtnA to Beep", 1, 39, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Press BtnB to play wav", 1, 74, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    hat_spk2_0 = Speaker2Hat((26, 0))
    hat_spk2_0.setVolumePercentage(1)


def loop():
    global title1, label0, label1, hat_spk2_0
    M5.update()
    if BtnA.wasPressed():
        hat_spk2_0.tone(2000, 100)
    if BtnB.wasPressed():
        hat_spk2_0.playWavFile("/flash/res/audio/poweron_2_5s.wav")


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
