# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import AudioPlayerUnit
import time


title0 = None
label0 = None
label1 = None
label2 = None
audioplayer_0 = None


play_state = None


def btn_b_was_pressed_event(state):
    global title0, label0, label1, label2, audioplayer_0, play_state
    if play_state:
        audioplayer_0.pause_audio()
    else:
        audioplayer_0.play_audio()


def setup():
    global title0, label0, label1, label2, audioplayer_0, play_state

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "AudioPlayerUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(">||", 145, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 71, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 123, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_PRESSED, cb=btn_b_was_pressed_event)

    audioplayer_0 = AudioPlayerUnit(2, port=(33, 32))
    audioplayer_0.set_play_mode(0)
    play_state = 0


def loop():
    global title0, label0, label1, label2, audioplayer_0, play_state
    M5.update()
    play_state = audioplayer_0.check_play_status()
    if play_state:
        label1.setText(str("Play Status: Playing"))
    else:
        label1.setText(str("Play Status: Paused"))
    label2.setText(str((str("Audio Num: ") + str((audioplayer_0.get_current_audio_number())))))
    time.sleep_ms(100)


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
