# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWAN868Module


lorawan868_0 = None


def setup():
    global lorawan868_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    lorawan868_0 = LoRaWAN868Module(1, (17, 16))
    lorawan868_0.wake_up()
    lorawan868_0.set_parameters(0, 0, 5, 0, 1, 8, 0, 0, 0)
    lorawan868_0.set_auto_low_power(False)
    print(lorawan868_0.query_chip_id())
    print(lorawan868_0.query_lorawan_mode())
    print(lorawan868_0.any())
    lorawan868_0.set_mode(LoRaWAN868Module.MODE_LORA)
    lorawan868_0.enable_rx(0)


def loop():
    global lorawan868_0
    M5.update()
    if lorawan868_0.any():
        print(lorawan868_0.receive_data())
        lorawan868_0.enable_rx(0)


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
