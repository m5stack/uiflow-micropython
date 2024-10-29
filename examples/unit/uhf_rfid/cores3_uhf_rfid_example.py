# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import UHFRFIDUnit


nbiot2_0 = None
uhfrfid_0 = None


epc = None


def setup():
    global nbiot2_0, uhfrfid_0, epc

    M5.begin()
    Widgets.fillScreen(0x222222)

    uhfrfid_0 = UHFRFIDUnit(2, port=(18, 17))
    epc = uhfrfid_0.inventory()
    print(epc)
    uhfrfid_0.select(UHFRFIDUnit.S0, 0b000, UHFRFIDUnit.RFU, 0x20, False, epc)
    uhfrfid_0.write_mem_bank(UHFRFIDUnit.RFU, 0x00, "12345678", "00000000")
    print(uhfrfid_0.read_mem_bank(UHFRFIDUnit.RFU, 0x00, 4, "00000000"))


def loop():
    global nbiot2_0, uhfrfid_0, epc
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
