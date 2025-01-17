# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import USBModule
import time



module_usb_0 = None
last_time = None
i = None
last_set_time = None
value = None
state = None
toggle = None


def setup():
    global module_usb_0, last_time, last_set_time, value, state, toggle, i
    M5.begin()
    Widgets.fillScreen(0x222222)
    module_usb_0 = USBModule(pin_cs=1, pin_int=10)
    module_usb_0.write_gpout(0, 0)
    module_usb_0.write_gpout(1, 1)
    module_usb_0.write_gpout(2, 0)
    module_usb_0.write_gpout(3, 1)
    module_usb_0.write_gpout(4, 0)
    state = [0] * 5
    toggle = True


def loop():
    global module_usb_0, last_time, last_set_time, value, state, toggle, i
    M5.update()
    module_usb_0.poll_data()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 200:
        last_time = time.ticks_ms()
        for i in range(5):
            value = module_usb_0.read_gpin(i)
            state[int((i + 1) - 1)] = value
        print(state)
    if (time.ticks_diff((time.ticks_ms()), last_set_time)) > 1000:
        last_set_time = time.ticks_ms()
        if toggle:
            for i in range(5):
                module_usb_0.write_gpout(i, 1)
        else:
            for i in range(5):
                module_usb_0.write_gpout(i, 0)
        toggle = not toggle


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

