# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Cat1Unit


page0 = None
button0 = None
label0 = None
label1 = None
cat1cn_0 = None


def button0_clicked_event(event_struct):
    global page0, button0, label0, label1, cat1cn_0
    cat1cn_0.http_request(
        1,
        "http://httpbin.org/post",
        {"Content-Type": "application/json", "Custom-Header": "MyHeaderValue"},
        {"message": "Hello from M5Stack!", "status": "active"},
    )
    label0.set_text(str((str("Data content:") + str((cat1cn_0.data_content)))))
    label1.set_text(str((str("Response status code:") + str((cat1cn_0.response_code)))))


def button0_event_handler(event_struct):
    global page0, button0, label0, label1, cat1cn_0
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button0_clicked_event(event_struct)
    return


def setup():
    global page0, button0, label0, label1, cat1cn_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    button0 = m5ui.M5Button(
        text="Send HTTP POST",
        x=82,
        y=104,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Data content:",
        x=3,
        y=8,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "Response status code:",
        x=4,
        y=35,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    cat1cn_0 = Cat1Unit(2, port=(33, 32))
    page0.screen_load()


def loop():
    global page0, button0, label0, label1, cat1cn_0
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
