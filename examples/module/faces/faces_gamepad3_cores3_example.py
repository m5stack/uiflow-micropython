# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import FacesGamepad3Module


title0 = None
label0 = None
faces_gamepad3_0 = None


button_state = None


def faces_gamepad3_0_button_up_event(key_state):
    global title0, label0, faces_gamepad3_0, button_state
    button_state = key_state
    if button_state:
        label0.setText(str((str("Key: ") + str("Up Press"))))
    else:
        label0.setText(str((str("Key: ") + str("Up Release"))))


def faces_gamepad3_0_button_down_event(key_state):
    global title0, label0, faces_gamepad3_0, button_state
    button_state = key_state
    if button_state:
        label0.setText(str((str("Key: ") + str("Down Press"))))
    else:
        label0.setText(str((str("Key: ") + str("Down Release"))))


def setup():
    global title0, label0, faces_gamepad3_0, button_state

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Faces Gamepad3 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label("label0", 5, 104, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    faces_gamepad3_0 = FacesGamepad3Module(address=0x08)
    faces_gamepad3_0.set_callback(faces_gamepad3_0.BUTTON_UP, faces_gamepad3_0_button_up_event)
    faces_gamepad3_0.set_callback(faces_gamepad3_0.BUTTON_DOWN, faces_gamepad3_0_button_down_event)
    label0.setText(str("Pls press key"))


def loop():
    global title0, label0, faces_gamepad3_0, button_state
    M5.update()
    faces_gamepad3_0.tick()


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
