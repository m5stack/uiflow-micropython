# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import ToFChain
import time



title0 = None
label_dis = None
bus2 = None
chain_tof_0 = None
last_time = None
distance = None


def setup():
    global title0, label_dis, bus2, chain_tof_0, last_time, distance

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Chain ToF Example", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_dis = Widgets.Label("Distance: --", 20, 92, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_tof_0 = ToFChain(bus2, 1)
    chain_tof_0.set_rgb_color(0x33ccff)
    chain_tof_0.set_rgb_brightness(10, save=False)
    chain_tof_0.set_measure_mode(ToFChain.MODE_CONTINUOUS)


def loop():
    global title0, label_dis, bus2, chain_tof_0, last_time, distance
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        distance = chain_tof_0.get_distance()
        label_dis.setText(str((str('Distance: ') + str(((str(distance) + str(' mm')))))))


if __name__ == '__main__':
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
