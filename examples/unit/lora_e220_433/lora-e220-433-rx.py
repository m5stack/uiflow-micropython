# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LoRaE220433Unit


lorae220433_0 = None


lorae220433_str_data = None
lorae220433_rssi = None


def lorae220433_0_receive_event(received_data, rssi):
    global lorae220433_0, lorae220433_str_data, lorae220433_rssi
    lorae220433_rssi = rssi
    try:
        lorae220433_str_data = received_data.decode()
    except:
        lorae220433_str_data = str(received_data)
    print(lorae220433_str_data)
    print(lorae220433_rssi)


def setup():
    global lorae220433_0, lorae220433_str_data, lorae220433_rssi

    M5.begin()
    Widgets.fillScreen(0x222222)

    lorae220433_0 = LoRaE220433Unit(1, port=(18, 17))
    lorae220433_0.receive_none_block(lorae220433_0_receive_event)


def loop():
    global lorae220433_0, lorae220433_str_data, lorae220433_rssi
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
