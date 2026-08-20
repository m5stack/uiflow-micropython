# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import RTC


page0 = None
label_title = None
label_date = None
label_hour = None
label_colon_1 = None
label_minute = None
label_colon_2 = None
label_second = None
button_hour_minus = None
button_hour_plus = None
button_minute_minus = None
button_minute_plus = None
button_second_minus = None
button_second_plus = None
label_hour_control = None
label_minute_control = None
label_second_control = None
rtc = None


editing = None
hour = None
minute = None
second = None
now = None
year = None
month = None
day = None


def button_hour_minus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    hour = hour - 1
    if hour < 0:
        hour = 23
    label_hour.set_text(str(hour))


def button_hour_plus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    hour = hour + 1
    if hour > 23:
        hour = 0
    label_hour.set_text(str(hour))


def button_minute_minus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    minute = minute - 1
    if minute < 0:
        minute = 59
    label_minute.set_text(str(minute))


def button_minute_plus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    minute = minute + 1
    if minute > 59:
        minute = 0
    label_minute.set_text(str(minute))


def button_second_minus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    second = second - 1
    if second < 0:
        second = 59
    label_second.set_text(str(second))


def button_second_plus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    second = second + 1
    if second > 59:
        second = 0
    label_second.set_text(str(second))


def button_hour_minus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_hour_minus_pressed_event(event_struct)
    return


def button_hour_plus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_hour_plus_pressed_event(event_struct)
    return


def button_minute_minus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_minute_minus_pressed_event(event_struct)
    return


def button_minute_plus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_minute_plus_pressed_event(event_struct)
    return


def button_second_minus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_second_minus_pressed_event(event_struct)
    return


def button_second_plus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_second_plus_pressed_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "RTC Example",
        x=480,
        y=35,
        text_c=0xE99628,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_date = m5ui.M5Label(
        "2026-01-01",
        x=510,
        y=125,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_hour = m5ui.M5Label(
        "00",
        x=440,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_colon_1 = m5ui.M5Label(
        ":",
        x=565,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_minute = m5ui.M5Label(
        "00",
        x=635,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_colon_2 = m5ui.M5Label(
        ":",
        x=760,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_second = m5ui.M5Label(
        "00",
        x=830,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_hour_minus = m5ui.M5Button(
        text="-",
        x=100,
        y=390,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_hour_plus = m5ui.M5Button(
        text="+",
        x=290,
        y=390,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_minute_minus = m5ui.M5Button(
        text="-",
        x=480,
        y=390,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_minute_plus = m5ui.M5Button(
        text="+",
        x=670,
        y=390,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_second_minus = m5ui.M5Button(
        text="-",
        x=860,
        y=390,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_second_plus = m5ui.M5Button(
        text="+",
        x=1050,
        y=390,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_hour_control = m5ui.M5Label(
        "HOUR",
        x=195,
        y=320,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_minute_control = m5ui.M5Label(
        "MIN",
        x=618,
        y=320,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_second_control = m5ui.M5Label(
        "SEC",
        x=998,
        y=320,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    button_hour_minus.add_event_cb(button_hour_minus_event_handler, lv.EVENT.ALL, None)
    button_hour_plus.add_event_cb(button_hour_plus_event_handler, lv.EVENT.ALL, None)
    button_minute_minus.add_event_cb(button_minute_minus_event_handler, lv.EVENT.ALL, None)
    button_minute_plus.add_event_cb(button_minute_plus_event_handler, lv.EVENT.ALL, None)
    button_second_minus.add_event_cb(button_second_minus_event_handler, lv.EVENT.ALL, None)
    button_second_plus.add_event_cb(button_second_plus_event_handler, lv.EVENT.ALL, None)

    rtc = RTC()
    page0.screen_load()
    now = rtc.datetime()
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[4]
    minute = now[5]
    second = now[6]
    editing = False
    label_date.set_text(
        str((str((str(year) + str("-"))) + str((str((str(month) + str("-"))) + str(day)))))
    )
    label_hour.set_text(str(hour))
    label_minute.set_text(str(minute))
    label_second.set_text(str(second))
    button_hour_minus.set_pos(100, 390)
    button_hour_minus.set_size(170, 90)
    button_hour_plus.set_pos(290, 390)
    button_hour_plus.set_size(170, 90)
    button_minute_minus.set_pos(480, 390)
    button_minute_minus.set_size(170, 90)
    button_minute_plus.set_pos(670, 390)
    button_minute_plus.set_size(170, 90)
    button_second_minus.set_pos(860, 390)
    button_second_minus.set_size(170, 90)
    button_second_plus.set_pos(1050, 390)
    button_second_plus.set_size(170, 90)


def loop():
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    M5.update()
    now = rtc.datetime()
    if not editing:
        year = now[0]
        month = now[1]
        day = now[2]
        hour = now[4]
        minute = now[5]
        second = now[6]
        label_date.set_text(
            str((str((str(year) + str("-"))) + str((str((str(month) + str("-"))) + str(day)))))
        )
        label_hour.set_text(str(hour))
        label_minute.set_text(str(minute))
        label_second.set_text(str(second))
    else:
        rtc.init((year, month, day, hour, minute, second, 0, 0))
        editing = False


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
