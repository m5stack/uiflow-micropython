# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from stamp import StampTimerPower2
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


import math

intensity = None
color_index = None
brightness = None
color_name = None
led_index = None
last_time = None
red = None
LED_COUNT = None
green = None
blue = None


# Describe this function...
def update_leds():
    global \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        led_index, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        blue, \
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
        stp2
    intensity = math.floor((255 * brightness) / 100)
    if color_index == 0:
        color_name = "Red"
        red = intensity
        green = 0
        blue = 0
    else:
        if color_index == 1:
            color_name = "Green"
            red = 0
            green = intensity
            blue = 0
        else:
            if color_index == 2:
                color_name = "Blue"
                red = 0
                green = 0
                blue = intensity
            else:
                color_name = "White"
                red = intensity
                green = intensity
                blue = intensity
    for led_index in range(LED_COUNT):
        stp2.set_neopixel_color(led_index, (red << 16) | (green << 8) | blue)

    stp2.refresh_neopixels()


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
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    color_index = (color_index + 1) % 4
    update_leds()


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
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    if brightness > 0:
        brightness = brightness + -10
    update_leds()


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
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    if brightness < 100:
        brightness = brightness + 10
    update_leds()


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
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Neopixel Output", 83, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "LED DIN -> G0; shared GND", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_caption1 = Widgets.Label(
        "LED Color", 12, 78, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "Brightness", 12, 134, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Color", 50, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Dim -10%", 125, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "Up +10%", 222, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    LED_COUNT = 1
    color_index = 0
    brightness = 20
    stp2.set_pin_drive(0, StampTimerPower2.DRIVE_PUSH_PULL)
    stp2.set_pin_function(0, StampTimerPower2.PIN_FUNCTION_OTHER)
    stp2.set_neopixel_count(LED_COUNT)
    update_leds()
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
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        label_value1.setText(str(color_name))
        label_value2.setText(str((str(brightness) + str("%"))))
        print(
            (str((str((str("LED: ") + str(color_name))) + str(" brightness: "))) + str(brightness))
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
