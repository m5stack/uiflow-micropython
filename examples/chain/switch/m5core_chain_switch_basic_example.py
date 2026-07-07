# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import SwitchChain
from chain import ChainBus


title0 = None
label_adc = None
label_state = None
bus2 = None
chain_switch_0 = None


def chain_switch_0_open_event(args):
    global title0, label_adc, label_state, bus2, chain_switch_0
    label_state.setText(str("State: Open"))


def chain_switch_0_close_event(args):
    global title0, label_adc, label_state, bus2, chain_switch_0
    label_state.setText(str("State: Close"))


def setup():
    global title0, label_adc, label_state, bus2, chain_switch_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Chain Switch Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_adc = Widgets.Label("ADC: --", 20, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24)
    label_state = Widgets.Label(
        "State: --", 20, 113, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_switch_0 = SwitchChain(bus2, 1)
    chain_switch_0.set_trigger_callback(SwitchChain.STATUS_OPEN, chain_switch_0_open_event)
    chain_switch_0.set_trigger_callback(SwitchChain.STATUS_CLOSE, chain_switch_0_close_event)
    chain_switch_0.set_trigger(True)
    if chain_switch_0.get_switch_status():
        label_state.setText(str("State: Open"))
    else:
        label_state.setText(str("State: Close"))


def loop():
    global title0, label_adc, label_state, bus2, chain_switch_0
    M5.update()
    label_adc.setText(str((str("ADC: ") + str((chain_switch_0.get_adc12())))))


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
