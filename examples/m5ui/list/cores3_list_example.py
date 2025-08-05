# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
list0 = None
File = None
New = None
Open = None
Save = None
Delete = None


def New_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("New")


def Open_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("Open")


def Save_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("Save")


def Delete_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("Delete")


def New_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        New_clicked_event(event_struct)
    return


def Open_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        Open_clicked_event(event_struct)
    return


def Save_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        Save_clicked_event(event_struct)
    return


def Delete_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        Delete_clicked_event(event_struct)
    return


def setup():
    global page0, list0, File, New, Open, Save, Delete

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    list0 = m5ui.M5List(x=-1, y=2, w=320, h=240, parent=page0)
    File = list0.add_text("File")
    New = list0.add_button(lv.SYMBOL.BULLET, "New")

    page0.screen_load()
    Open = list0.add_button(lv.SYMBOL.DIRECTORY, "Open")
    Save = list0.add_button(lv.SYMBOL.SAVE, "Save")
    Delete = list0.add_button(lv.SYMBOL.CLOSE, "Delete")

    New.add_event_cb(New_event_handler, lv.EVENT.ALL, None)
    Open.add_event_cb(Open_event_handler, lv.EVENT.ALL, None)
    Save.add_event_cb(Save_event_handler, lv.EVENT.ALL, None)
    Delete.add_event_cb(Delete_event_handler, lv.EVENT.ALL, None)

    New.set_text_color(0xFFFF00, 255, lv.PART.MAIN | lv.STATE.PRESSED)
    Open.set_text_color(0xFFFF00, 100, lv.PART.MAIN | lv.STATE.PRESSED)
    Save.set_text_color(0xFFFF00, 255, lv.PART.MAIN | lv.STATE.PRESSED)
    Delete.set_text_color(0xFFFF00, 255, lv.PART.MAIN | lv.STATE.PRESSED)


def loop():
    global page0, list0, File, New, Open, Save, Delete
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
