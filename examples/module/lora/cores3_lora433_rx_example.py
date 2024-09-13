# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoraModule
import time


label0 = None
recvdata = None
label1 = None
timestamp = None
title0 = None
lora433_0 = None


lora433_data = None


def lora433_0_receive_event(received_data):
    global label0, recvdata, label1, timestamp, title0, lora433_0, lora433_data
    lora433_data = received_data
    recvdata.setText(str(lora433_data.decode()))
    timestamp.setText(str(time.ticks_ms()))


def setup():
    global label0, recvdata, label1, timestamp, title0, lora433_0, lora433_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Received:", 8, 31, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    recvdata = Widgets.Label("label1", 13, 73, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label1 = Widgets.Label("Timestamp:", 9, 137, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    timestamp = Widgets.Label("label2", 15, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    title0 = Widgets.Title("LoRa Module Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    lora433_0 = LoraModule(0, 10, 5, null, 8, 250, 8, 12, 200)
    lora433_0.set_irq_callback(lora433_0_receive_event)
    lora433_0.start_recv()


def loop():
    global label0, recvdata, label1, timestamp, title0, lora433_0, lora433_data
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
