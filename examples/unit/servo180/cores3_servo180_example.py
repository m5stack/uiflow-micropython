# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Servo180Unit


page0 = None
label0 = None
button0 = None
slider0 = None
label1 = None
slider1 = None
button1 = None
label2 = None
slider2 = None
button2 = None
label3 = None
slider3 = None
button3 = None
servo_0 = None


def button0_short_clicked_event(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    servo_0.set_angle(slider0.get_value())


def button1_short_clicked_event(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    servo_0.set_duty(slider1.get_value())


def button2_short_clicked_event(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    servo_0.set_percent(slider2.get_value())


def button3_short_clicked_event(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    servo_0.set_radian((slider3.get_value()) / 100)


def button0_event_handler(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return


def button1_event_handler(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button1_short_clicked_event(event_struct)
    return


def button2_event_handler(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button2_short_clicked_event(event_struct)
    return


def button3_event_handler(event_struct):
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button3_short_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "angle:",
        x=6,
        y=36,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="set",
        x=258,
        y=26,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    slider0 = m5ui.M5Slider(
        x=60,
        y=38,
        w=180,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=180,
        value=180,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "duty:",
        x=6,
        y=76,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    slider1 = m5ui.M5Slider(
        x=60,
        y=74,
        w=180,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=500,
        max_value=2500,
        value=500,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    button1 = m5ui.M5Button(
        text="set",
        x=258,
        y=66,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "per:",
        x=6,
        y=116,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    slider2 = m5ui.M5Slider(
        x=60,
        y=118,
        w=180,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=100,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    button2 = m5ui.M5Button(
        text="set",
        x=258,
        y=110,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label3 = m5ui.M5Label(
        "rad:",
        x=6,
        y=162,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    slider3 = m5ui.M5Slider(
        x=60,
        y=163,
        w=180,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=314,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    button3 = m5ui.M5Button(
        text="set",
        x=258,
        y=152,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)
    button1.add_event_cb(button1_event_handler, lv.EVENT.ALL, None)
    button2.add_event_cb(button2_event_handler, lv.EVENT.ALL, None)
    button3.add_event_cb(button3_event_handler, lv.EVENT.ALL, None)

    servo_0 = Servo180Unit((8, 9))
    label0.align_to(page0, lv.ALIGN.TOP_LEFT, 6, 20)
    label1.align_to(label0, lv.ALIGN.OUT_BOTTOM_RIGHT, 0, 40)
    label2.align_to(label1, lv.ALIGN.OUT_BOTTOM_RIGHT, 0, 40)
    label3.align_to(label2, lv.ALIGN.OUT_BOTTOM_RIGHT, 0, 40)
    slider0.align_to(label0, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    slider1.align_to(label1, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    slider2.align_to(label2, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    slider3.align_to(label3, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    button0.align_to(slider0, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    button1.align_to(slider1, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    button2.align_to(slider2, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    button3.align_to(slider3, lv.ALIGN.OUT_RIGHT_MID, 20, 0)
    page0.screen_load()
    servo_0.set_angle(59)


def loop():
    global \
        page0, \
        label0, \
        button0, \
        slider0, \
        label1, \
        slider1, \
        button1, \
        label2, \
        slider2, \
        button2, \
        label3, \
        slider3, \
        button3, \
        servo_0
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
