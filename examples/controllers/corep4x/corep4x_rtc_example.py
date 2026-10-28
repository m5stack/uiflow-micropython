# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import RTC
import time


page_live = None
page_edit = None
label_title = None
label_date = None
label_live_hour = None
label_live_colon_1 = None
label_live_min = None
label_live_colon_2 = None
label_live_sec = None
button_set = None
label_edit_title = None
label_hour_name = None
label_min_name = None
label_sec_name = None
label_hour = None
label_min = None
label_sec = None
button_hour_plus = None
button_hour_minus = None
button_min_plus = None
button_min_minus = None
button_sec_plus = None
button_sec_minus = None
button_cancel = None
button_save = None
rtc = None


edit_hour = None
edit_min = None
edit_sec = None


def button_set_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    page_edit.screen_load()
    edit_hour = (rtc.datetime())[4]
    edit_min = (rtc.datetime())[5]
    edit_sec = (rtc.datetime())[6]
    if edit_hour < 10:
        label_hour.set_text(str((str("0") + str(edit_hour))))
    else:
        label_hour.set_text(str(edit_hour))
    if edit_min < 10:
        label_min.set_text(str((str("0") + str(edit_min))))
    else:
        label_min.set_text(str(edit_min))
    if edit_sec < 10:
        label_sec.set_text(str((str("0") + str(edit_sec))))
    else:
        label_sec.set_text(str(edit_sec))


def button_hour_plus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_hour = (edit_hour + 1) % 24
    if edit_hour < 10:
        label_hour.set_text(str((str("0") + str(edit_hour))))
    else:
        label_hour.set_text(str(edit_hour))


def button_hour_minus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_hour = (edit_hour + -1) % 24
    if edit_hour < 10:
        label_hour.set_text(str((str("0") + str(edit_hour))))
    else:
        label_hour.set_text(str(edit_hour))


def button_min_plus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_min = (edit_min + 1) % 60
    if edit_min < 10:
        label_min.set_text(str((str("0") + str(edit_min))))
    else:
        label_min.set_text(str(edit_min))


def button_min_minus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_min = (edit_min + -1) % 60
    if edit_min < 10:
        label_min.set_text(str((str("0") + str(edit_min))))
    else:
        label_min.set_text(str(edit_min))


def button_sec_plus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_sec = (edit_sec + 1) % 60
    if edit_sec < 10:
        label_sec.set_text(str((str("0") + str(edit_sec))))
    else:
        label_sec.set_text(str(edit_sec))


def button_sec_minus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_sec = (edit_sec + -1) % 60
    if edit_sec < 10:
        label_sec.set_text(str((str("0") + str(edit_sec))))
    else:
        label_sec.set_text(str(edit_sec))


def button_cancel_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    page_live.screen_load()


def button_save_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    rtc.init(
        (
            ((rtc.datetime())[0]),
            ((rtc.datetime())[1]),
            ((rtc.datetime())[2]),
            edit_hour,
            edit_min,
            edit_sec,
            0,
            0,
        )
    )
    page_live.screen_load()


def button_set_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_set_clicked_event(event_struct)
    return


def button_hour_plus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_hour_plus_clicked_event(event_struct)
    return


def button_hour_minus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_hour_minus_clicked_event(event_struct)
    return


def button_min_plus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_min_plus_clicked_event(event_struct)
    return


def button_min_minus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_min_minus_clicked_event(event_struct)
    return


def button_sec_plus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_sec_plus_clicked_event(event_struct)
    return


def button_sec_minus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_sec_minus_clicked_event(event_struct)
    return


def button_cancel_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_cancel_clicked_event(event_struct)
    return


def button_save_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_save_clicked_event(event_struct)
    return


