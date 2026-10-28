# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWANModule_RUI3
import time


title0 = None
label0 = None
module_lorawaneu868_0 = None


def setup():
    global title0, label0, module_lorawaneu868_0

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoraWAN868 P2P Send", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label(
        "Press BtnA to Send", 1, 105, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18
    )

    module_lorawaneu868_0 = LoRaWANModule_RUI3(2, tx=17, rx=16, rst=13)
    module_lorawaneu868_0.set_network_mode(0)
    module_lorawaneu868_0.set_p2p_frequency(868000000)
    module_lorawaneu868_0.set_p2p_spreading_factor(8)
    module_lorawaneu868_0.set_p2p_bandwidth(0)
    module_lorawaneu868_0.set_p2p_tx_power(22)
    module_lorawaneu868_0.set_p2p_code_rate(0)
    module_lorawaneu868_0.set_p2p_preamble_length(8)


def loop():
    global title0, label0, module_lorawaneu868_0
    M5.update()
    label0.setText(str("Press BtnA to Send"))
    if BtnA.wasPressed():
        module_lorawaneu868_0.send_p2p_data("abcdef", timeout=0, to_hex=False)
        label0.setText(str("Sent"))
        time.sleep(1)


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
