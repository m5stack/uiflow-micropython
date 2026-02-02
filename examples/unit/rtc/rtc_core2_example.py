# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Pin
from hardware import I2C
from unit import RTC8563Unit
import time


page0 = None
label0 = None
i2c0 = None
rtc_0 = None


str2 = None


def setup():
    global page0, label0, i2c0, rtc_0, str2

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "label0",
        x=3,
        y=99,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    rtc_0 = RTC8563Unit(i2c0)
    page0.screen_load()
    rtc_0.set_date_time(3, 49, 15, 0, 2, 2, 26)
    str2 = ""


def loop():
    global page0, label0, i2c0, rtc_0, str2
    M5.update()
    str2 = str("Time: ") + str(
        (
            str((rtc_0.get_date_time(6)))
            + str(
                (
                    str(".")
                    + str(
                        (
                            str((rtc_0.get_date_time(5)))
                            + str(
                                (
                                    str(".")
                                    + str(
                                        (
                                            str((rtc_0.get_date_time(4)))
                                            + str(
                                                (
                                                    str(" ")
                                                    + str(
                                                        (
                                                            str((rtc_0.get_date_time(2)))
                                                            + str(
                                                                (
                                                                    str(":")
                                                                    + str(
                                                                        (
                                                                            str(
                                                                                (
                                                                                    rtc_0.get_date_time(
                                                                                        1
                                                                                    )
                                                                                )
                                                                            )
                                                                            + str(
                                                                                (
                                                                                    str(":")
                                                                                    + str(
                                                                                        (
                                                                                            str(
                                                                                                (
                                                                                                    rtc_0.get_date_time(
                                                                                                        0
                                                                                                    )
                                                                                                )
                                                                                            )
                                                                                            + str(
                                                                                                ""
                                                                                            )
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    print(str2)
    label0.set_text(str(str2))
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
