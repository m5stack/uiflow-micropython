# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import DLightChain
import time


label_title = None
label_lux = None
bus2 = None
chain_dlight_0 = None
reading = None


def setup():
    global label_title, label_lux, bus2, chain_dlight_0, reading

    M5.begin()
    Widgets.setRotation(1)
    label_title = Widgets.Label(
        "Chain DLight", 83, 12, 1.0, 0x33CCFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_lux = Widgets.Label(
        "-- Lux", 96, 100, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat40
    )

    label_title.setCursor(
        x=(int((320 - (M5.Display.textWidth("Chain DLight", Widgets.FONTS.Montserrat24))) / 2)),
        y=12,
    )
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_dlight_0 = DLightChain(bus2, 1)


def loop():
    global label_title, label_lux, bus2, chain_dlight_0, reading
    M5.update()
    reading = str((chain_dlight_0.read_lux())) + str(" Lux")
    label_lux.setText(str(""))
    label_lux.setCursor(
        x=(int((320 - (M5.Display.textWidth(reading, Widgets.FONTS.Montserrat40))) / 2)),
        y=(int((240 - (M5.Display.fontHeight(Widgets.FONTS.Montserrat40))) / 2)),
    )
    label_lux.setText(str(reading))
    time.sleep_ms(250)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
