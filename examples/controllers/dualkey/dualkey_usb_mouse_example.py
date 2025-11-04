# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import RGB
from usb.device.mouse import Mouse
import time


rgb = None
mouse = None
click_left = None
click_right = None
last_time = None


def btna_was_clicked_event(state):
    global rgb, mouse, click_left, click_right, last_time
    print("click left")
    click_left = True


def btnb_was_clicked_event(state):
    global rgb, mouse, click_left, click_right, last_time
    print("click right")
    click_right = True


def setup():
    global rgb, mouse, click_left, click_right, last_time

    M5.begin()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    rgb = RGB()
    rgb.set_color(0, 0x3333FF)
    rgb.set_color(1, 0x3333FF)
    mouse = Mouse()


def loop():
    global rgb, mouse, click_left, click_right, last_time
    M5.update()
    if click_left:
        click_left = False
        if mouse.is_open():
            mouse.click_left(True)
            rgb.set_color(0, 0x009900)
            rgb.set_color(1, 0x000000)
            last_time = time.ticks_ms()
    if click_right:
        click_right = False
        if mouse.is_open():
            mouse.click_right(True)
            rgb.set_color(0, 0x000000)
            rgb.set_color(1, 0x009900)
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 300:
        rgb.set_color(0, 0x000000)
        rgb.set_color(1, 0x000000)


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
