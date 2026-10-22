# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Note: This example supports StickS3 Lite and StickS3 v1.1 or later.
import os, sys, io
import M5
from M5 import *
from hardware import RTC
import time


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


def btnA_wasClicked_event(state):
    global \
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
    Speaker.tone(2000, 200)
    sw = (sw if isinstance(sw, (int, float)) else 0) + 1
    if sw == 1:
        label_hour.setColor(0xFF0000, 0x000000)
    elif sw == 2:
        label_hour.setColor(0x00CCCC, 0x000000)
        label_min.setColor(0xFF0000, 0x000000)
    elif sw == 3:
        label_min.setColor(0x00CCCC, 0x000000)
        label_second.setColor(0xFF0000, 0x000000)
    else:
        label_second.setColor(0x00CCCC, 0x000000)
        sw = 0
        rtc.init((2026, 10, 19, hour, minute, second, 584, 0))


def btnB_wasClicked_event(state):
    global \
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
    Speaker.tone(2000, 200)
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
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_tip = Widgets.Label("Clock", 33, 28, 1.0, 0x00CCCC, 0x000000, Widgets.FONTS.Montserrat24)
    label_hour = Widgets.Label("00", 21, 109, 1.0, 0x00CCCC, 0x000000, Widgets.FONTS.Montserrat18)
    label_min = Widgets.Label("00", 54, 109, 1.0, 0x00CCCC, 0x000000, Widgets.FONTS.Montserrat18)
    label_second = Widgets.Label(
        "00", 88, 109, 1.0, 0x00CCCC, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_dot1 = Widgets.Label(":", 46, 109, 1.0, 0x00CCCC, 0x000000, Widgets.FONTS.Montserrat18)
    label_dot2 = Widgets.Label(":", 81, 109, 1.0, 0x00CCCC, 0x000000, Widgets.FONTS.Montserrat18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)

    rtc = RTC()
    hour = 11
    minute = 10
    second = 0
    sw = 0
    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.tone(1000, 300)
    label_dot1.setCursor(x=47, y=109)
    label_dot2.setCursor(x=81, y=109)


def loop():
    global \
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
            label_hour.setText(str((str("0") + str(hour))))
        else:
            label_hour.setText(str(hour))
    label_hour.setCursor(x=21, y=109)
    if minute < 10:
        label_min.setText(str((str("0") + str(minute))))
    else:
        label_min.setText(str(minute))
    label_min.setCursor(x=54, y=109)
    if second < 10:
        label_second.setText(str((str("0") + str(second))))
    else:
        label_second.setText(str(second))
    label_second.setCursor(x=88, y=109)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
