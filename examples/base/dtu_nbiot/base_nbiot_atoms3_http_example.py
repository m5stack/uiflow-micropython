# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import UART
from base import AtomDTUNBIoT


title0 = None
label0 = None
label1 = None
uart2 = None
base_nbiot = None


def setup():
    global title0, label0, label1, uart2, base_nbiot

    M5.begin()
    title0 = Widgets.Title("NBIoT HTTP", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Press to", 23, 43, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Request", 23, 74, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=6)
    base_nbiot = AtomDTUNBIoT(uart2)


def loop():
    global title0, label0, label1, uart2, base_nbiot
    M5.update()
    if BtnA.wasPressed():
        base_nbiot.http_request(
            1,
            "http://httpbin.org/post",
            {"Content-Type": "application/json", "Custom-Header": "MyHeaderValue"},
            {"message": "Hello from M5Stack!", "status": "active"},
        )
        print(base_nbiot.data_content)
        print(base_nbiot.response_code)


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
