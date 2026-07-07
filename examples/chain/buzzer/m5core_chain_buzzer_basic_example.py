# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import BuzzerChain
from chain import ChainBus


title0 = None
label_freq = None
label_tip = None
bus2 = None
chain_buzzer_0 = None


def btna_was_clicked_event(state):
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    label_freq.setText(str("Freq: 500 Hz"))
    chain_buzzer_0.tone(500, 50, 100)


def btnb_was_clicked_event(state):
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    label_freq.setText(str("Freq: 1000 Hz"))
    chain_buzzer_0.tone(1000, 50, 100)


def btnc_was_clicked_event(state):
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    label_freq.setText(str("Freq: 1500 Hz"))
    chain_buzzer_0.tone(1500, 50, 100)


def setup():
    global title0, label_freq, label_tip, bus2, chain_buzzer_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title(
        "Chain Buzzer Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label_freq = Widgets.Label(
        "Freq: -- Hz", 107, 90, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_tip = Widgets.Label(
        "Press button tone", 78, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_buzzer_0 = BuzzerChain(bus2, 1)
    chain_buzzer_0.tone(2700, 50, 100)
    chain_buzzer_0.set_rgb_color(0x33FFFF)
    chain_buzzer_0.set_rgb_brightness(100, save=False)
    chain_buzzer_0.set_mode(BuzzerChain.MODE_AUTO_PLAY)


def loop():
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
