# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LoRaWANUnit_RUI3
import time


title0 = None
label0 = None
lorawancn470_0 = None


def setup():
    global title0, label0, lorawancn470_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoRaWAN P2P Send CoreS3 e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "P2P Message Send State:", 3, 115, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    lorawancn470_0 = LoRaWANUnit_RUI3(2, port=(1, 2))
    lorawancn470_0.set_network_mode(0)
    lorawancn470_0.set_p2p_frequency(470000000)
    lorawancn470_0.set_p2p_spreading_factor(7)
    lorawancn470_0.set_p2p_bandwidth(0)
    lorawancn470_0.set_p2p_tx_power(14)
    lorawancn470_0.set_p2p_code_rate(0)
    lorawancn470_0.set_p2p_preamble_length(8)
    lorawancn470_0.set_p2p_sync_word(0xFFFF)


def loop():
    global title0, label0, lorawancn470_0
    M5.update()
    label0.setText(
        str(
            (
                str("P2P Message Send State:")
                + str((lorawancn470_0.send_p2p_data("1122", timeout=3000)))
            )
        )
    )
    time.sleep(3.5)


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
