# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from base import AtomDTULoRaWANRUI3Base


rgb = None
base_lorawaneu868 = None


def setup():
    global rgb, base_lorawaneu868

    M5.begin()
    rgb = RGB()
    base_lorawaneu868 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))
    base_lorawaneu868.set_network_mode(0)
    base_lorawaneu868.set_p2p_frequency(600000000)
    base_lorawaneu868.set_p2p_spreading_factor(7)
    base_lorawaneu868.set_p2p_bandwidth(0)
    base_lorawaneu868.set_p2p_tx_power(14)
    base_lorawaneu868.set_p2p_code_rate(0)
    base_lorawaneu868.set_p2p_preamble_length(8)
    print("Press the button to send P2P message")


def loop():
    global rgb, base_lorawaneu868
    M5.update()
    if BtnA.wasPressed():
        base_lorawaneu868.send_p2p_data("AABBCC", timeout=0, to_hex=False)


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
