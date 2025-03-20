# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import PWR485
from unit import ISO485Unit


label0 = None
pwr485_0 = None
iso485_0 = None


def btnA_wasClicked_event(state):  # noqa: N802
    global label0, pwr485_0, iso485_0
    pwr485_0.write("A")


def btnB_wasClicked_event(state):  # noqa: N802
    global label0, pwr485_0, iso485_0
    pwr485_0.write("B")


def btnC_wasClicked_event(state):  # noqa: N802
    global label0, pwr485_0, iso485_0
    pwr485_0.write("C")


def setup():
    global label0, pwr485_0, iso485_0

    M5.begin()
    label0 = Widgets.Label("label0", 69, 61, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnC_wasClicked_event)

    pwr485_0 = PWR485(
        2,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=0,
        rx=39,
        rts=46,
        mode=PWR485.MODE_RS485_HALF_DUPLEX,
    )
    iso485_0 = ISO485Unit(
        1,
        port=(4, 5),
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
    global label0, pwr485_0, iso485_0
    M5.update()
    if iso485_0.any():
        label0.setText(str(iso485_0.read()))


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
