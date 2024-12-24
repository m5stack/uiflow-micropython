# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import PPSModule
import time


label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
pps_0 = None


def setup():
    global label0, label1, label2, label3, label4, label5, pps_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label(
        "Output Voltage:", 20, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Output Current:", 20, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Mode:", 22, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 180, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("label4", 180, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 180, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pps_0 = PPSModule(address=0x35)
    pps_0.set_output_voltage(5.5)
    pps_0.set_output_current(1)
    pps_0.enable_output()


def loop():
    global label0, label1, label2, label3, label4, label5, pps_0
    M5.update()
    label3.setText(str(pps_0.read_output_voltage()))
    label4.setText(str(pps_0.read_output_current()))
    label5.setText(str(pps_0.read_psu_running_mode()))
    time.sleep_ms(100)


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
