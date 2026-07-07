# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from tab5 import Keyboard
from hardware import Pin
from hardware import SoftI2C


page0 = None
textarea0 = None
tab5_keyboard_0 = None


key_char = None


def tab5_keyboard_0_char_pressed_event(kb):
    global page0, textarea0, tab5_keyboard_0, key_char
    key_char = kb
    textarea0.add_text(str(key_char))


def setup():
    global page0, textarea0, tab5_keyboard_0, key_char

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=0,
        y=0,
        w=1280,
        h=720,
        font=lv.font_montserrat_24,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )

    softi2c_0 = SoftI2C(scl=Pin(1), sda=Pin(0), freq=100000)
    tab5_keyboard_0 = Keyboard(softi2c_0, 0x6D)
    tab5_keyboard_0.set_callback(tab5_keyboard_0_char_pressed_event)
    tab5_keyboard_0.set_keyboard_mode(tab5_keyboard_0.MODE_CHAR)
    page0.screen_load()
    textarea0.set_text("")


def loop():
    global page0, textarea0, tab5_keyboard_0, key_char
    M5.update()
    tab5_keyboard_0.tick()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
