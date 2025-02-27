# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import PwrCANModule
from module import PwrCANModuleRS485
from unit import RS485Unit
import time


title0 = None
label3 = None
label0 = None
label1 = None
label2 = None
pwrcan_0 = None
pwrcan_1 = None
rs485_0 = None


def setup():
    global title0, label3, label0, label1, label2, pwrcan_0, pwrcan_1, rs485_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "PwrCANModule CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label("CAN Rec:", 0, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "CAN Message State: ", 0, 49, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "RS485 Message State: ", 0, 138, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("RS485 Rec:", 0, 179, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pwrcan_0 = PwrCANModule(0, 17, 18, PwrCANModule.NORMAL, baudrate=1000000)
    pwrcan_1 = PwrCANModuleRS485(1, baudrate=115200, bits=8, parity=None, stop=1, tx=13, rx=7)
    rs485_0 = RS485Unit(
        2,
        port=(1, 2),
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )


def loop():
    global title0, label3, label0, label1, label2, pwrcan_0, pwrcan_1, rs485_0
    M5.update()
    if M5.Touch.getCount():
        pwrcan_0.send("uiflow2", 0, timeout=0, rtr=False, extframe=False)
        label0.setText(str("CAN Message State: Send"))
        pwrcan_1.write("RS485_uiflow2" + "\r\n")
        label1.setText(str("RS485 Message State: Send"))
        time.sleep(1)
    else:
        label0.setText(str("CAN Message State: Not Send"))
        label1.setText(str("RS485 Message State: Not Send"))
    if pwrcan_0.any(0):
        label3.setText(str((str("CAN Rec:") + str((pwrcan_0.recv(0, timeout=5000))))))
    if rs485_0.any():
        label2.setText(str((str("RS485 Rec:") + str((rs485_0.read())))))


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
