# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWANModule_RUI3


title0 = None
label0 = None
module_lorawaneu868_0 = None


def setup():
    global title0, label0, module_lorawaneu868_0

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoraWAN868 P2P Receive", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label(
        "Touch to Receive", 2, 37, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18
    )

    M5.Lcd.setTextScroll(True)
    M5.Lcd.setTextColor(0xFFFFFF, 0x330000)
    module_lorawaneu868_0 = LoRaWANModule_RUI3(2, tx=17, rx=18, rst=7)
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
    if M5.Touch.getCount():
        M5.Lcd.printf(
            (str((str((module_lorawaneu868_0.get_p2p_receive_data(5000, False))))) + str("\n"))
        )


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
