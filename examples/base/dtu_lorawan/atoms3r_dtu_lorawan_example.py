# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomDTULoRaWANBase


title0 = None
base_lorawan470 = None


def setup():
    global title0, base_lorawan470

    M5.begin()
    title0 = Widgets.Title("LoRaWAN", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    base_lorawan470 = AtomDTULoRaWANBase(2, port=(5, 6))
    base_lorawan470.set_join_mode(0)
    base_lorawan470.config_otaa("xxxx", "xxxx", "xxxx")
    base_lorawan470.set_frequency_band_mask("0400")
    base_lorawan470.set_rx_window_param(0, 0, 505300000)
    base_lorawan470.set_class_mode(2)
    base_lorawan470.set_uplink_downlink_mode(1)
    base_lorawan470.set_uplink_app_port(1)
    base_lorawan470.join(1, 1, 20, 20)
    print("LoRaWAN configuration complete")


def loop():
    global title0, base_lorawan470
    M5.update()
    if BtnA.isPressed():
        print("Send Message")
        base_lorawan470.send_data("11", 1, 15)


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
