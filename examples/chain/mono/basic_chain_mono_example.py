# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import MonoChain


label_title = None
label_text = None
label_state = None
label_rotation = None
label_direction = None
bus2 = None
chain_mono_0 = None
scroll_state = None
display_rotation = None
brightness = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    scroll_state = (scroll_state if isinstance(scroll_state, (int, float)) else 0) + 1
    if scroll_state >= 2:
        scroll_state = 0
    chain_mono_0.set_scroll_state(scroll_state)


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    display_rotation = (display_rotation if isinstance(display_rotation, (int, float)) else 0) + 1
    if display_rotation >= 4:
        display_rotation = 0
    chain_mono_0.set_display_rotation(display_rotation, save=False)


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    brightness = (brightness if isinstance(brightness, (int, float)) else 0) + 1
    if brightness >= 7:
        brightness = 0
    chain_mono_0.set_brightness(brightness, save=False)


def setup():
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Chain Mono Control", 37, 11, 1.0, 0x0F92E8, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_text = Widgets.Label(
        "M5STACK", 62, 80, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat40
    )
    label_state = Widgets.Label(
        "state", 40, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_rotation = Widgets.Label(
        "brighness", 204, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_direction = Widgets.Label(
        "rotation", 118, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_mono_0 = MonoChain(bus2, 1)
    chain_mono_0.set_display_mode(MonoChain.MODE_SCROLL)
    chain_mono_0.set_display_rotation(MonoChain.ROTATION_0, save=True)
    chain_mono_0.set_scroll_text(
        "M5STACK", MonoChain.SCROLL_DIR_RIGHT, MonoChain.SCROLL_MODE_LOOP, 100
    )
    scroll_state = 0
    brightness = 5
    display_rotation = 0
    chain_mono_0.set_brightness(brightness, save=False)
    chain_mono_0.set_display_rotation(display_rotation, save=True)


def loop():
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
