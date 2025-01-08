# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LoRaWANUnit_RUI3
import time


title0 = None
label2 = None
label0 = None
label1 = None
lorawancn470_0 = None


def setup():
    global title0, label2, label0, label1, lorawancn470_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoRaWAN OTAA CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label(
        "LoRa Message Rec:", 1, 172, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "LoRa Network Join status:", 1, 68, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "LoRa Message Send status:", 1, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    lorawancn470_0 = LoRaWANUnit_RUI3(2, port=(1, 2))
    lorawancn470_0.set_network_mode(1)
    lorawancn470_0.set_otaa_config("xxxxx", "xxxxx", "xxxxx")
    lorawancn470_0.set_channel_mask("0400")
    lorawancn470_0.set_rx_delay_on_window1(1)
    lorawancn470_0.set_rx_delay_on_window2(2)
    lorawancn470_0.set_rx_data_rate_on_windows2(0)
    lorawancn470_0.set_lorawan_node_class("C")
    lorawancn470_0.join_network(0)


def loop():
    global title0, label2, label0, label1, lorawancn470_0
    M5.update()
    label0.setText(
        str((str("LoRa Network Join status:") + str((lorawancn470_0.get_join_state()))))
    )
    if lorawancn470_0.get_join_state():
        label1.setText(
            str(
                (
                    str("LoRa Message Send status:")
                    + str((lorawancn470_0.send_data(1, "aabbcc", 6000)))
                )
            )
        )
        label2.setText(str((str("LoRa Message Rec:") + str((lorawancn470_0.get_last_receive())))))
    time.sleep(6)


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
