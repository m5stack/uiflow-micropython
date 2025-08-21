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
from unit import MQUnit


page0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
mq_0 = None


valid = None


def setup():
    global page0, label0, label1, label2, i2c0, mq_0, valid

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "Valid Flag:",
        x=1,
        y=76,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "ADC 8bits:0",
        x=1,
        y=111,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "ADC 12bits:0",
        x=1,
        y=145,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    mq_0 = MQUnit(i2c0, 0x11)
    mq_0.set_mq_mode(1)
    page0.screen_load()


def loop():
    global page0, label0, label1, label2, i2c0, mq_0, valid
    M5.update()
    valid = mq_0.get_valid_tags()
    if valid:
        label0.set_text(str((str("Valid Flag:") + str(valid))))
        label1.set_text(str((str("ADC 8bits:") + str((mq_0.get_adc_value(0))))))
        label2.set_text(str((str("ADC 12bits:") + str((mq_0.get_adc_value(1))))))
    else:
        label0.set_text(str("Valid Flag: Wait heating"))


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
