# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCodeBase


title0 = None
label_data = None
label_status = None
base_qrcode = None
data = None


def setup():
    global title0, label_data, label_status, base_qrcode, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "detecting", 5, 25, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode = AtomicQRCodeBase(2, 5, 6, 7, 8)
    base_qrcode.set_trigger_mode(base_qrcode.TRIGGER_MODE_MOTION_SENSING)


def loop():
    global title0, label_data, label_status, base_qrcode, data
    M5.update()
    data = base_qrcode.read()
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
