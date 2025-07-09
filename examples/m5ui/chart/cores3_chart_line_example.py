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
from unit import ENVUnit
import time


page0 = None
chart0 = None
i2c0 = None
series_temp = None
series_humi = None
env3_0 = None


def setup():
    global page0, chart0, i2c0, series_temp, series_humi, env3_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    chart0 = m5ui.M5Chart(
        x=43,
        y=40,
        w=240,
        h=160,
        chart_type=lv.chart.TYPE.LINE,
        point_num=10,
        hdiv=3,
        vdiv=5,
        bg_radius=7,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        border_w=2,
        parent=page0,
    )
    chart0.y_axis1_init(
        min_value=0,
        max_value=50,
        major_ticks=3,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    )
    chart0.y_axis2_init(
        min_value=0,
        max_value=100,
        major_ticks=3,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    env3_0 = ENVUnit(i2c=i2c0, type=3)
    page0.screen_load()
    series_temp = chart0.add_series(0xFF0000, lv.chart.AXIS.PRIMARY_Y)
    series_humi = chart0.add_series(0x009900, lv.chart.AXIS.SECONDARY_Y)
    chart0.set_update_mode(lv.chart.UPDATE_MODE.SHIFT)
    chart0.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    chart0.set_style_size(0, 0, lv.PART.INDICATOR | lv.STATE.DEFAULT)


def loop():
    global page0, chart0, i2c0, series_temp, series_humi, env3_0
    M5.update()
    chart0.set_next_value(series_temp, int(env3_0.read_temperature()))
    chart0.set_next_value(series_humi, int(env3_0.read_humidity()))
    time.sleep(1)


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
