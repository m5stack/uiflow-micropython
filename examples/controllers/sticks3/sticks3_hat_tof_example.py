# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from hat import ToFHat
import time


label_title = None
label_distance = None
label_dis = None
label_cm = None
i2c0 = None
hat_tof_0 = None
last_time = None
dis = None


def setup():
    global label_title, label_distance, label_dis, label_cm, i2c0, hat_tof_0, last_time, dis

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("HAT ToF", 27, 5, 1.0, 0x1F70D7, 0x000000, Widgets.FONTS.DejaVu18)
    label_distance = Widgets.Label(
        "Distance", 27, 55, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_dis = Widgets.Label("---", 35, 90, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu56)
    label_cm = Widgets.Label("cm", 53, 155, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    i2c0 = I2C(0, scl=Pin(0), sda=Pin(8), freq=100000)
    hat_tof_0 = ToFHat(i2c0)
    dis = 0
    Power.setBatteryCharge(True)
    Power.setExtOutput(True)


def loop():
    global label_title, label_distance, label_dis, label_cm, i2c0, hat_tof_0, last_time, dis
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 200:
        last_time = time.ticks_ms()
        dis = int(hat_tof_0.get_distance())
        if dis < 10:
            label_dis.setCursor(x=48, y=90)
        elif dis < 100:
            label_dis.setCursor(x=33, y=90)
        else:
            label_dis.setCursor(x=12, y=90)
        label_dis.setText(str(dis))
        print((str("Distance: ") + str((str(dis) + str(" cm")))))


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
