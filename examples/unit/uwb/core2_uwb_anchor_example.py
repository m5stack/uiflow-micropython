# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import UWBUnit


label0 = None
label4 = None
label1 = None
label5 = None
label2 = None
label6 = None
label3 = None
label7 = None
circle0 = None
circle1 = None
circle2 = None
circle3 = None
uwb_0 = None


def uwb_0_0_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle0.setColor(color=0x33FF33, fill_c=0x33FF33)


def uwb_0_1_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle1.setColor(color=0x33FF33, fill_c=0x33FF33)


def uwb_0_2_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle2.setColor(color=0x33FF33, fill_c=0x33FF33)


def uwb_0_3_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle3.setColor(color=0x33FF33, fill_c=0x33FF33)


def uwb_0_0_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle0.setColor(color=0xFF0000, fill_c=0xFF0000)


def uwb_0_1_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle1.setColor(color=0xFF0000, fill_c=0xFF0000)


def uwb_0_2_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle2.setColor(color=0xFF0000, fill_c=0xFF0000)


def uwb_0_3_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle3.setColor(color=0xFF0000, fill_c=0xFF0000)


def setup():
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Anchor0", 0, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("label4", 0, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label1 = Widgets.Label("Anchor1", 80, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 80, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label2 = Widgets.Label("Anchor2", 160, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 160, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label3 = Widgets.Label("Anchor3", 240, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 240, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    circle0 = Widgets.Circle(38, 50, 15, 0xFF0000, 0xFF0000)
    circle1 = Widgets.Circle(118, 52, 15, 0xFF0000, 0xFF0000)
    circle2 = Widgets.Circle(193, 51, 15, 0xFF0000, 0xFF0000)
    circle3 = Widgets.Circle(273, 51, 15, 0xFF0000, 0xFF0000)

    uwb_0 = UWBUnit(2, port=(33, 32), device_mode=UWBUnit.TAG, verbose=False)
    uwb_0.set_callback(0, uwb_0.ONLINE, uwb_0_0_online_event)
    uwb_0.set_callback(1, uwb_0.ONLINE, uwb_0_1_online_event)
    uwb_0.set_callback(2, uwb_0.ONLINE, uwb_0_2_online_event)
    uwb_0.set_callback(3, uwb_0.ONLINE, uwb_0_3_online_event)
    uwb_0.set_callback(0, uwb_0.OFFLINE, uwb_0_0_offline_event)
    uwb_0.set_callback(1, uwb_0.OFFLINE, uwb_0_1_offline_event)
    uwb_0.set_callback(2, uwb_0.OFFLINE, uwb_0_2_offline_event)
    uwb_0.set_callback(3, uwb_0.OFFLINE, uwb_0_3_offline_event)
    uwb_0.set_measurement_interval(5)
    uwb_0.set_measurement(True)


def loop():
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    M5.update()
    uwb_0.update()
    label4.setText(str(uwb_0.get_distance(0)))
    label5.setText(str(uwb_0.get_distance(1)))
    label6.setText(str(uwb_0.get_distance(2)))
    label7.setText(str(uwb_0.get_distance(3)))


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
