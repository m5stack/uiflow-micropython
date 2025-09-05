# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import camera
import image


img = None
qrcode_list = None
qrcode_res = None
corners = None
i = None
point = None
coord = None
x0 = None
y0 = None
x1 = None
y1 = None


def setup():
    global img, qrcode_list, corners, point, i, coord, x0, y0, x1, y1
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)


def loop():
    global img, qrcode_list, corners, point, i, coord, x0, y0, x1, y1
    M5.update()
    img = camera.snapshot()
    qrcode_list = img.find_qrcodes()
    if qrcode_list:
        for qrcode_res in qrcode_list:
            corners = qrcode_res.corners()
            for i in range(len(corners)):
                point = i
                coord = corners[int((point + 1) - 1)]
                x0 = coord[0]
                y0 = coord[1]
                point = (i + 1) % len(corners)
                coord = corners[int((point + 1) - 1)]
                x1 = coord[0]
                y1 = coord[1]
                img.draw_line(x0, y0, x1, y1, color=0x3333FF, thickness=3)
            img.draw_string(0, 0, str(qrcode_res.payload()), color=0x3333FF, scale=1.5)
    M5.Lcd.show(img, 0, 0, 320, 240)


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
