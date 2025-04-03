# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ECGModule
import time
import m5utils


label0 = None
title0 = None
label_hr = None
ecg_0 = None
display_width = None
ecg_data = None
last_time = None
points = None
heartrate = None
new_ecg_data = None
new_ecg_data_len = None
data_max = None
data_min = None
i = None
y0 = None
y1 = None


def setup():
    global \
        label0, \
        title0, \
        label_hr, \
        ecg_0, \
        display_width, \
        ecg_data, \
        last_time, \
        points, \
        heartrate, \
        new_ecg_data, \
        new_ecg_data_len, \
        data_max, \
        data_min, \
        y0, \
        i, \
        y1

    M5.begin()
    label0 = Widgets.Label("HearRate:", 5, 35, 1.0, 0xFF0000, 0x000000, Widgets.FONTS.DejaVu24)
    title0 = Widgets.Title("ECGModule Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_hr = Widgets.Label("  BPM", 142, 35, 1.0, 0xFF0000, 0x000000, Widgets.FONTS.DejaVu24)

    ecg_0 = ECGModule(1, tx=7, rx=1)
    display_width = M5.Lcd.width()
    ecg_data = [0] * display_width
    points = [0] * display_width


def loop():
    global \
        label0, \
        title0, \
        label_hr, \
        ecg_0, \
        display_width, \
        ecg_data, \
        last_time, \
        points, \
        heartrate, \
        new_ecg_data, \
        new_ecg_data_len, \
        data_max, \
        data_min, \
        y0, \
        i, \
        y1
    M5.update()
    ecg_0.poll_data()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 200:
        last_time = time.ticks_ms()
        heartrate = ecg_0.read_heartrate()
        if heartrate > 0:
            label0.setColor(0x00FF00, 0x000000)
            label_hr.setColor(0x00FF00, 0x000000)
            label_hr.setText(str((str(heartrate) + str("BPM"))))
        else:
            label0.setColor(0xFF0000, 0x000000)
            label_hr.setText(str(" "))
        new_ecg_data = ecg_0.read_raw_ecg_data()
        if new_ecg_data:
            new_ecg_data_len = len(new_ecg_data)
            ecg_data = ecg_data[int((new_ecg_data_len + 1) - 1) :]
            ecg_data = ecg_data + new_ecg_data
            data_max = max(ecg_data)
            data_min = min(ecg_data)
            data_max = data_max + data_max / 10
            data_min = data_min - data_min / 10
            if data_min < 0:
                data_min = 0
            for i in range(display_width):
                points[int((i + 1) - 1)] = m5utils.remap(
                    ecg_data[int((i + 1) - 1)], data_min, data_max, 150, 0
                )

            M5.Lcd.fillRect(0, 70, display_width, 155, 0x000000)
            for i in range(display_width - 1):
                y0 = int(70 + points[int((i + 1) - 1)])
                y1 = int(70 + points[int((i + 2) - 1)])
                M5.Lcd.drawLine(i + 1, y0, i + 2, y1, 0xFF0000)


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
