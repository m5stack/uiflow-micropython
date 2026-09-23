# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from chain import PedalChain
from chain import ChainBus


page0 = None
bus1 = None
chain_pedal_0 = None


def chain_pedal_0_status_open_event(args):
    global page0, bus1, chain_pedal_0
    print("switch open")


def chain_pedal_0_status_close_event(args):
    global page0, bus1, chain_pedal_0
    print("switch close")


def setup():
    global page0, bus1, chain_pedal_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)

    bus1 = ChainBus(1, tx=14, rx=13)
    chain_pedal_0 = PedalChain(bus1, 1)
    chain_pedal_0.set_trigger_callback(PedalChain.STATUS_OPEN, chain_pedal_0_status_open_event)
    chain_pedal_0.set_trigger_callback(PedalChain.STATUS_CLOSE, chain_pedal_0_status_close_event)
    print(chain_pedal_0.set_work_mode(PedalChain.WORK_MODE_SWITCH, save=False))
    chain_pedal_0.fill_rgb_color(0x6600CC)
    chain_pedal_0.set_rgb_overlay(0x0F, save=False)


def loop():
    global page0, bus1, chain_pedal_0
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus1.deinit()
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
