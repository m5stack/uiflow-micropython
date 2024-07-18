# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
from unit import QRCodeUnit
from hardware import *


label0 = None
i2c0 = None
qrcode_0 = None


qrdata = None


def qrcode_0_event(_qrdata):
    global label0, i2c0, qrcode_0, qrdata
    qrdata = _qrdata
    print(qrdata)


def setup():
    global label0, i2c0, qrcode_0, qrdata

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 16, 20, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    qrcode_0 = QRCodeUnit(0, i2c0, 0x21)
    qrcode_0.set_event_cb(qrcode_0_event)
    qrcode_0.set_trigger_mode(1)


def loop():
    global label0, i2c0, qrcode_0, qrdata
    M5.update()
    qrcode_0.event_poll_loop()


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