def setup():
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page_live = m5ui.M5Page(bg_c=0x080808)
    page_edit = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "RTC (UTC)",
        x=24,
        y=22,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page_live,
    )
    label_date = m5ui.M5Label(
        "---- -- --",
        x=175,
        y=104,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page_live,
    )
    label_live_hour = m5ui.M5Label(
        "--",
        x=105,
        y=160,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_colon_1 = m5ui.M5Label(
        ":",
        x=175,
        y=156,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_min = m5ui.M5Label(
        "--",
        x=205,
        y=160,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_colon_2 = m5ui.M5Label(
        ":",
        x=275,
        y=156,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_sec = m5ui.M5Label(
        "--",
        x=305,
        y=160,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    button_set = m5ui.M5Button(
        text="SET TIME",
        x=32,
        y=368,
        bg_c=0x245A85,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_live,
    )
    label_edit_title = m5ui.M5Label(
        "Set UTC Time",
        x=158,
        y=22,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page_edit,
    )
    label_hour_name = m5ui.M5Label(
        "HOUR",
        x=62,
        y=72,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    label_min_name = m5ui.M5Label(
        "MIN",
        x=212,
        y=72,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    label_sec_name = m5ui.M5Label(
        "SEC",
        x=362,
        y=72,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    label_hour = m5ui.M5Label(
        "00",
        x=56,
        y=190,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_edit,
    )
    label_min = m5ui.M5Label(
        "00",
        x=206,
        y=190,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_edit,
    )
    label_sec = m5ui.M5Label(
        "00",
        x=356,
        y=190,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_edit,
    )
    button_hour_plus = m5ui.M5Button(
        text="+",
        x=36,
        y=106,
        bg_c=0x176C48,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_hour_minus = m5ui.M5Button(
        text="-",
        x=36,
        y=270,
        bg_c=0x7A2731,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_min_plus = m5ui.M5Button(
        text="+",
        x=186,
        y=106,
        bg_c=0x176C48,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_min_minus = m5ui.M5Button(
        text="-",
        x=186,
        y=270,
        bg_c=0x7A2731,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_sec_plus = m5ui.M5Button(
        text="+",
        x=336,
        y=106,
        bg_c=0x176C48,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_sec_minus = m5ui.M5Button(
        text="-",
        x=336,
        y=270,
        bg_c=0x7A2731,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_cancel = m5ui.M5Button(
        text="CANCEL",
        x=32,
        y=368,
        bg_c=0x3B4850,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_save = m5ui.M5Button(
        text="SAVE",
        x=252,
        y=368,
        bg_c=0x245A85,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )

    button_set.add_event_cb(button_set_event_handler, lv.EVENT.ALL, None)
    button_hour_plus.add_event_cb(button_hour_plus_event_handler, lv.EVENT.ALL, None)
    button_hour_minus.add_event_cb(button_hour_minus_event_handler, lv.EVENT.ALL, None)
    button_min_plus.add_event_cb(button_min_plus_event_handler, lv.EVENT.ALL, None)
    button_min_minus.add_event_cb(button_min_minus_event_handler, lv.EVENT.ALL, None)
    button_sec_plus.add_event_cb(button_sec_plus_event_handler, lv.EVENT.ALL, None)
    button_sec_minus.add_event_cb(button_sec_minus_event_handler, lv.EVENT.ALL, None)
    button_cancel.add_event_cb(button_cancel_event_handler, lv.EVENT.ALL, None)
    button_save.add_event_cb(button_save_event_handler, lv.EVENT.ALL, None)

    page_live.screen_load()
    rtc = RTC()
    button_set.set_size(416, 72)
    button_hour_plus.set_size(108, 54)
    button_hour_minus.set_size(108, 54)
    button_min_plus.set_size(108, 54)
    button_min_minus.set_size(108, 54)
    button_sec_plus.set_size(108, 54)
    button_sec_minus.set_size(108, 54)
    button_cancel.set_size(196, 72)
    button_save.set_size(196, 72)
    label_date.align_to(page_live, lv.ALIGN.TOP_MID, 0, 104)


def loop():
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    M5.update()
    label_date.set_text(
        str(
            (
                str(
                    (
                        str((str((str("") + str(((rtc.datetime())[0])))) + str("-")))
                        + str(((rtc.datetime())[1]))
                    )
                )
                + str((str("-") + str(((rtc.datetime())[2]))))
            )
        )
    )
    if (rtc.datetime())[4] < 10:
        label_live_hour.set_text(str((str("0") + str(((rtc.datetime())[4])))))
    else:
        label_live_hour.set_text(str((rtc.datetime())[4]))
    if (rtc.datetime())[5] < 10:
        label_live_min.set_text(str((str("0") + str(((rtc.datetime())[5])))))
    else:
        label_live_min.set_text(str((rtc.datetime())[5]))
    if (rtc.datetime())[6] < 10:
        label_live_sec.set_text(str((str("0") + str(((rtc.datetime())[6])))))
    else:
        label_live_sec.set_text(str((rtc.datetime())[6]))
    label_date.align_to(page_live, lv.ALIGN.TOP_MID, 0, 104)
    time.sleep_ms(100)


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
