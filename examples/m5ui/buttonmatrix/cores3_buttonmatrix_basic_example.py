# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
textarea0 = None
buttonmatrix0 = None
label0 = None
label1 = None


def buttonmatrix0_value_changed_event(event_struct):
    global page0, textarea0, buttonmatrix0, label0, label1
    label1.set_text(str(buttonmatrix0.get_button_text(buttonmatrix0.get_selected_button())))


def buttonmatrix0_event_handler(event_struct):
    global page0, textarea0, buttonmatrix0, label0, label1
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        buttonmatrix0_value_changed_event(event_struct)
    return


def setup():
    global page0, textarea0, buttonmatrix0, label0, label1

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="",
        placeholder="Placeholder...",
        x=24,
        y=15,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    buttonmatrix0 = m5ui.M5ButtonMatrix(
        ["0", "1", "2", "4", "\n", "5", "6", "7", "8", "9"],
        x=25,
        y=100,
        w=260,
        h=130,
        target_textarea=textarea0,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "last key:",
        x=189,
        y=15,
        text_c=0xC9C9C9,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "label1",
        x=203,
        y=42,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    buttonmatrix0.add_event_cb(buttonmatrix0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, textarea0, buttonmatrix0, label0, label1
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
