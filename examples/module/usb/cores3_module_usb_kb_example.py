# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import USBModule


module_usb_0 = None
modifier = None
indata = None


def setup():
    global module_usb_0, modifier, indata
    M5.begin()
    Widgets.fillScreen(0x222222)
    module_usb_0 = USBModule(pin_cs=1, pin_int=10)


def loop():
    global module_usb_0, modifier, indata
    M5.update()
    module_usb_0.poll_data()
    modifier = module_usb_0.read_kb_modifier()
    if modifier & 0x01:
        print("Left Control pressed")
    if modifier & 0x02:
        print("Left Shift pressed")
    if modifier & 0x04:
        print("Left Alt pressed")
    if modifier & 0x08:
        print("Left GUI pressed")
    if modifier & 0x10:
        print("Right Control pressed")
    if modifier & 0x20:
        print("Right Shift pressed")
    if modifier & 0x40:
        print("Right Alt pressed")
    if modifier & 0x80:
        print("Right GUI pressed")
    indata = module_usb_0.read_kb_input(True)
    if indata:
        print(indata)


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
