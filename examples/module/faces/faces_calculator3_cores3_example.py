# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import FacesCalculator3Module


title0 = None
label0 = None
faces_calculator3_0 = None


event_args = None


def faces_calculator3_0_key_event(args):
    global title0, label0, faces_calculator3_0, event_args
    event_args = chr(args)
    label0.setText(str((str("Key: ") + str(event_args))))


def setup():
    global title0, label0, faces_calculator3_0, event_args

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Faces Calculator3 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label("label0", 1, 112, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    faces_calculator3_0 = FacesCalculator3Module(address=0x08)
    faces_calculator3_0.set_callback(faces_calculator3_0_key_event)


def loop():
    global title0, label0, faces_calculator3_0, event_args
    M5.update()
    faces_calculator3_0.tick()


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
