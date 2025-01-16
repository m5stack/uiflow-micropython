# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import USBModule



title0 = None
label_x = None
label_y = None
module_usb_0 = None
x = None
y = None
mouse_move = None
dx = None
dy = None


def setup():
    global title0, label_x, label_y, module_usb_0, x, y, mouse_move, dx, dy
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Module USB Example mouse", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_x = Widgets.Label("x", 130, 90, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
    label_y = Widgets.Label("y", 180, 90, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
    module_usb_0 = USBModule(pin_cs=1, pin_int=10)
    x = 0
    y = 0


def loop():
    global title0, label_x, label_y, module_usb_0, x, y, mouse_move, dx, dy
    module_usb_0.poll_data()
    if module_usb_0.is_left_btn_pressed():
        print('click left')
    if module_usb_0.is_right_btn_pressed():
        print('click right')
    if module_usb_0.is_middle_btn_pressed():
        print('click middle')
    mouse_move = module_usb_0.read_mouse_move()
    dx = mouse_move[0]
    dy = mouse_move[1]
    if dx != 0 or dy != 0:
        print((str('move: ') + str(((str(dx) + str(((str(', ') + str(dy)))))))))
        x = min(max(x + dx, 0), 320)
        y = min(max(y + dy, 0), 240)
        label_x.setText(str(x))
        label_y.setText(str(y))


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

