# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ZigbeeUnit
import time


label0 = None
zigbee_0 = None


def setup():
    global label0, zigbee_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 67, 43, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    zigbee_0 = ZigbeeUnit(1, port=(18, 17), verbose=True)
    zigbee_0.set_module_param(
        ZigbeeUnit.DEVICE_TYPE_COORDINATOR,
        0x1620,
        11,
        ZigbeeUnit.TRANSFER_MODE_PASS_THROUGH,
        0x6677,
    )
    label0.setText(str("start"))


def loop():
    global label0, zigbee_0
    M5.update()
    zigbee_0.p2p_transmission(0x0066, "p2p")
    time.sleep(3)
    zigbee_0.broadcast("broadcast")
    time.sleep(3)


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
