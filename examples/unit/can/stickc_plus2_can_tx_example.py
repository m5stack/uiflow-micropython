# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CANUnit
from hardware import *


label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
can_0 = None


import random

id2 = None
payload = None


def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        can_0, \
        id2, \
        payload

    M5.begin()
    label0 = Widgets.Label("Master", 35, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ID:", 4, 39, 1.0, 0xF5A41D, 0x080808, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("RTR:", 4, 90, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Ext:", 4, 141, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Msg:", 3, 192, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 3, 64, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 4, 115, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 4, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 4, 217, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    can_0 = CANUnit((33, 32), CANUnit.NORMAL, baudrate=25000)
    id2 = 123
    payload = "uiflow2"
    label5.setText(str(id2))
    label6.setText(str(False))
    label7.setText(str(False))
    label0.setText(str(payload))


def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        can_0, \
        id2, \
        payload
    M5.update()
    can_0.send(payload, id2, timeout=0, rtr=False, extframe=False)
    if BtnA.wasClicked():
        id2 = random.randint(1, 100)
        label5.setText(str(id2))
        payload = str((random.randint(32, 126)))
        label8.setText(str(payload))


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
