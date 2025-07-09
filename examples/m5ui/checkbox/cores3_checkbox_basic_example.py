# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
checkbox0 = None
checkbox1 = None
label0 = None


def checkbox0_checked_event(event_struct):
    global page0, checkbox0, checkbox1, label0
    label0.set_text(str("checked"))


def checkbox0_unchecked_event(event_struct):
    global page0, checkbox0, checkbox1, label0
    label0.set_text(str("unchecked"))


def checkbox0_event_handler(event_struct):
    global page0, checkbox0, checkbox1, label0
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            checkbox0_checked_event(event_struct)
        else:
            checkbox0_unchecked_event(event_struct)
    return


def setup():
    global page0, checkbox0, checkbox1, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    checkbox0 = m5ui.M5Checkbox(
        title="checkbox0",
        value=False,
        x=77,
        y=106,
        title_c=0x212121,
        title_font=lv.font_montserrat_24,
        bullet_border_c=0x2193F3,
        bullet_bg_c=0xFFFFFF,
        parent=page0,
    )
    checkbox1 = m5ui.M5Checkbox(
        title="checkbox1",
        value=False,
        x=80,
        y=54,
        title_c=0x212121,
        title_font=lv.font_montserrat_24,
        bullet_border_c=0x2193F3,
        bullet_bg_c=0xFFFFFF,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=124,
        y=153,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    checkbox0.add_event_cb(checkbox0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    checkbox1.set_state(lv.STATE.DISABLED, True)
    checkbox1.set_state(lv.STATE.CHECKED, True)


def loop():
    global page0, checkbox0, checkbox1, label0
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
