# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit
from usb.device.keyboard import Keyboard 
from hardware import I2C
from hardware import Pin


label = None
keyboard = None
i2c0 = None
cardkb_0 = None
key = None
update = None

def cardkb_0_pressed_event(kb):
    global label, keyboard, i2c0, cardkb_0, key, update
    key = cardkb_0.get_key()
    update = True

def setup():
    global label, keyboard, i2c0, cardkb_0, key, update
    M5.begin()
    Widgets.fillScreen(0x222222)
    label = Widgets.Label("USB Keyboard", 73, 6, 1.0, 0x3cc7f1, 0x222222, Widgets.FONTS.DejaVu24)
    keyboard = Keyboard()
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    cardkb_0 = CardKBUnit(i2c0)
    cardkb_0.set_callback(cardkb_0_pressed_event)
    update = False

def loop():
    global label, keyboard, i2c0, cardkb_0, key, update
    M5.update()
    cardkb_0.tick()
    if keyboard.is_open():
        if update:
            keyboard.input(str(chr(key)))
            update = False

if __name__ == '__main__':
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

