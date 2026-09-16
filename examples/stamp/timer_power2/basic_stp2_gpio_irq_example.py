# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from driver.m5pm1 import EVENT
from hardware import Pin
from hardware import I2C
import time


label_title = None
label_description = None
label_note = None
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


count = None
event_handle = None
event_data = None
running = None
removed = None
last_time = None
level = None


# Describe this function...
def start_irq():
    global \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level, \
        label_title, \
        label_description, \
        label_note, \
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
        stp2
    stp2 = StampTimerPower2(i2c0, pm1_int_gpio=0, mcu_int_gpio=26)
    event_handle = stp2.add_event_cb(stp2_gpio4_change_event, EVENT.GPIO4_CHANGE)
    stp2.wake()
    stp2.set_pin_pull(4, StampTimerPower2.GPIO_PULL_UP)
    running = 1
    label_note.setText(str("G4: connect to GND / release"))


def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_note, \
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
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    count = 0


def stp2_gpio4_change_event(event):
    global \
        label_title, \
        label_description, \
        label_note, \
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
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    event_data = event.user_data
    count = count + 1


def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_note, \
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
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    if running:
        removed = stp2.remove_event_cb(event_handle)
        stp2.deinit()
        event_handle = None
        running = 0
        label_note.setText(str("PAUSED"))


def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_note, \
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
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    if running == 0:
        start_irq()


def setup():
    global \
        label_title, \
        label_description, \
        label_note, \
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
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "GPIO Interrupt", 91, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "IRQ: STP2 G0 -> Basic G26", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_note = Widgets.Label(
        "G4: connect to GND / release", 12, 54, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_caption1 = Widgets.Label(
        "G4 Change Count", 12, 78, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "G4 Level", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Clear", 46, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Pause", 135, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "Resume", 222, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    count = 0
    running = 0
    start_irq()


def loop():
    global \
        label_title, \
        label_description, \
        label_note, \
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
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        label_value1.setText(str(count))
        level = stp2.read_pin(4)
        if level:
            label_value2.setText(str("HIGH (1)"))
        else:
            label_value2.setText(str("LOW (0)"))
        print((str("G4 IRQ count: ") + str(count)))


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
