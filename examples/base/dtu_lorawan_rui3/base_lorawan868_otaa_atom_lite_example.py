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
    base_lorawaneu868.set_network_mode(1)
    base_lorawaneu868.set_otaa_config(
        "70B3D57ED007006A", "A843ECB026197C981D67AEFACC72D01E", "70B3D57ED0063472"
    )
    base_lorawaneu868.set_rx_delay_on_window1(1)
    base_lorawaneu868.set_rx_delay_on_window2(2)
    base_lorawaneu868.set_rx_data_rate_on_windows2(0)
    base_lorawaneu868.set_lorawan_node_class("C")
    if base_lorawaneu868.join_network(10000):
        print("Success join the network")
        rgb.fill_color(0x33FF33)
        base_lorawaneu868.send_data(1, "AABBCC", 0)
    else:
        print("Failed Join to the network")
        rgb.fill_color(0xFF0000)


def loop():
    global rgb, base_lorawaneu868
    M5.update()
    if BtnA.wasPressed():
        if (base_lorawaneu868.get_received_data_count()) != 0:
            print(base_lorawaneu868.get_received_data_string())
        else:
            print("Message queue is empty")


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
