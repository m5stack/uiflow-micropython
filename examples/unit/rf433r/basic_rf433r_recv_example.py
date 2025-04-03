# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import RF433RUnit


title0 = None
label_cnt = None
rf433r_0 = None
rf433r_data = None
cnt = None


def rf433r_0_receive_event(received_data):
    global title0, label_cnt, rf433r_0, rf433r_data, cnt
    rf433r_data = received_data
    cnt = rf433r_data[-1]
    label_cnt.setText(str((str("Count: ") + str(cnt))))
    print(rf433r_data)


def setup():
    global title0, label_cnt, rf433r_0, rf433r_data, cnt
    M5.begin()
    title0 = Widgets.Title("RF433R Recv Data", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_cnt = Widgets.Label("Count", 115, 118, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18)
    rf433r_0 = RF433RUnit((36, 26))
    rf433r_0.set_recv_callback(rf433r_0_receive_event)
    rf433r_0.start_recv()


def loop():
    global title0, label_cnt, rf433r_0, rf433r_data, cnt
    M5.update()


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
