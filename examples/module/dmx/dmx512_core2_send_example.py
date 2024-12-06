# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import DMX512Module
import time


Title = None
label1 = None
label0 = None
module_dmx_0 = None


ch_data = None


def setup():
    global Title, label1, label0, module_dmx_0, ch_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title(
        "DMX512Module Send example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label("Not Sent", 2, 129, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Not initialized", 2, 76, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    module_dmx_0 = DMX512Module(2, mode=1)
    ch_data = 0
    label0.setText(str("Initialized"))


def loop():
    global Title, label1, label0, module_dmx_0, ch_data
    M5.update()
    label1.setText(str("Not Sent"))
    ch_data = ch_data + 1
    if ch_data >= 255:
        ch_data = 0
    module_dmx_0.write_data(1, ch_data)
    module_dmx_0.write_data(2, ch_data)
    module_dmx_0.write_data(3, ch_data)
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
