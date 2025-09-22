# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import m5utils


page0 = None
led0 = None
switch0 = None
slider0 = None
label0 = None
brightness = None


def switch0_checked_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    led0.set_color(0x3366FF)
    led0.on()


def switch0_unchecked_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    led0.off()
    led0.set_color(0x000000)


def slider0_value_changed_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    brightness = slider0.get_value()
    led0.set_brightness(int(m5utils.remap(brightness, 0, 100, 80, 255)))
    label0.set_text(str((str("Brightness: ") + str((str(brightness) + str("%"))))))
    print(led0.get_brightness())


def switch0_event_handler(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return


def slider0_event_handler(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider0_value_changed_event(event_struct)
    return


def setup():
    global page0, led0, switch0, slider0, label0, brightness
    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    led0 = m5ui.M5LED(x=135, y=14, size=50, color=0x00FF00, on=True, parent=page0)
    switch0 = m5ui.M5Switch(
        x=110,
        y=159,
        w=100,
        h=40,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )
    slider0 = m5ui.M5Slider(
        x=20,
        y=118,
        w=280,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Brightness: 0%",
        x=99,
        y=85,
        text_c=0x2193F3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)
    slider0.add_event_cb(slider0_event_handler, lv.EVENT.ALL, None)
    page0.screen_load()
    led0.off()
    brightness = 0
    slider0.set_value(0, True)
    led0.align_to(page0, lv.ALIGN.TOP_MID, 0, 5)
    label0.align_to(slider0, lv.ALIGN.CENTER, 0, -25)
    led0.set_brightness(80)
    print(led0.get_brightness())


def loop():
    global page0, led0, switch0, slider0, label0, brightness
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
