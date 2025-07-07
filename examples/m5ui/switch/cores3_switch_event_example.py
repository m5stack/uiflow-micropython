# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
switch0 = None


def switch0_checked_event(event_struct):
    global page0, switch0

    print("switch0 checked")


def switch0_unchecked_event(event_struct):
    global page0, switch0

    print("switch0 unchecked")


def switch0_event_handler(event_struct):
    global page0, switch0
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return


def setup():
    global page0, switch0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    switch0 = m5ui.M5Switch(
        x=128,
        y=91,
        w=60,
        h=30,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )

    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    switch0.set_bg_color(0x666666, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    switch0.set_bg_color(0x33FF33, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)


def loop():
    global page0, switch0
    M5.update()


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
