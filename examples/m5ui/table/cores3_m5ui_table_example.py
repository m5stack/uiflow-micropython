# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
table0 = None
table = None
i = None
info = None
row = None
k = None


def setup():
    global page0, table0, table, i, info, row, k

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    table0 = m5ui.M5Table(x=10, y=35, w=300, h=180, row_cnt=3, col_cnt=3, parent=page0)
    table = m5ui.M5Label(
        "M5UI Table Example",
        x=35,
        y=2,
        text_c=0x0000FF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    page0.screen_load()
    for i in range(3):
        table0.set_column_width(i, 85)

    table0.set_column_count(3)
    table0.set_row_count(4)
    table0.set_width(260)
    table0.align_to(page0, lv.ALIGN.CENTER, 0, 10)
    table0.set_cell_value(0, 0, "name")
    table0.set_cell_value(0, 1, "age")
    table0.set_cell_value(0, 2, "score")
    info = {"name": ["Alice", "Bob", "Carol"], "age": [18, 18, 17], "score": [95, 80, 86]}
    row = 1
    for k in info["name"]:
        table0.set_cell_value(row, 0, k)
        row = row + 1
    row = 1
    for k in info["age"]:
        table0.set_cell_value(row, 1, str(k))
        row = row + 1
    row = 1
    for k in info["score"]:
        table0.set_cell_value(row, 2, str(k))
        row = row + 1


def loop():
    global page0, table0, table, i, info, row, k
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
