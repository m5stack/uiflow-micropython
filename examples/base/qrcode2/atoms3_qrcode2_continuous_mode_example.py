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
data = None


def btna_was_clicked_event(state):
    global title0, label_data, label_status, base_qrcode2, is_scanning, data
    if is_scanning:
        base_qrcode2.stop_decode()
        label_status.setText(str("stop scan"))
        label_status.setColor(0xFFFFFF, 0x000000)
    else:
        base_qrcode2.start_decode()
        label_status.setText(str("scanning"))
        label_status.setColor(0x00FF00, 0x000000)
    is_scanning = not is_scanning


def setup():
    global title0, label_data, label_status, base_qrcode2, is_scanning, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_CONTINUOUS)
    base_qrcode2.set_startup_tone(1)
    base_qrcode2.set_decode_success_beep(2)
    base_qrcode2.stop_decode()
    is_scanning = False


def loop():
    global title0, label_data, label_status, base_qrcode2, is_scanning, data
    M5.update()
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
