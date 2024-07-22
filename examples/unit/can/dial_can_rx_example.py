# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import MiniCANUnit


label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
minican_0 = None


frame = None


def setup():
    global label0, label1, label2, label3, label4, label5, label6, label7, label8, minican_0, frame

    M5.begin()
    label0 = Widgets.Label("Slaver", 90, 13, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ID:", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Ext:", 25, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("RTR:", 20, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Msg:", 18, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 72, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 72, 89, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 72, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 72, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    minican_0 = MiniCANUnit((1, 2), MiniCANUnit.NORMAL, baudrate=25000)


def loop():
    global label0, label1, label2, label3, label4, label5, label6, label7, label8, minican_0, frame
    M5.update()
    if minican_0.any(0):
        frame = minican_0.recv(0, timeout=5000)
        label5.setText(str(frame[0]))
        label6.setText(str(frame[4]))
        label7.setText(str(frame[2]))
        label8.setText(str(frame[1]))


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
