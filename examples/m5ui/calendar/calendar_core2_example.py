# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
calendar0 = None


year = None
month = None
day = None


def calendar0_value_changed_event(date):
    global page0, calendar0, year, month, day
    year = date.year
    month = date.month
    day = date.day
    calendar0.set_today_date(year, month, day)
    print((str("Today is:") + str((str(year) + str((str(month) + str(day)))))))


def calendar0_event_handler(event_struct):
    global page0, calendar0, year, month, day
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED:
        date = lv.calendar_date_t()
        if calendar0.get_pressed_date(date) == lv.RESULT.OK:
            calendar0_value_changed_event(date)
    return


def setup():
    global page0, calendar0, year, month, day

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    calendar0 = m5ui.M5Calendar(
        x=0,
        y=0,
        w=320,
        h=240,
        style="arrow",
        today_date=[2025, 8, 7],
        show_month=[2025, 8],
        parent=page0,
    )

    calendar0.add_event_cb(calendar0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()


def loop():
    global page0, calendar0, year, month, day
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
