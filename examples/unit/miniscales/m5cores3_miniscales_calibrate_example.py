# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import MiniScaleUnit
import time


page0 = None
label_weight = None
button0 = None
label_tip = None
label_title = None
i2c0 = None
miniscales_0 = None
state = None
adc_0 = None
adc_100 = None
last_time = None
weight = None


def button0_short_clicked_event(event_struct):
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight
    Speaker.tone(888, 200)
    if state == 0:
        state = 1
        adc_0 = miniscales_0.adc
        print((str("ADC0 Value: ") + str(adc_0)))
        label_tip.set_text(str("Put 100g weight, then press button."))
    elif state == 1:
        state = 2
        adc_100 = miniscales_0.adc
        print((str("ADC100 Value: ") + str(adc_100)))
        print("do calibrate")
        miniscales_0.calibration(0, adc_0, 100, adc_100)
        label_tip.set_text(str("Remove all items, then press button."))
    elif state == 2:
        state = 3
        print("tare the scale")
        print((str("Tare: ") + str((str((miniscales_0.weight)) + str(" g")))))
        miniscales_0.tare()
        label_tip.set_text(str("Weight"))
        label_tip.set_flag(lv.obj.FLAG.HIDDEN, True)
        button0.set_flag(lv.obj.FLAG.HIDDEN, True)
        miniscales_0.set_average_filter_level(5)


def button0_event_handler(event_struct):
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label_weight = m5ui.M5Label(
        "Weight: ",
        x=14,
        y=90,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="Button",
        x=116,
        y=160,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:",
        x=10,
        y=50,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_title = m5ui.M5Label(
        "MiniScales",
        x=93,
        y=5,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    miniscales_0 = MiniScaleUnit(i2c0)
    page0.screen_load()
    label_tip.set_text(str("Remove all items, then press button."))
    label_weight.set_text(str("Weight: -- g"))
    label_weight.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    state = 0
    button0.set_size(100, 50)
    button0.align_to(page0, lv.ALIGN.CENTER, 0, 60)
    Speaker.begin()
    Speaker.setVolumePercentage(0.6)
    Speaker.tone(888, 200)


def loop():
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight
    M5.update()
    if state == 3:
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
            last_time = time.ticks_ms()
            weight = int(miniscales_0.weight)
            label_weight.set_text(str((str("Weight:  ") + str((str(weight) + str(" g"))))))
            label_weight.align_to(page0, lv.ALIGN.CENTER, 0, 0)


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
