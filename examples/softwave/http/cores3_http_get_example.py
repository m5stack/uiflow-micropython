# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import requests2


label0 = None
http_req = None


def setup():
    global label0, http_req

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 6, 6, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    http_req = requests2.get(
        "https://httpbin.org/get", headers={"Content-Type": "application/json"}
    )
    label0.setText(str(http_req.text))


def loop():
    global label0, http_req
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
