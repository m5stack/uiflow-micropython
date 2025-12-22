# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network
from stamplc import PoEStamPLC
import time
import requests2


title0 = None
label0 = None
label1 = None
label2 = None
wlan_sta = None
stamplc_poe_0 = None
http_req = None


def setup():
    global title0, label0, label1, label2, wlan_sta, stamplc_poe_0, http_req

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("StamPLC PoE Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("IP:", 2, 33, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Status Code:", 2, 65, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text:", 2, 96, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(False)
    stamplc_poe_0 = PoEStamPLC()
    stamplc_poe_0.ifconfig(("192.168.8.198", "255.255.255.0", "192.168.8.1", "8.8.8.8"))
    while not (stamplc_poe_0.isconnected()):
        time.sleep(1)
        print(".")
    label0.setText(str((str("IP:") + str((stamplc_poe_0.ifconfig()[0])))))
    print("local network is connected")
    print((str("IP:") + str((stamplc_poe_0.ifconfig()[0]))))


def loop():
    global title0, label0, label1, label2, wlan_sta, stamplc_poe_0, http_req
    M5.update()
    if BtnA.wasPressed():
        print("Btn Pressed")
        label0.setText(str((str("IP:") + str((stamplc_poe_0.ifconfig()[0])))))
        label1.setText(str("Status Code:"))
        label2.setText(str("Text:"))
        http_req = requests2.get(
            "https://wttr.in/?format=%22%C,%20%t%22", headers={"Content-Type": "application/json"}
        )
        print((str("Status Code:") + str((http_req.status_code))))
        print((str("Text:") + str((http_req.text))))
        label1.setText(str((str("Status Code:") + str((http_req.status_code)))))
        label2.setText(str((str("Text:") + str((http_req.text)))))


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
