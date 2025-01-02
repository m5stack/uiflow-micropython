# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from usb.device.mouse import Mouse
import time
import m5utils



label0 = None
mouse = None
touch_active = None
sensitivity = None
x = None
last_touch_time = None
y = None
dx = None
click_active = None
dy = None
prev_x = None
prev_y = None


def setup():
    global label0, mouse, touch_active, sensitivity, x, last_touch_time, y, dx, click_active, dy, prev_x, prev_y
    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("USB Mouse", 91, 6, 1.0, 0x158ee6, 0x222222, Widgets.FONTS.DejaVu24)
    mouse = Mouse()
    touch_active = False
    sensitivity = 2
    last_touch_time = 0
    click_active = False


def loop():
    global label0, mouse, touch_active, sensitivity, x, last_touch_time, y, dx, click_active, dy, prev_x, prev_y
    M5.update()
    if mouse.is_open():
        if M5.Touch.getCount():
            x = m5utils.remap(M5.Touch.getX(), 0, 320, -127, 127)
            y = m5utils.remap(M5.Touch.getY(), 0, 240, -127, 127)
            if not touch_active:
                touch_active = True
                prev_x = x
                prev_y = y
                last_touch_time = time.ticks_ms()
            if x != prev_x or y != prev_y:
                dx = x - prev_x
                dy = y - prev_y
                prev_x = x
                prev_y = y
                mouse.move(int(dx * sensitivity), int(dy * sensitivity))
        else:
            touch_active = False
            dx = 0
            dy = 0
            if (time.ticks_diff((time.ticks_ms()), last_touch_time)) < 100:
                if click_active and dx < 30 and dy < 30:
                    click_active = False
                    mouse.click_left(True)
            else:
                click_active = True
        if BtnPWR.wasClicked():
            mouse.click_right(True)
    else:
        time.sleep_ms(100)


if __name__ == '__main__':
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

