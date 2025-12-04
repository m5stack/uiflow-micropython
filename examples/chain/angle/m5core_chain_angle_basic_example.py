# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import AngleChain
import time
import m5utils


title0 = None
label_brightness = None
label_val = None
bus2 = None
chain_angle_0 = None
last_time = None
value = None
brightness = None


def setup():
    global title0, label_brightness, label_val, bus2, chain_angle_0, last_time, value, brightness
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Chain Angle Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_brightness = Widgets.Label(
        "Brightness: ", 5, 117, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_val = Widgets.Label("Value:", 5, 69, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_angle_0 = AngleChain(bus2, 1)
    chain_angle_0.set_rgb_color(0x00CCCC)


def loop():
    global title0, label_brightness, label_val, bus2, chain_angle_0, last_time, value, brightness
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        value = chain_angle_0.get_adc8()
        brightness = int(m5utils.remap(value, 0, 255, 0, 100))
        label_val.setText(str((str("Value: ") + str(value))))
        label_brightness.setText(str((str("Brightness: ") + str(brightness))))
        chain_angle_0.set_rgb_brightness(brightness, save=False)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
