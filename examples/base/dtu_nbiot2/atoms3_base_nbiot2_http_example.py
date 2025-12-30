# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import UART
from base import AtomRS485
from base import AtomDTUNBIoT2


label0 = None
uart2 = None
base_rs485 = None
base_nbiot2 = None
base_nbiot2_http_req = None


def setup():
    global label0, uart2, base_rs485, base_nbiot2, base_nbiot2_http_req

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("label0", 8, 7, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=6)
    base_rs485 = AtomRS485(
        1,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=7,
        rx=8,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )
    base_nbiot2 = AtomDTUNBIoT2(uart2, verbose=False)
    base_nbiot2.connect(apn="cmnbiot")
    while not (base_nbiot2.isconnected()):
        pass
    base_nbiot2_http_req = base_nbiot2.post(
        "http://httpbin.org/post",
        json={"message": "Hello from M5Stack!", "status": "active"},
        headers={
            "Content-Type": "application/json",
            "Custom-Header": "MyHeaderValue",
        },
    )
    print((str("status code: ") + str((base_nbiot2_http_req.status_code))))
    print((str("content: ") + str((base_nbiot2_http_req.content))))


def loop():
    global label0, uart2, base_rs485, base_nbiot2, base_nbiot2_http_req
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
