# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from base import Motion
import time


label_speed = None
title_e = None
label_vol = None
label_cur = None
label_pow = None
i2c0 = None
motion = None
speed = None
voltage = None
curent = None
last_time = None
power = None


def btnA_wasClicked_event(state):
    global \
        label_speed, \
        title_e, \
        label_vol, \
        label_cur, \
        label_pow, \
        i2c0, \
        motion, \
        speed, \
        voltage, \
        curent, \
        last_time, \
        power
    speed = speed + 20
    if speed > 120:
        speed = 0
    motion.set_motor_speed(1, speed)
    label_speed.setText(str((str("speed: ") + str(speed))))


def setup():
    global \
        label_speed, \
        title_e, \
        label_vol, \
        label_cur, \
        label_pow, \
        i2c0, \
        motion, \
        speed, \
        voltage, \
        curent, \
        last_time, \
        power
    M5.begin()
    label_speed = Widgets.Label("speed：", 5, 27, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    title_e = Widgets.Title("Motor Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("vol:", 5, 55, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_cur = Widgets.Label("cur:", 5, 75, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_pow = Widgets.Label("pow:", 5, 95, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
    motion = Motion(i2c0, 0x38)
    last_time = time.ticks_us()
    speed = 0
    label_speed.setText(str((str("speed: ") + str(speed))))


def loop():
    global \
        label_speed, \
        title_e, \
        label_vol, \
        label_cur, \
        label_pow, \
        i2c0, \
        motion, \
        speed, \
        voltage, \
        curent, \
        last_time, \
        power
    M5.update()
    voltage = motion.read_voltage()
    curent = motion.read_current()
    power = motion.read_power()
    label_vol.setText(str((str("vol: ") + str(voltage))))
    label_cur.setText(str((str("cur: ") + str(curent))))
    label_pow.setText(str((str("pow: ") + str(power))))


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
