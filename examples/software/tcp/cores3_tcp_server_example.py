# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network
import socket


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
title0 = None
wlan = None
tcps = None


con_info = None
con_sock = None
address = None
data = None


def setup():
    global \
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
        title0, \
        wlan, \
        tcps, \
        con_info, \
        con_sock, \
        address, \
        data

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Local IP:", 4, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Local Port:", 4, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Remote IP:", 4, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Remote Port:", 4, 118, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Data:", 4, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 136, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 136, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 136, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 136, 118, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("label9", 136, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("TCP Server", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    tcps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcps.bind(("0.0.0.0", 8001))
    tcps.listen(5)
    tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    label5.setText(str(wlan.ifconfig()[0]))
    label6.setText(str("8001"))


def loop():
    global \
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
        title0, \
        wlan, \
        tcps, \
        con_info, \
        con_sock, \
        address, \
        data
    M5.update()
    con_info = tcps.accept()
    con_sock = con_info[0]
    address = con_info[1]
    label7.setText(str(address[0]))
    label8.setText(str(address[1]))
    while True:
        data = con_sock.recv(1024)
        label9.setText(str(data))
        con_sock.send(data)


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
