# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import machine
import network
import requests2
import time


ethernet_0 = None
http_req = None


def setup():
    global ethernet_0, http_req

    M5.begin()
    ethernet_0 = network.LAN(
        0,
        phy_addr=1,
        phy_type=network.PHY_IP101,
        mdc=machine.Pin(31),
        mdio=machine.Pin(52),
        power=machine.Pin(51),
    )

    ethernet_0.active(True)
    print("wait network connect")
    while not (ethernet_0.status()) == (network.ETH_GOT_IP):
        print(".")
        time.sleep(1)
    print("local network is connected")
    print((str("IP:") + str((ethernet_0.ifconfig()[0]))))
    print("Please press the Btn")


def loop():
    global ethernet_0, http_req
    M5.update()
    if BtnA.wasClicked():
        print("Btn Pressed")
        http_req = requests2.get(
            "https://wttr.in/?format=%22%C,%20%t%22", headers={"Content-Type": "application/json"}
        )
        print((str("Status Code:") + str((http_req.status_code))))
        print((str("Text:") + str((http_req.text))))


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
