# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import DMX512Unit


Title = None
label0 = None
label1 = None
dmx_0 = None


dmx_data = None
dmx_data2 = None


def dmx_0_channel1_receive_event(received_data):
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2
    dmx_data = received_data
    label0.setText(str((str("Channel 1:") + str(dmx_data))))


def dmx_0_channel2_receive_event(received_data):
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2
    dmx_data2 = received_data
    label1.setText(str((str("Channel 2:") + str(dmx_data2))))


def setup():
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title("DMX512Unit Rec example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Channel 1:", 0, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Channel 2:", 2, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    dmx_0 = DMX512Unit(1, port=(13, 14), mode=2)
    dmx_0.attach_channel(1, dmx_0_channel1_receive_event)
    dmx_0.attach_channel(2, dmx_0_channel2_receive_event)
    dmx_0.receive_none_block()


def loop():
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2
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
