# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import DualKmeterModule


label0 = None
label1 = None
label2 = None
label3 = None
km_0 = None


def setup():
    global label0, label1, label2, label3, km_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 39, 41, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 202, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text", 17, 139, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Text", 174, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    km_0 = DualKmeterModule(address=0x11)
    km_0.set_kmeter_channel(0)
    label0.setText(str(km_0.get_kmeter_channel()))
    label0.setText(str(km_0.get_fw_ver()))


def loop():
    global label0, label1, label2, label3, km_0
    M5.update()
    if km_0.is_ready():
        label0.setText(str(km_0.get_thermocouple_temperature(scale=km_0.CELSIUS)))
        label1.setText(str(km_0.get_thermocouple_temperature_string(scale=km_0.CELSIUS)))
        label2.setText(str(km_0.get_kmeter_temperature(scale=km_0.CELSIUS)))
        label3.setText(str(km_0.get_kmeter_temperature_string(scale=km_0.CELSIUS)))


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
