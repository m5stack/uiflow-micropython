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


last_time = None


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
        last_time
    if stp2.is_ldo_enabled():
        stp2.disable_ldo()
    else:
        stp2.enable_ldo()


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
        last_time
    if stp2.is_dcdc_enabled():
        stp2.disable_dcdc()
    else:
        stp2.enable_dcdc()


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
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Power Control", 94, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "STP2 LDO / DCDC Toggle", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_caption1 = Widgets.Label(
        "LDO Output", 12, 90, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label(
        "--", 140, 86, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_caption2 = Widgets.Label(
        "DCDC Output", 12, 140, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 140, 136, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "LDO", 50, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "DCDC", 140, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "--", 248, 215, 1.0, 0x475569, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    label_key_a.setColor(0x38BDF8, 0x000000)
    label_action_a.setColor(0xE2E8F0, 0x000000)
    label_key_b.setColor(0x38BDF8, 0x000000)
    label_action_b.setColor(0xE2E8F0, 0x000000)
    label_key_c.setColor(0x475569, 0x000000)
    label_action_c.setColor(0x475569, 0x000000)
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
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        if stp2.is_ldo_enabled():
            label_value1.setText(str("On"))
        else:
            label_value1.setText(str("Off"))
        if stp2.is_dcdc_enabled():
            label_value2.setText(str("On"))
        else:
            label_value2.setText(str("Off"))
        print(
            (
                str((str((str("LDO: ") + str((stp2.is_ldo_enabled())))) + str(" DCDC: ")))
                + str((stp2.is_dcdc_enabled()))
            )
        )


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
