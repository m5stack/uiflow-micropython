# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import AudioModule


audio_0 = None


def setup():
    global audio_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    audio_0 = AudioModule(
        0,
        16000,
        i2s_sck=7,
        i2s_ws=6,
        i2s_di=14,
        i2s_do=13,
        i2s_mclk=0,
        work_mode=AudioModule.MODE_HEADPHONE,
        offset=False,
        mux=AudioModule.MUX_NATIONAL,
    )
    audio_0.play_wav_file("/flash/res/audio/66.wav")


def loop():
    global audio_0
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            audio_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
