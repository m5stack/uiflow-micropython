# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network
import socket
import time


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
wlan = None
udpc = None


count = None
resp = None


def setup():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        wlan, \
        udpc, \
        count, \
        resp

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("UDP Clinet", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Local IP:", 4, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Server IP:", 4, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Server Port:", 4, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Send:", 4, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Recv:", 4, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 136, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 136, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 136, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 136, 118, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("label9", 136, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    udpc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpc.connect(("192.168.8.236", 8000))
    count = 0
    label5.setText(str(wlan.ifconfig()[0]))
    label6.setText(str("192.168.8.236"))
    label7.setText(str("8000"))


def loop():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        wlan, \
        udpc, \
        count, \
        resp
    M5.update()
    udpc.send(str(count))
    time.sleep_ms(100)
    resp = udpc.recv(1024)
    label8.setText(str(count))
    label9.setText(str(resp))
    count = (count if isinstance(count, (int, float)) else 0) + 1
    time.sleep(1)


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
