# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import MicChain
import time
from chain import ChainBus


title0 = None
label_adc = None
label_status = None
bus2 = None
chain_mic_0 = None
last_trigger_time = None


def chain_mic_0_low_to_high_event(args):
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time
    last_trigger_time = time.ticks_ms()
    label_status.setVisible(True)


def chain_mic_0_high_to_low_event(args):
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time
    last_trigger_time = time.ticks_ms()
    label_status.setVisible(True)


def setup():
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Chain MIC Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_adc = Widgets.Label("ADC: --", 95, 76, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "voice trigger", 82, 158, 1.0, 0x4CEB18, 0x000000, Widgets.FONTS.DejaVu24
    )
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_mic_0 = MicChain(bus2, 1)
    chain_mic_0.set_trigger_callback(MicChain.TRIGGER_LOW_TO_HIGH, chain_mic_0_low_to_high_event)
    chain_mic_0.set_trigger_callback(MicChain.TRIGGER_HIGH_TO_LOW, chain_mic_0_high_to_low_event)
    chain_mic_0.set_trigger(True)
    chain_mic_0.set_rgb_color(0x000064)
    label_status.setVisible(False)


def loop():
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time
    M5.update()
    label_adc.setText(str((str("ADC: ") + str((chain_mic_0.get_adc12())))))
    time.sleep_ms(100)
    if (time.ticks_diff((time.ticks_ms()), last_trigger_time)) > 3000:
        label_status.setVisible(False)


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
