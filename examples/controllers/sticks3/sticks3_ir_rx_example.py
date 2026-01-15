# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR


label_title = None
label0 = None
label_addr = None
label_data = None
ir = None


data = None
addr = None


def ir_rx_event(_data, _addr, _ctrl):
    global label_title, label0, label_addr, label_data, ir, data, addr
    data = _data
    addr = _addr
    label_addr.setText(str((str("addr: ") + str(addr))))
    label_data.setText(str((str("data: ") + str(data))))


def setup():
    global label_title, label0, label_addr, label_data, ir, data, addr

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("IR RX", 41, 5, 1.0, 0x0FBAE1, 0x000000, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("NEC Decode", 8, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_addr = Widgets.Label("addr:", 5, 115, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data:", 5, 145, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    Speaker.setPA(False)
    ir = IR()
    ir.rx_cb(ir_rx_event)


def loop():
    global label_title, label0, label_addr, label_data, ir, data, addr
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
