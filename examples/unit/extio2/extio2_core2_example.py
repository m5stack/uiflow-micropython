# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import EXTIO2Unit


title0 = None
label0 = None
i2c0 = None
extio2_0 = None


def setup():
    global title0, label0, i2c0, extio2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ExtIO2Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("IO6 State:", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    extio2_0 = EXTIO2Unit(i2c0)
    extio2_0.set_config_mode(0, 1)
    extio2_0.set_config_mode(6, 2)
    extio2_0.set_config_mode(3, 4)
    extio2_0.write_rgb_led(3, 0xFF0000)


def loop():
    global title0, label0, i2c0, extio2_0
    M5.update()
    label0.setText(str((str("IO6 State:") + str((extio2_0.read_adc12_pin(0))))))


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
