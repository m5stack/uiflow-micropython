# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network


ap_client = None


def setup():
    M5.begin()
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.config(essid="test")
    wlan.config(password="testtest")
    wlan.config(txpower=20)
    wlan.config(authmode=network.AUTH_WPA_WPA2_PSK)
    wlan.config(dhcp_hostname="m5stack")
    wlan.config(max_clients=3)
    while not (wlan.isconnected()):
        pass
    print(wlan.ifconfig()[0])
    print(wlan.ifconfig()[1])
    print(wlan.ifconfig()[2])
    print(wlan.ifconfig()[3])
    print(wlan.config("hidden"))
    print(wlan.config("authmode"))
    print(wlan.config("channel"))
    print(wlan.config("dhcp_hostname"))
    print(wlan.config("max_clients"))
    print(wlan.config("txpower"))
    print("stations:")
    for ap_client in wlan.status("stations"):
        print(ap_client[0])


def loop():
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
