# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR


label_title = None
label_addr = None
label_data = None
label_tip = None
ir = None
data = None
addr = None


def btna_click_event_cb(state):
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    data = (data if isinstance(data, (int, float)) else 0) + 1
    ir.tx(addr, data)
    print((str("IR: Send addr: ") + str((str(addr) + str((str(" data: ") + str(data)))))))
    label_data.setText(str((str("data: ") + str(data))))


def setup():
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("IR", 58, 5, 1.0, 0x1AEAEB, 0x000000, Widgets.FONTS.DejaVu18)
    label_addr = Widgets.Label("addr:", 5, 45, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data:", 5, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "BtnA Send", 18, 200, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    ir = IR()
    addr = 56
    data = 0
    Power.setExtOutput(True)
    label_addr.setText(str((str("addr: ") + str(addr))))


def loop():
    global label_title, label_addr, label_data, label_tip, ir, data, addr
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
