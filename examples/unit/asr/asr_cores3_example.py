# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ASRUnit


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
asr_0 = None


def asr_0_hello_event(args):
    global title0, label0, label1, label2, label3, asr_0
    print("Rec Hello")


def setup():
    global title0, label0, label1, label2, label3, asr_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "UnitASR M5CoreSe Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("msg:", 0, 51, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("rec cmd num:", 0, 93, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label(
        "rec cmd word:", 0, 134, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label(
        "rec cmd handler state:", 0, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    asr_0 = ASRUnit(2, port=(1, 2))
    print(asr_0.search_command_num("hello"))
    print(asr_0.search_command_word(0x32))
    asr_0.add_command_word(0x32, "hello", asr_0_hello_event)


def loop():
    global title0, label0, label1, label2, label3, asr_0
    M5.update()
    if asr_0.get_received_status():
        label0.setText(str((str("msg:") + str((asr_0.get_current_raw_message())))))
        label1.setText(str((str("rec cmd num:") + str((asr_0.get_current_command_num())))))
        label2.setText(str((str("rec cmd word:") + str((asr_0.get_current_command_word())))))
        label3.setText(str((str("rec cmd handler state:") + str((asr_0.get_command_handler())))))


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
