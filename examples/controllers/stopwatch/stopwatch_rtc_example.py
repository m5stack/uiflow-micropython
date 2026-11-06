import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import RTC
import time


page0 = None
label_tip = None
label_hour = None
label_min = None
label_second = None
label_dot1 = None
label_dot2 = None
rtc = None


sw = None
hour = None
minute = None
second = None
last_time = None


def btna_was_click_event(state):
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time
    Speaker.tone(1000, 200)
    sw = (sw if isinstance(sw, (int, float)) else 0) + 1
    if sw == 1:
        label_hour.set_text_color(0xFF0000, 255, 0)
    elif sw == 2:
        label_hour.set_text_color(0x00CCCC, 255, 0)
        label_min.set_text_color(0xFF0000, 255, 0)
    elif sw == 3:
        label_min.set_text_color(0x00CCCC, 255, 0)
        label_second.set_text_color(0xFF0000, 255, 0)
    else:
        label_second.set_text_color(0x00CCCC, 255, 0)
        sw = 0
        rtc.init((2026, 5, 21, hour, minute, second, 339, 0))


def btnb_was_click_event(state):
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time
    Speaker.tone(1000, 200)
    if sw == 1:
        hour = (hour if isinstance(hour, (int, float)) else 0) + 1
        if hour > 23:
            hour = 0
    elif sw == 2:
        minute = (minute if isinstance(minute, (int, float)) else 0) + 1
        if minute > 59:
            minute = 0
    elif sw == 3:
        second = (second if isinstance(second, (int, float)) else 0) + 1
        if second > 59:
            second = 0
    else:
        sw = 0


def setup():
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_tip = m5ui.M5Label(
        "Clock",
        x=176,
        y=40,
        text_c=0x10AACD,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_hour = m5ui.M5Label(
        "00",
        x=100,
        y=208,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_min = m5ui.M5Label(
        "00",
        x=200,
        y=206,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_second = m5ui.M5Label(
        "00",
        x=300,
        y=205,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_dot1 = m5ui.M5Label(
        ":",
        x=177,
        y=202,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_dot2 = m5ui.M5Label(
        ":",
        x=275,
        y=202,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_click_event)

    page0.screen_load()
    rtc = RTC()
    rtc.timezone("GMT0")
    hour = 11
    minute = 10
    second = 0
    sw = 0
    label_dot1.align_to(page0, lv.ALIGN.TOP_MID, -45, 201)
    label_dot2.align_to(page0, lv.ALIGN.TOP_MID, 45, 201)
    Speaker.begin()
    Speaker.setVolumePercentage(0.9)
    Speaker.tone(1000, 300)


def loop():
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        if sw == 0:
            hour = (rtc.local_datetime())[4]
            minute = (rtc.local_datetime())[5]
            second = (rtc.local_datetime())[6]
        if hour < 10:
            label_hour.set_text(str((str("0") + str(hour))))
        else:
            label_hour.set_text(str(hour))
        label_hour.align_to(page0, lv.ALIGN.TOP_MID, -90, 205)
        if minute < 10:
            label_min.set_text(str((str("0") + str(minute))))
        else:
            label_min.set_text(str(minute))
        label_min.align_to(page0, lv.ALIGN.TOP_MID, 0, 205)
        if second < 10:
            label_second.set_text(str((str("0") + str(second))))
        else:
            label_second.set_text(str(second))
        label_second.align_to(page0, lv.ALIGN.TOP_MID, 90, 205)


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
