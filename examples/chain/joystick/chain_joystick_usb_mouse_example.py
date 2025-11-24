# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import JoystickChain
from chain import ChainBus
from usb.device.mouse import Mouse
import m5utils


bus2 = None
mouse = None
chain_joystick_0 = None


key_press = None
x = None
y = None


def chain_joystick_0_click_event(args):
    global bus2, mouse, chain_joystick_0, key_press, x, y
    key_press = True


def setup():
    global bus2, mouse, chain_joystick_0, key_press, x, y

    M5.begin()
    bus2 = ChainBus(2, tx=6, rx=5)
    chain_joystick_0 = JoystickChain(bus2, 1)
    chain_joystick_0.set_click_callback(chain_joystick_0_click_event)
    print(chain_joystick_0.get_firmware_version())
    mouse = Mouse()
    key_press = False


def loop():
    global bus2, mouse, chain_joystick_0, key_press, x, y
    M5.update()
    if mouse.is_open():
        x = int(m5utils.remap(chain_joystick_0.get_x(), -128, 127, -64, 64))
        y = int(m5utils.remap(chain_joystick_0.get_y(), -128, 127, 64, -64))
        mouse.move(x, y)
        if key_press:
            mouse.click_left(True)
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
