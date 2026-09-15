# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import camera
import image


stamp_addon_cam0308_0 = None


cam_img = None


def setup():
    global stamp_addon_cam0308_0, cam_img

    M5.begin()
    camera.init(pixformat=camera.RGB565, framesize=camera.FRAME_QVGA)
    cam_img = camera.snapshot()
    cam_img.draw_string(2, 2, str("cam0308"), color=0x3366FF, scale=1)
    cam_img.draw_rectangle(2, 2, 316, 236, color=0x33CC00, thickness=1, fill=False)
    cam_img.draw_line(0, 0, 319, 239, color=0xFF0000, thickness=1)
    cam_img.draw_circle(160, 120, 50, color=0xFFCC00, thickness=1, fill=False)
    print(cam_img.width())
    print(cam_img.height())
    print(cam_img.format())
    print(cam_img.size())


def loop():
    global stamp_addon_cam0308_0, cam_img
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
