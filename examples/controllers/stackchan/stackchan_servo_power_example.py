# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan


page0 = None
label_title = None
label_voltage = None
label_current = None
label_power = None
stackchan = None
last_time = None
volatge = None
current = None
power = None


def setup():
    global \
        page0, \
        label_title, \
        label_voltage, \
        label_current, \
        label_power, \
        stackchan, \
        last_time, \
        volatge, \
        current, \
        power

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Power Info",
        x=56,
        y=5,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_voltage = m5ui.M5Label(
        "Voltage:",
        x=10,
        y=80,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_current = m5ui.M5Label(
        "Current:",
        x=10,
        y=115,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_power = m5ui.M5Label(
        "Power:",
        x=25,
        y=150,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    last_time = time.ticks_ms()


def loop():
    global \
        page0, \
        label_title, \
        label_voltage, \
        label_current, \
        label_power, \
        stackchan, \
        last_time, \
        volatge, \
        current, \
        power
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        volatge = stackchan.get_battery_voltage()
        current = stackchan.get_battery_current()
        power = stackchan.get_battery_power()
        label_voltage.set_text(str((str("Voltage: ") + str((str(volatge) + str(" V"))))))
        label_current.set_text(str((str("Current: ") + str((str(current) + str(" A"))))))
        label_power.set_text(str((str("Power: ") + str((str(power) + str(" W"))))))


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
