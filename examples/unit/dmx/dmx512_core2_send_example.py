# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import DMX512Unit
import time


Title = None
label1 = None
label0 = None
dmx_0 = None


ch_data = None


def setup():
    global Title, label1, label0, dmx_0, ch_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title("DMX512Unit Send example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Not Sent", 2, 129, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Not initialized", 2, 76, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    dmx_0 = DMX512Unit(1, port=(13, 14), mode=1)
    label0.setText(str("Initialized"))
    ch_data = 0


def loop():
    global Title, label1, label0, dmx_0, ch_data
    M5.update()
    label1.setText(str("Not Sent"))
    dmx_0.write_data(1, ch_data)
    dmx_0.write_data(2, ch_data)
    dmx_0.write_data(3, ch_data)
    ch_data = (ch_data if isinstance(ch_data, (int, float)) else 0) + 1
    if ch_data >= 255:
        ch_data = 0
    label1.setText(str("Sent"))
    time.sleep(0.7)


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
