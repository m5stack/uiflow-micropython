# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import camera
import image

img = None

def setup():
    global img
    M5.begin()
    Widgets.fillScreen(0x222222)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)

def loop():
    global img
    M5.update()
    img = camera.snapshot()
    img.draw_string(10, 10, str('M5Stack'), color=0x3366ff, scale=2)
    img.draw_rectangle(60, 80, 50, 40, color=0x33cc00, thickness=3, fill=False)
    img.draw_line(200, 60, 260, 100, color=0xff0000, thickness=3)
    img.draw_circle(160, 120, 30, color=0xffcc00, thickness=2, fill=False)
    M5.Lcd.show(img, 0, 0, 320, 240)

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
