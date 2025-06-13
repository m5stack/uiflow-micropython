# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network
from module import LANModule
import time
import requests2


label_status = None
title0 = None
label_info = None
wlan = None
lan_0 = None
http_req = None


def setup():
    global label_status, title0, label_info, wlan, lan_0, http_req
    M5.begin()
    Widgets.fillScreen(0x222222)
    label_status = Widgets.Label(
        "Waiting for network connection", 5, 50, 1.0, 0xFF0000, 0x222222, Widgets.FONTS.DejaVu18
    )
    title0 = Widgets.Title("LANModule Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_info = Widgets.Label("Get info", 5, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    lan_0 = LANModule(cs=1, rst=0, int=10)
    lan_0.active(True)
    while not (lan_0.isconnected()):
        time.sleep(1)
        print(".")
    print("local network is connected")
    label_status.setText(str("Network connected!"))
    label_status.setColor(0x00FF00, 0x222222)
    http_req = requests2.get(
        "https://wttr.in/?format=%22%C,%20%t%22", headers={"Content-Type": "application/json"}
    )
    print(http_req.text)
    label_info.setText(str(http_req.text))


def loop():
    global label_status, title0, label_info, wlan, lan_0, http_req
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            lan_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
