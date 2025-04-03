# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCode2Base


title0 = None
label_data = None
label_status = None
base_qrcode2 = None
is_scanning = None
status = None
data = None


def setup():
    global title0, label_data, label_status, base_qrcode2, is_scanning, status, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_KEY)
    is_scanning = False
    status = is_scanning


def loop():
    global title0, label_data, label_status, base_qrcode2, is_scanning, status, data
    M5.update()
    if BtnA.isPressed():
        base_qrcode2.set_trig(0)
        is_scanning = True
    else:
        base_qrcode2.set_trig(1)
        is_scanning = False
    if status != is_scanning:
        status = is_scanning
        if status:
            label_status.setColor(0x00FF00, 0x000000)
            label_status.setText(str("scanning"))
        else:
            label_status.setColor(0xFFFFFF, 0x000000)
            label_status.setText(str("stop scan"))
    data = base_qrcode2.read()
    if data:
        label_data.setText(str(data.decode()))


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
