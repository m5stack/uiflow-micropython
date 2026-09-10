# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import Servos8V2Unit


label_title = None
label_channel = None
label_angle = None
label_sel = None
label_increase = None
label_decrease = None
i2c0 = None
servos8v2_0 = None
channel = None
angle = None
i = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
    channel = (channel if isinstance(channel, (int, float)) else 0) + 1
    if channel >= 9:
        channel = 0
    if channel == 8:
        label_channel.setText(str("Channel: all"))
        for i in range(7):
            servos8v2_0.set_servo_angle(i, angle)
    else:
        label_channel.setText(str((str("Channel: ") + str(channel))))
        servos8v2_0.set_servo_angle(channel, angle)


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
    angle = angle + 10
    if angle >= 180:
        angle = 0
    if channel == 8:
        for i in range(7):
            servos8v2_0.set_servo_angle(i, angle)
    else:
        servos8v2_0.set_servo_angle(channel, angle)
    label_angle.setText(str((str("Angle: ") + str(angle))))


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
    angle = angle - 10
    if angle <= 0:
        angle = 180
    if channel == 8:
        for i in range(7):
            servos8v2_0.set_servo_angle(i, angle)
    else:
        servos8v2_0.set_servo_angle(channel, angle)
    label_angle.setText(str((str("Angle: ") + str(angle))))


def setup():
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Servo Control", 76, 2, 1.0, 0x1393E8, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_channel = Widgets.Label(
        "Channel: 1", 36, 77, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_angle = Widgets.Label(
        "Angle: 0", 40, 112, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_sel = Widgets.Label(
        "select", 43, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat16
    )
    label_increase = Widgets.Label(
        "+10", 143, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat16
    )
    label_decrease = Widgets.Label(
        "-10", 233, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat16
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    servos8v2_0 = Servos8V2Unit(i2c0, 0x25)
    channel = 0
    angle = 0
    for i in range(7):
        servos8v2_0.set_channel_mode(i, Servos8V2Unit.MODE_SERVO)
        servos8v2_0.set_servo_angle(i, 0)


def loop():
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
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
