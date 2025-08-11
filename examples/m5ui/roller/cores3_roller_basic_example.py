import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
roller0 = None


def setup():
    global page0, roller0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    roller0 = m5ui.M5Roller(
        x=110,
        y=71,
        w=100,
        h=0,
        options=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        mode=lv.roller.MODE.INFINITE,
        selected=0,
        visible_row_count=3,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    print(roller0.get_options())


def loop():
    global page0, roller0
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
