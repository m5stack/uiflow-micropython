# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import KeyChain
from chain import ChainBus
from usb.device.keyboard import Keyboard
from usb.device.hid import KeyCode


bus2 = None
keyboard = None
chain_key_0 = None


key_press = None


def chain_key_0_click_event(args):
    global bus2, keyboard, chain_key_0, key_press
    key_press = True


def setup():
    global bus2, keyboard, chain_key_0, key_press

    M5.begin()
    bus2 = ChainBus(2, tx=6, rx=5)
    keyboard = Keyboard()
    chain_key_0 = KeyChain(bus2, 1)
    chain_key_0.set_click_callback(chain_key_0_click_event)
    key_press = False


def loop():
    global bus2, keyboard, chain_key_0, key_press
    M5.update()
    if keyboard.is_open():
        if key_press:
            keyboard.input(KeyCode.A)
            key_press = False


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
