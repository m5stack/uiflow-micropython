# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from hardware import Pin
from hardware import I2C
import time


label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None


level = None
last_time = None
actual = None


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    level = 0
    stp2.set_pin_value(3, level)


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    level = 1 - level
    stp2.set_pin_value(3, level)


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    level = 1
    stp2.set_pin_value(3, level)


def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "GPIO Output", 99, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "G3 -> meter or resistor + LED",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "G3 Output Command", 12, 78, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "G3 Pin Readback", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Low", 50, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Toggle", 140, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "High", 235, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    level = 0
    stp2.set_pin_mode(3, StampTimerPower2.GPIO_MODE_IN)
    stp2.set_pin_function(3, StampTimerPower2.PIN_FUNCTION_GPIO)
    stp2.set_pin_pull(3, StampTimerPower2.GPIO_PULL_NONE)
    stp2.set_pin_value(3, 0)
    stp2.set_pin_mode(3, StampTimerPower2.GPIO_MODE_OUT)
    last_time = time.ticks_ms()


def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        actual = stp2.read_pin(3)
        if level:
            label_value1.setText(str("High (1)"))
        else:
            label_value1.setText(str("Low (0)"))
        if actual:
            label_value2.setText(str("High (1)"))
        else:
            label_value2.setText(str("Low (0)"))
        print((str((str((str("G3 command: ") + str(level))) + str(" readback: "))) + str(actual)))


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
