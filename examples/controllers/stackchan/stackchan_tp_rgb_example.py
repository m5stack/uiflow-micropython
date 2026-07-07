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


HOLD_MS = 300
TOUCH_COLORS = (0x33CC00, 0x00CCCC, 0x000099)
TOUCH_TONES = (700, 900, 1100)
TOUCH_LEDS = (
    ((0, 0), (0, 1), (1, 0), (1, 1)),
    ((0, 2), (0, 3), (1, 2), (1, 3)),
    ((0, 4), (0, 5), (1, 4), (1, 5)),
)

page0 = None
label_title = None
stackchan = None
tp = None
last_time = None
active = None


def set_touch_group(index, color):
    for strip, led in TOUCH_LEDS[index]:
        stackchan.set_rgb_color(strip, led, color)


def setup():
    global page0, label_title, stackchan, tp, last_time, active

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "TP & RGB Strip Example",
        x=13,
        y=10,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    now = time.ticks_ms()
    last_time = [now, now, now]
    active = [False, False, False]
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    stackchan.set_rgb_color(0x000000)


def loop():
    global page0, label_title, stackchan, tp, last_time, active
    M5.update()
    now = time.ticks_ms()
    tp = stackchan.get_touch()
    if tp is None:
        tp = [0, 0, 0]

    for index in range(3):
        if tp[index]:
            last_time[index] = now
            if not active[index]:
                active[index] = True
                set_touch_group(index, TOUCH_COLORS[index])
                Speaker.tone(TOUCH_TONES[index], 50)
        elif active[index] and time.ticks_diff(now, last_time[index]) > HOLD_MS:
            active[index] = False
            set_touch_group(index, 0x000000)


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
