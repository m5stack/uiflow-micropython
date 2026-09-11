# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Pin
from hardware import I2C
from unit import DoF10Unit
import time


page0 = None
title = None
unit_label = None
range_label = None
axis_x = None
axis_y = None
axis_z = None
slider_x = None
slider_y = None
slider_z = None
label_x_value = None
label_y_value = None
label_z_value = None
scale_low = None
scale_zero = None
scale_high = None
i2c0 = None
dof10_0 = None


last_time = None
UPDATE_DURATION_MS = None
accel = None


def setup():
    global \
        page0, \
        title, \
        unit_label, \
        range_label, \
        axis_x, \
        axis_y, \
        axis_z, \
        slider_x, \
        slider_y, \
        slider_z, \
        label_x_value, \
        label_y_value, \
        label_z_value, \
        scale_low, \
        scale_zero, \
        scale_high, \
        i2c0, \
        dof10_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        accel

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x10171D)
    title = m5ui.M5Label(
        "DoF10 / Accel Vector",
        x=12,
        y=8,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    unit_label = m5ui.M5Label(
        "m/s2",
        x=274,
        y=11,
        text_c=0x4CD7D0,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    range_label = m5ui.M5Label(
        "Range  -20.0 ~ +20.0",
        x=12,
        y=34,
        text_c=0x8FA1AD,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )
    axis_x = m5ui.M5Label(
        "X",
        x=11,
        y=69,
        text_c=0xFF6B6B,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    axis_y = m5ui.M5Label(
        "Y",
        x=11,
        y=115,
        text_c=0x63D08C,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    axis_z = m5ui.M5Label(
        "Z",
        x=11,
        y=159,
        text_c=0x63A8FF,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    slider_x = m5ui.M5Slider(
        x=44,
        y=70,
        w=200,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=-200,
        max_value=200,
        value=0,
        bg_c=0x27323A,
        color=0xFF6B6B,
        parent=page0,
    )
    slider_y = m5ui.M5Slider(
        x=44,
        y=115,
        w=200,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=-200,
        max_value=200,
        value=0,
        bg_c=0x27323A,
        color=0x63D08C,
        parent=page0,
    )
    slider_z = m5ui.M5Slider(
        x=44,
        y=160,
        w=200,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=-200,
        max_value=200,
        value=0,
        bg_c=0x27323A,
        color=0x63A8FF,
        parent=page0,
    )
    label_x_value = m5ui.M5Label(
        "0.00",
        x=260,
        y=70,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_y_value = m5ui.M5Label(
        "0.00",
        x=260,
        y=115,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_z_value = m5ui.M5Label(
        "0.00",
        x=260,
        y=160,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    scale_low = m5ui.M5Label(
        "-20",
        x=55,
        y=211,
        text_c=0x8FA1AD,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )
    scale_zero = m5ui.M5Label(
        "0",
        x=153,
        y=211,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )
    scale_high = m5ui.M5Label(
        "+20",
        x=235,
        y=211,
        text_c=0x8FA1AD,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof10_0 = DoF10Unit(i2c0, addr=0x68)
    page0.screen_load()
    UPDATE_DURATION_MS = 100
    last_time = time.ticks_ms()


def loop():
    global \
        page0, \
        title, \
        unit_label, \
        range_label, \
        axis_x, \
        axis_y, \
        axis_z, \
        slider_x, \
        slider_y, \
        slider_z, \
        label_x_value, \
        label_y_value, \
        label_z_value, \
        scale_low, \
        scale_zero, \
        scale_high, \
        i2c0, \
        dof10_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        accel
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        accel = dof10_0.get_accel()
        slider_x.set_value(int(accel[0] * 10), True)
        label_x_value.set_text(str(round(accel[0], 2)))
        slider_y.set_value(int(accel[1] * 10), True)
        label_y_value.set_text(str(round(accel[1], 2)))
        slider_z.set_value(int(accel[2] * 10), True)
        label_z_value.set_text(str(round(accel[2], 2)))


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
