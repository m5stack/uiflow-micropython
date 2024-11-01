# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import UWBUnit


label0 = None
label1 = None
uwb_0 = None


anchor_id = None


def btnA_wasClicked_event(state):  # noqa: N802
    global label0, label1, uwb_0, anchor_id
    anchor_id = (anchor_id + 1) % 4
    uwb_0.set_device_mode(UWBUnit.ANCHOR, anchor_id)
    label1.setText(str(uwb_0.get_device_id()))


def setup():
    global label0, label1, uwb_0, anchor_id

    M5.begin()
    label0 = Widgets.Label("label0", 29, 36, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label1 = Widgets.Label("0", 44, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu72)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    anchor_id = 0
    uwb_0 = UWBUnit(2, port=(33, 32), device_mode=UWBUnit.ANCHOR, device_id=0, verbose=False)
    print(uwb_0.isconnected())
    print(uwb_0.get_version())
    if (uwb_0.get_device_mode()) == 1:
        label0.setText(str("Anchor"))
    else:
        label0.setText(str("Tag"))
    label1.setText(str(uwb_0.get_device_id()))


def loop():
    global label0, label1, uwb_0, anchor_id
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
