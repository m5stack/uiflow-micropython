# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import Relay2Unit


title0 = None
label2 = None
label0 = None
label3 = None
label1 = None
relay2_0 = None


def setup():
    global title0, label2, label0, label3, label1, relay2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Relay2Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Relay1", 38, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 2, 91, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Relay2", 220, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 2, 136, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    relay2_0 = Relay2Unit((33, 32))


def loop():
    global title0, label2, label0, label3, label1, relay2_0
    M5.update()
    label0.setText(str((str("Relay1 State:") + str((relay2_0.get_relay_status(1))))))
    label1.setText(str((str("Relay2 State:") + str((relay2_0.get_relay_status(2))))))
    if BtnA.wasPressed():
        relay2_0.set_relay_cntrl(1, not (relay2_0.get_relay_status(1)))
    elif BtnC.wasPressed():
        relay2_0.set_relay_cntrl(2, not (relay2_0.get_relay_status(2)))


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
