# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import QRCodeModule


title0 = None
label_status = None
label_data = None
module_qrcode_0 = None
is_scanning = None
data = None


def btn_pwr_was_clicked_event(state):
    global title0, label_status, label_data, module_qrcode_0, is_scanning, data
    if is_scanning:
        module_qrcode_0.stop_decode()
        label_status.setColor(0xFFFFFF, 0x222222)
        label_status.setText(str("stop scan"))
    else:
        module_qrcode_0.start_decode()
        label_status.setColor(0x00FF00, 0x222222)
        label_status.setText(str("scanning"))
    is_scanning = not is_scanning


def setup():
    global title0, label_status, label_data, module_qrcode_0, is_scanning, data
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "stop scan", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_data = Widgets.Label("data", 4, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)
    module_qrcode_0 = QRCodeModule(1, tx=17, rx=18)
    module_qrcode_0.set_trigger_mode(QRCodeModule.TRIGGER_MODE_CONTINUOUS)
    module_qrcode_0.stop_decode()
    is_scanning = False


def loop():
    global title0, label_status, label_data, module_qrcode_0, is_scanning, data
    M5.update()
    data = module_qrcode_0.read()
    if data:
        label_data.setText(str(data.decode()))
        print(data.decode())


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
