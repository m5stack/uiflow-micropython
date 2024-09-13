# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network


title0 = None
label0 = None
label1 = None
label2 = None
wlan = None


ap_client = None


def setup():
    global title0, label0, label1, label2, wlan

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("WLAN AP CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 2, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 2, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 2, 145, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan = network.WLAN(network.AP_IF)
    wlan.config(max_clients=4)
    wlan.config(essid="M5CoreS3AP")
    wlan.active(True)


# Please connect to the AP named M5CoreS3.
def loop():
    global title0, label0, label1, label2, wlan
    M5.update()
    label0.setText(str((str("AP is connected?:") + str((wlan.isconnected())))))
    label1.setText(str((str("SSID:") + str((wlan.config("essid"))))))
    for ap_client in wlan.status("stations"):
        label2.setText(str(ap_client[0]))


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
